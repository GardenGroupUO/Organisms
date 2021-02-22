#!/usr/bin/python

import os, sys
import numpy as np
from ase import Atom, Atoms
from ase.io import read, write
from ase.visualize import view
from RunMinimisation_LJ import Minimisation_Function
from T_SCM_Method import get_CNA_profile, get_CNA_similarities
from copy import deepcopy

def minmise(cluster):
	cluster.set_cell((1000,1000,1000))
	cluster.center()
	cluster = Minimisation_Function(cluster)
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

def get_data(LJ_data,LJ_gm_minTXT,cluster_type):

	LJ_dataTXT = LJ_data+'/population_results_'+str(cluster_type)+'.txt'
	databaseDB = LJ_data+'/Recorded_Data/GA_Recording_Database.db'

	LJ_gm_cluster = Atoms()
	with open(LJ_gm_minTXT,'r') as LJ_positions:
		for line in LJ_positions:
			xx, yy, zz = line.rstrip().split()
			atom = Atom(symbol='Au', position=(xx, yy, zz))
			LJ_gm_cluster.append(atom)

	LJ_gm_cluster = minmise(LJ_gm_cluster)
	rCuts = get_rCuts()
	LJ_gm_cluster_CNA_profile = get_CNA_profile(LJ_gm_cluster, rCuts)

	# ---------------------------------------------------------------------------- %
	from ase.db import connect
	db = connect(databaseDB)
	rCuts = get_rCuts()

	resultsTXT = open(LJ_dataTXT,'w')
	for row in db.select():
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
		#datum['cluster'] = cluster
		datum['name'] = row['name']
		datum['gen_made'] = row['gen_made']
		datum['cluster_energy'] = row['cluster_energy']
		datum['id'] = row['id']
		print(datum['id'])

		CNA_profile = get_CNA_profile(cluster, rCuts)
		datum['CNA_profile'] = CNA_profile
		max_sim, half_sim = get_similarity_value_for_max_and_half(LJ_gm_cluster_CNA_profile,CNA_profile,rCuts)
		datum['max_sim'] = max_sim
		datum['half_sim'] = half_sim

		resultsTXT.write(str(datum)+'\n')

	resultsTXT.close()

# ------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------ #
'''
LJ_data = 'Tesing_Sim_Theory/LJ38_Test/Epoch_D_Energy_F_Energy/Trial'
LJ_gm_minTXT = 'data/LJ38_positions_1.txt'
cluster = 'LJ38'
for trial_no in range(1,101):
	print(LJ_data+str(trial_no))
	get_data(LJ_data+str(trial_no),LJ_gm_minTXT,cluster)

# ------------------------------------------------------------------------------------------ #

LJ_data = 'Tesing_Sim_Theory/LJ98_Test/Epoch_D_Energy_F_Energy/Trial'
LJ_gm_minTXT = 'data/LJ98_positions_1.txt'
cluster = 'LJ98'
for trial_no in range(1,11):
	print(LJ_data+str(trial_no))
	get_data(LJ_data+str(trial_no),LJ_gm_minTXT,cluster)

# ------------------------------------------------------------------------------------------ #
'''

#LJ_data = 'Tesing_Sim_Theory/LJ38_Test/Epoch_D_Energy_F_Energy/Trial'
#LJ_gm_minTXT = 'data/LJ38_positions_1.txt'
#cluster = 'LJ38'

LJ_data = sys.argv[1]
LJ_gm_minTXT = sys.argv[2]
cluster = sys.argv[3]
trial_no = sys.argv[4]
get_data(LJ_data+str(trial_no),LJ_gm_minTXT,cluster)









