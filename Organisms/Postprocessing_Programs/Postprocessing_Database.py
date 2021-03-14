#!/usr/bin/env python3
'''
Postprocessing_Database.py, Geoffrey Weal, 26/9/2020

This program is designed to break down the database from the GA_Recording_System into manageable chunks if the original database was too large to process.
'''
import os, sys
import numpy as np
from shutil import rmtree
from math import ceil

#from ase.db.row import row2dct
from ase.db import connect

def get_distance(atom1,atom2):
	diff_x = atom1.x - atom2.x
	diff_y = atom1.y - atom2.y
	diff_z = atom1.z - atom2.z
	distance = (diff_x**2.0 + diff_y**2.0 + diff_z**2.0)**0.5
	return distance

def get_cluster_interatomic_distances(cluster):
	cluster_interatomic_distances = {}
	for index1 in range(len(cluster)):
		for index2 in range(index1+1,len(cluster)):
			cluster_interatomic_distances[(index1,index2)] = round(get_distance(cluster[index1],cluster[index2]),4)
	return cluster_interatomic_distances

def compared_cluster_interatomic_distances(cluster_interatomic_distances_1, cluster2):
	for index1 in range(len(cluster2)):
		for index2 in range(index1+1,len(cluster2)):
			cluster2_interatomic_distance = round(get_distance(cluster2[index1],cluster[index2]),4)
			cluster1_interatomic_distance = cluster_interatomic_distances_1[(index1,index2)]
			if not cluster2_interatomic_distance == cluster1_interatomic_distance:
				exit('Error')

def get_rotation_matrix(i_v, unit=None):
    # From http://www.j3d.org/matrix_faq/matrfaq_latest.html#Q38
    if unit is None:
        unit = (0.0,0.0,1.0)
    # Normalize vector length
    i_v /= np.linalg.norm(i_v)
    # Get axis
    uvw = np.cross(i_v, unit)
    # compute trig values - no need to go through arccos and back
    rcos = np.dot(i_v, unit)
    rsin = np.linalg.norm(uvw)
    #normalize and unpack axis
    if not np.isclose(rsin, 0):
        uvw /= rsin
    u, v, w = uvw
    # Compute rotation matrix - re-expressed to show structure
    return (
        rcos * np.eye(3) +
        rsin * np.array([
            [ 0, -w,  v],
            [ w,  0, -u],
            [-v,  u,  0]
        ]) +
        (1.0 - rcos) * uvw[:,None] * uvw[None,:]
    )

def rotate_cluster_to_major_inertia_vector(cluster):
	"""
	This method will rotate its axis such that the cluster 
	"""
	evals, evecs = cluster.get_moments_of_inertia(vectors=True)
	major_evec = evecs[0]
	matrix = get_rotation_matrix(major_evec)
	cluster.center(about=(0., 0., 0.))
	cluster_interatomic_distances_initial = get_cluster_interatomic_distances(cluster)
	cluster.set_positions(np.dot(matrix,cluster.get_positions().T).T)
	compared_cluster_interatomic_distances(cluster_interatomic_distances_initial, cluster)
	cluster.center()
	return cluster

# ----------------------------------------------------------------------------------------------------------------------------

sort_cluster_keys = ['id', 'name', 'cluster_energy']

def get_input_int(input_message,default_input):
	if not isinstance(default_input,int):
		print('Error in get_input_int of Coagulate_EnergyProfiles.py')
		print('The default_input must be an int')
		print('default_input: '+str(default_input))
		print('Check this out')
		import pdb; pdb.set_trace()
		exit()
	while True:
		get_input = str(input(str(input_message)+' [Default: '+str(default_input)+']?: '))
		get_input.lower()
		if get_input == '':
			get_input = str(default_input)
		if not get_input.isdigit():
			print('Error. Your input must be an integer.')
		else:
			return int(get_input)

def get_int(given_input):
	given_input = str(given_input)
	given_input.lower()
	if not given_input.isdigit():
		print('Error. Your input must be an integer.')
	else:
		return int(given_input)

def get_input_str(input_message,options,default_input):
	if not isinstance(default_input,str):
		print('Error')
		print('The default_input must be an str')
		print('default_input: '+str(default_input))
		print('Check this out')
		import pdb; pdb.set_trace()
		exit()
	while True:
		to_string = str(input_message)+', [Options: '+', '.join(options)+'], [Default: '+str(default_input)+']?: '
		get_input = str(input(to_string))
		get_input.lower()
		if get_input == '':
			return str(default_input)
		options = [option.lower() for option in options]
		if get_input in options:
			return str(get_input)
		print('Error, you must input one of the following options: '+', '.join(options))
		pritn('Try entering in an option again.')

number_of_sys_argvs = len(sys.argv)

if number_of_sys_argvs == 1:
	number_of_clusters_per_database = get_input_int('How many clusters would you like in each database?',2000)
	sort_clusters_by = get_input_str('What parameter would you like the clusters in the database(s) sorted by?', sort_cluster_keys,'cluster_energy')
elif number_of_sys_argvs == 2:
	number_of_clusters_per_database = get_int(sys.argv[1])
	print('No. of clusters in each database: '+str(number_of_clusters_per_database))
	sort_clusters_by = get_input_str('What parameter would you like the clusters in the database(s) sorted by?',sort_cluster_keys,'cluster_energy')
elif number_of_sys_argvs == 3:
	number_of_clusters_per_database = get_int(sys.argv[1])
	print('No. of clusters in each database: '+str(number_of_clusters_per_database))
	sort_clusters_by = str(sys.argv[2])
	print('Sorting clusters by: '+str(sort_clusters_by))

if not sort_clusters_by in sort_cluster_keys:
	print('Error in Postprocessing_Database.py')
	print('Your input for sort_clusters_by must be one of either: '+str(sort_cluster_keys))
	print('Your input for sort_clusters_by: '+str(sort_clusters_by))
	print('Check this out.')
	exit('This program will finish without completing.')

# ----------------------------------------------------------------------------------------------------------------------------

database_name = 'GA_Recording_Database'
if os.path.exists(database_name+'.db'):
	db = connect(database_name+'.db')
else:
	exit('Error. You need to be inside the Recorded_Data folder than contains the '+str(database_name)+'.db database file.')

for file in os.listdir(os.getcwd()):
	if file.startswith(database_name+'_postprocessed_') and file.endswith('.db'):
		os.remove(file)

clusters_info = []

print('========================================================')
len_db = len(db)
number_of_smaller_databases = ceil(float(len_db)/float(number_of_clusters_per_database))
print('Rough number of smaller databases that will be created: '+str(number_of_smaller_databases))
print('========================================================')
print('Making sure database is all good and all the information required is included in the database.')
print('Number of clusters to check: '+str(len_db))
print('Clusters checked: ')
for row in db.select():
	if not (sort_clusters_by in row._keys):
		print('Error. issue with database for the following cluster')
		print(row)
		exit('Program will finish without completing')
	if row.id%10000 == 0:
		print(row.id)
	clusters_info.append((row.id, row.get(sort_clusters_by)))
print('========================================================')

clusters_info.sort(key=lambda x:x[1])

smaller_database_folder = 'Smaller_Database_folder'
if os.path.exists(smaller_database_folder):
	rmtree(smaller_database_folder)
os.mkdir(smaller_database_folder)
print('========================================================')
print('Making smaller databases where clusters have been ordered by '+str(sort_clusters_by))
print('Rough number of smaller databases that will be created: '+str(number_of_smaller_databases))
counter = 1
database_number = 1
small_database_name = smaller_database_folder+'/'+database_name+'_postprocessed_'+str(database_number)+'.db'
print('Making '+str(small_database_name))
db_smaller = connect(small_database_name)
for cluster_id, cluster_datum in clusters_info:
	if counter == number_of_clusters_per_database+1:
		counter = 1
		database_number += 1
		small_database_name = smaller_database_folder+'/'+database_name+'_postprocessed_'+str(database_number)+'.db'
		print('Making '+str(small_database_name))
		db_smaller = connect(small_database_name)
	row = db.get(id=cluster_id)
	cluster = row.toatoms()
	cluster = rotate_cluster_to_major_inertia_vector(cluster)
	cluster_data = {}
	for key in row._keys:
		cluster_data[key] = row[key]
	db_smaller.write(cluster, key_value_pairs=cluster_data)
	if counter%1 == 0:
		print(counter)
	counter += 1
print('========================================================')
