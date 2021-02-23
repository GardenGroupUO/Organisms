import os, sys, io
import numpy as np
from ase import Atom, Atoms
from ase.io import read, write
from ase.visualize import view
from Check_LJ_Sims_Programs.RunMinimisation import Minimisation_Function
from Check_LJ_Sims_Programs.T_SCM_Method import get_CNA_profile, get_CNA_similarities
from copy import deepcopy
from shutil import rmtree

def minimise(cluster,calculator):
	cluster.set_cell((1000,1000,1000))
	cluster.center()
	cluster = Minimisation_Function(cluster,calculator)
	#cluster.set_cell((10,10,10))
	#cluster.center()
	return cluster

def get_rCuts():
	first_nn = 1.0; second_nn = round(first_nn*(2.0**0.5),4)
	diff = second_nn - first_nn
	rCut_low = first_nn + (1.0/3.0)*diff
	rCut_high = first_nn + (2.0/3.0)*diff
	rCuts = np.linspace(rCut_low,rCut_high,78,endpoint=True)
	for index in range(len(rCuts)):
		rCuts[index] = round(rCuts[index],4)
	return rCuts

def get_similarity_value_for_max_and_half(cluster_1_CNA_profile,cluster_2_CNA_profile,rCuts):
	#cluster_1_CNA_profile = get_CNA_profile(cluster_1, rCuts)
	#cluster_2_CNA_profile = get_CNA_profile(cluster_2, rCuts)
	get_similarity_values = get_CNA_similarities(cluster_1_CNA_profile,cluster_2_CNA_profile)
	return max(get_similarity_values), get_similarity_values[int(len(get_similarity_values)/2)]

def view_cluster(cluster):
	new_cluster = cluster.copy()
	new_cluster.set_cell((10,10,10))
	new_cluster.center()
	view(new_cluster)

# ---------------------------------------------------------------------------- %

def get_data(data_path,gm_min_XYZ,cluster_type,calculator,rCuts,energy_of_global_minimum,energy_decimal_places):

	compared_cluster_name = gm_min_XYZ.split('.')[0].split('/')[-1]
	folder_name = 'Similarity_Investigation_Data'+'/'+compared_cluster_name
	LJ_dataTXT = data_path+'/'+folder_name+'/population_results_'+str(cluster_type)+'.txt'
	databaseDB = data_path+'/Recorded_Data/GA_Recording_Database.db'

	if os.path.exists(LJ_dataTXT):
		print('Have already got data.')
		return

	if os.path.exists(data_path+'/'+folder_name):
		os.rename(data_path+'/'+folder_name,data_path+'/'+folder_name+'-'+'to_delete')
		rmtree(data_path+'/'+folder_name+'-'+'to_delete')
	os.makedirs(data_path+'/'+folder_name)

	LJ_gm_cluster = read(gm_min_XYZ)
	LJ_gm_cluster = minimise(LJ_gm_cluster,calculator)
	#rCuts = get_rCuts()
	LJ_gm_cluster_CNA_profile = get_CNA_profile(LJ_gm_cluster, rCuts)

	# ---------------------------------------------------------------------------- %
	from ase.db import connect
	db = connect(databaseDB)
	no_of_rows = db.count()
	del db
	#rCuts = get_rCuts()

	# preprocessing
	finishing_generation = float('inf')
	indices_to_sample = []
	print('--------------------------------')
	print('Preprocessing work')
	print('No of clusters: '+str(no_of_rows))
	generation = 0
	with open(LJ_dataTXT,'w') as resultsTXT:
		for index in range(no_of_rows):
			with connect(databaseDB) as db:
				if index%500 == 0:
					print(index)
				row = db.get(id=index+1)
				name = row['name']
				cluster_energy = round(row['cluster_energy'],energy_decimal_places)
				gen_made = row['gen_made']
				if cluster_energy == energy_of_global_minimum:
					if gen_made < finishing_generation:
						finishing_generation = gen_made
				if gen_made == 0:
					gen_made = generation
				else:
					generation = gen_made
				indices_to_sample.append((index,name,gen_made))
	indices_to_sample.sort(key=lambda x:x[1])
	if indices_to_sample[-1][2] < finishing_generation:
		pass
	else:
		for index in range(len(indices_to_sample)-1,-1,-1):
			if indices_to_sample[index][2] > finishing_generation:
				del indices_to_sample[index]
			else:
				break
	print('Stopping at Gen:'+str(indices_to_sample[-1][2])+'\tCluster no: '+str(indices_to_sample[-1][1]))
	print('Getting data and writing it to disk')
	with open(LJ_dataTXT,'w') as resultsTXT:
		with connect(databaseDB) as db:
			for index in range(len(indices_to_sample)):
				#if index%500 == 0:
				#	print(index)
				row = db.get(id=indices_to_sample[index][0]+1)
				numbers = row['numbers']
				positions = row['positions']
				cell = (1000,1000,1000)
				pbc = row['pbc']
				cluster = Atoms()
				for index in range(len(numbers)):
					cluster.append(Atom('Ne', position=list(positions[index]))) # numbers[index]
				cluster.set_cell(cell)
				cluster.center()
				#cluster = minmise(cluster)

				datum = {}
				datum['name'] = row['name']
				datum['gen_made'] = row['gen_made']
				datum['cluster_energy'] = row['cluster_energy']
				datum['id'] = row['id']
				print(datum['id'])

				CNA_profile = get_CNA_profile(cluster, rCuts)
				datum['CNA_profile'] = CNA_profile
				max_sim, half_sim = get_similarity_value_for_max_and_half(LJ_gm_cluster_CNA_profile,CNA_profile,rCuts)
				break
				datum['max_sim'] = max_sim
				datum['half_sim'] = half_sim

				resultsTXT.write(str(datum)+'\n')
	print('Obtained data')
	print('--------------------------------')




