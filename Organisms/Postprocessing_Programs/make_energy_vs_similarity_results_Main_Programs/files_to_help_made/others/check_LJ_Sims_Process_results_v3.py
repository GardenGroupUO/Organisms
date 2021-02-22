#!/usr/bin/python

import os
import numpy as np
from ase import Atom, Atoms
from ase.io import read, write
from ase.visualize import view
from RunMinimisation_LJ import Minimisation_Function
from T_SCM_Method import get_CNA_profile, get_CNA_similarities
from copy import deepcopy
from collections import Counter

# ---------------------------------------------------------------------------- %
def get_Pop_history(path_to):
	path_to_Population_history = path_to+'/Population/Population_history.txt'
	population_history = []
	with open(path_to_Population_history,'r') as Pop_historyTXT:
		for line in Pop_historyTXT:
			if line.startswith('Clusters in Pool'):
				clusters_in_pop = line.strip().replace('Clusters in Pool:\t','').split('\t')
				clusters_in_pop = [int(cluster.split('(')[0]) for cluster in clusters_in_pop]
				population_history.append(clusters_in_pop)
	return population_history

def get_EnergyProfile(path_to):
	path_to_EnergyProfile = path_to+'/Population/EnergyProfile.txt'
	cluster_history = {}
	restart_gens = []
	with open(path_to_EnergyProfile,'r') as EnergyProfileTXT:
		for line in EnergyProfileTXT:
			if line.startswith('Finished prematurely as LES energy found.'):
				break
			elif line.startswith('Restarting due to epoch.'):
				restart_gens.append(generation)
			else:
				cluster_name, generation, energy = line.rstrip().split('\t')
				cluster_name = int(cluster_name)
				generation = int(generation)
				cluster_history.setdefault(generation,[]).append(cluster_name)
	return cluster_history, restart_gens

# ---------------------------------------------------------------------------- %

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

def get_similarity_value_for_max_and_half(cluster_1_CNA_profile,cluster_2,rCuts):
	#cluster_1_CNA_profile = get_CNA_profile(cluster_1, rCuts)
	cluster_2_CNA_profile = get_CNA_profile(cluster_2, rCuts)
	get_similarity_values = get_CNA_similarities(cluster_1_CNA_profile,cluster_2_CNA_profile)
	return max(get_similarity_values), get_similarity_values[int(len(get_similarity_values)/2)]

def view_cluster(cluster):
	new_cluster = cluster.copy()
	new_cluster.set_cell((10,10,10))
	new_cluster.center()
	view(new_cluster)

# ---------------------------------------------------------------------------- %

def process_data(LJ_data_path,LJ_gm_minTXT,cluster_type):

	LJ_dataTXT = LJ_data_path+'/population_results_'+str(cluster_type)+'.txt'
	databaseDB = LJ_data_path+'/Recorded_Data/GA_Recording_Database.db'

	LJ_gm_cluster = Atoms()
	with open(LJ_gm_minTXT,'r') as LJ_positions:
		for line in LJ_positions:
			xx, yy, zz = line.rstrip().split()
			atom = Atom(symbol='Au', position=(xx, yy, zz))
			LJ_gm_cluster.append(atom)

	LJ_gm_cluster = minmise(LJ_gm_cluster)
	tetrahedral_energy = LJ_gm_cluster.get_potential_energy()
	rCuts = get_rCuts()
	LJ_gm_cluster_CNA_profile = get_CNA_profile(LJ_gm_cluster, rCuts)

	# ---------------------------------------------------------------------------- %
	from ase.db import connect

	db = connect(databaseDB)
	rCuts = get_rCuts()
	data = []
	database = {}

	with open(LJ_dataTXT,'r') as resultsTXT:
		counter = 1
		for line in resultsTXT:
			if counter%100 == 0:
				print(counter)
			datum = eval(line.rstrip())
			data.append(datum)
			name = datum['name']
			database[name] = datum
			counter += 1

	# ---------------------------------------------------------------------------- %

	energies = []
	max_sims = []
	sim_halfs = []
	counter = 0
	for cluster_datum in data:
		if counter%100 == 0:
			print((counter,cluster_datum['id']))
		energies.append(cluster_datum['cluster_energy'])
		max_sims.append(cluster_datum['max_sim'])
		sim_halfs.append(cluster_datum['half_sim'])
		counter += 1

		# ---->

	import matplotlib.pyplot as plt
	import matplotlib.cm as cm
	from Animation import get_energy_limits

	all_max_energy, all_min_energy = get_energy_limits([energies])
	colors = cm.rainbow(np.linspace(1, 0.1, len(energies)))

	plt.scatter(energies,sim_halfs,s=2,color=colors)
	plt.xlabel('Energy (LJ units)')
	plt.xlim(all_max_energy, all_min_energy)
	plt.ylabel('Similarity compared to Leary (%)')
	plt.ylim(-1,101)
	plt.savefig(LJ_data_path+'/energy_vs_sim_'+str(cluster_type)+'.png')
	plt.clf()

	plt.scatter(sim_halfs,energies,s=2,color=colors)
	plt.xlabel('Similarity compared to Leary (%)')
	plt.xlim(-1,101)
	plt.ylabel('Energy (LJ units)')
	plt.ylim(all_max_energy, all_min_energy)
	plt.savefig(LJ_data_path+'/sim_vs_energy_'+str(cluster_type)+'.png')
	plt.clf()

	# ---------------------------------------------------------------------------- %

	def get_collection_data(collection_history,database):
		collection_Per_generation = []
		for col in collection_history:
			collection = []
			for cluster_name in col:
				try:
					datum = database[cluster_name]
				except:
					continue
				collection.append(datum)
			collection_Per_generation.append(collection)
		return collection_Per_generation

	def get_offspring_data(clusters_made_each_geneneration,database):
		generation = 1
		offspring_Per_generation = []
		while generation < len(clusters_made_each_geneneration):
			off = clusters_made_each_geneneration[generation]
			offsprings = []
			for cluster_name in off:
				try:
					datum = database[cluster_name]
				except:
					continue
				offsprings.append(datum)
			offspring_Per_generation.append(offsprings)
			generation += 1
		return offspring_Per_generation

	population_history = get_Pop_history(LJ_data_path)
	clusters_made_each_geneneration, restart_gens = get_EnergyProfile(LJ_data_path)
	clusters_made_each_geneneration[0]
	for restart_gen in sorted(restart_gens,reverse=True):
		del population_history[restart_gen]

	populations_Per_generation = get_collection_data(population_history,database)
	offspring_Per_generation = get_offspring_data(clusters_made_each_geneneration,database)

	import matplotlib.pyplot as plt
	import matplotlib.cm as cm

	all_similarities = []
	all_energies = []
	all_generations = []
	for generation in range(len(populations_Per_generation)):
		print('generation: '+str(generation))
		population_data = populations_Per_generation[generation]
		#import pdb; pdb.set_trace()
		similarities = [cluster['half_sim'] for cluster in population_data]
		energies = [cluster['cluster_energy'] for cluster in population_data]
		generations = [generation for Not_Used in range(len(population_data))]
		if not (len(similarities) == len(energies) == len(generations)):
			print('Error')
			import pdb; pdb.set_trace()
		all_similarities += similarities
		all_energies += energies
		all_generations += generations

	all_max_energy, all_min_energy = get_energy_limits([all_energies])
	colors = cm.rainbow(np.linspace(1, 0.1, all_generations[-1]+1))
	generation_colors = [colors[generation] for generation in all_generations]

	plt.scatter(all_energies,all_similarities,s=1,color=generation_colors)
	plt.xlabel('Energy (LJ units)')
	plt.xlim(all_max_energy, all_min_energy)
	plt.ylabel('Similarity compared to Leary (%)')
	plt.ylim(-1,101)
	plt.savefig(LJ_data_path+'/energy_vs_sim-population_over_generations_'+str(cluster_type)+'.png')
	plt.clf()

	plt.scatter(all_similarities,all_energies,s=1,color=generation_colors)
	plt.xlabel('Similarity compared to Leary (%)')
	plt.xlim(-1,101)
	plt.ylabel('Energy (LJ units)')
	plt.ylim(all_max_energy, all_min_energy)
	plt.savefig(LJ_data_path+'/sim_vs_energy-population_over_generations_'+str(cluster_type)+'.png')
	plt.clf()


	from matplotlib import pyplot
	from mpl_toolkits.mplot3d import Axes3D
	fig = pyplot.figure()
	ax = Axes3D(fig)
	ax.scatter(all_energies,all_similarities,all_generations,s=1,color=generation_colors)
	ax.set_xlabel('Energy (LJ units)')
	plt.xlim(all_max_energy, all_min_energy)
	ax.set_ylabel('Similarity compared to Leary (%)')
	ax.set_ylim(-1,101)
	ax.set_zlabel('Generations')
	pyplot.savefig(LJ_data_path+'/sim_vs_energy_vs_generations-population_over_generations_'+str(cluster_type)+'.png')
	pyplot.clf()


	from Animation import AnimatedScatter
	AnimatedScatter(populations_Per_generation,offspring_Per_generation,LJ_data_path,cluster_type)

# ------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------ #
'''
LJ_data = 'Tesing_Sim_Theory/LJ38_Test/Epoch_D_Energy_F_Energy/Trial'
LJ_gm_minTXT = 'data/LJ38_positions_1.txt'
for trial_no in range(1,101):
	print(LJ_data+str(trial_no))
	process_data(LJ_data+str(trial_no),LJ_gm_minTXT,'LJ38')
'''
# ------------------------------------------------------------------------------------------ #
'''
LJ_data = 'Tesing_Sim_Theory/LJ98_Test/Epoch_D_Energy_F_Energy/Trial'
LJ_gm_minTXT = 'data/LJ98_positions_1.txt'
for trial_no in range(1,11):
	print(LJ_data+str(trial_no))
	process_data(LJ_data+str(trial_no),LJ_gm_minTXT,'LJ98')
'''
# ------------------------------------------------------------------------------------------ #






