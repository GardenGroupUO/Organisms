import os
import shutil
import numpy as np
from ase import Atom, Atoms
from ase.io import read, write
from ase.visualize import view
from make_energy_vs_similarity_results_Main_Programs.T_SCM_Method import get_CNA_profile, get_CNA_similarities
from copy import deepcopy
from collections import Counter
import matplotlib as mpl
import matplotlib.pyplot as plt


######################################################################################################
######################################################################################################

def process_data(LJ_data_path,compared_cluster_name,LJ_gm_minTXT,cluster_type,restarts):
	print('Processing Data')

	compared_cluster_name = LJ_gm_minTXT.split('.')[0].split('/')[-1]
	folder_name = 'Similarity_Investigation_Data'+'/'+compared_cluster_name

	if not os.path.exists(LJ_data_path+'/'+folder_name):
		exit('Error')

	LJ_dataTXT = LJ_data_path+'/'+str(folder_name)+'/population_results_'+str(cluster_type)+'.txt'
	databaseDB = LJ_data_path+'/'+str(folder_name)+'/Recorded_Data/GA_Recording_Database.db'

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

	original_population_history = get_Pop_history(LJ_data_path, give_full_info=True)
	clusters_made_each_geneneration, restart_gens = get_EnergyProfile(LJ_data_path)
	#clusters_made_each_geneneration[0]
	population_history = deepcopy(original_population_history)

	for restart_gen in sorted(restart_gens,reverse=True):
		del population_history[restart_gen]

	runs = []
	between_restart_gens = [0] + restart_gens + [len(population_history)]
	for index in range(len(between_restart_gens)-1):
		starting_gen = between_restart_gens[index]
		ending_gen   = between_restart_gens[index+1]
		runs.append([x[1] for x in population_history[starting_gen:ending_gen]])

	clusters_to_record_full = []
	for run in runs:
		clusters_to_record_full.append((min(run[0]), max(run[-1])))

	clusters_to_record = []
	for restart in restarts:
		clusters_to_record.append(clusters_to_record_full[restart-1])
	import pdb; pdb.set_trace()

	# ---------------------------------------------------------------------------- %


	folder_name = 'Similarity_Investigation_Data'+'/'+compared_cluster_name
	LJ_dataTXT = LJ_data_path+'/'+str(folder_name)+'/population_results_'+str(cluster_type)+'.txt'
	counter = 0
	clusters_similarity = {}

	def cluster_in(name,clusters_to_record):
		for starting_cluster_no, ending_cluster_no in clusters_to_record:
			if starting_cluster_no <= name <= ending_cluster_no+500:
				return True
		else:
			return False
	
	rCuts = get_rCuts()
	data = []
	database = {}

	min_energy = float('inf')
	max_energy = -float('inf')

	with open(LJ_dataTXT,'r') as resultsTXT:
		counter = 1
		for line in resultsTXT:
			if counter%500 == 0:
				print(counter)
			if cluster_in(counter,clusters_to_record):
				datum = eval(line.rstrip())
				name = datum['name']
				if not name == counter:
					exit('Error')
				cluster_2_CNA_profile = datum['CNA_profile']
				half_sigma = get_similarity_value_for_half(LJ_gm_cluster_CNA_profile,cluster_2_CNA_profile)
				clusters_similarity[name] = half_sigma
				del datum['CNA_profile']
				database[name] = datum
				energy = datum['cluster_energy']
				if energy < min_energy:
					min_energy = energy
				if energy > max_energy:
					max_energy = energy
				#import pdb; pdb.set_trace()
				#data.append(datum)
				#database[name] = datum['CNA_profile']
			counter += 1
			# Debugging issue
			#if counter == 250000:
			#	break

	# ---------------------------------------------------------------------------- %

	import matplotlib.pyplot as plt
	import matplotlib.cm as cm

	#all_max_energy, all_min_energy = get_energy_limits([energies])
	#colors = cm.rainbow(np.linspace(1, 0.1, len(energies)))

	# ---------------------------------------------------------------------------- %

	def get_collection_data(collection_history,database):
		collection_Per_generation = []
		for gen, col in collection_history:
			collection = []
			for cluster_name in col:
				try:
					datum = database[cluster_name]
				except:
					continue
				collection.append(datum)
			collection_Per_generation.append((gen,collection))
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

	# ---------------------------------------------------------------------------- %

	populations_Per_generation = get_collection_data(population_history,database)
	for index in range(len(populations_Per_generation)):
		gen, population = populations_Per_generation[index]
		populations_Per_generation[index] = population
	offspring_Per_generation = get_offspring_data(clusters_made_each_geneneration,database)

	import matplotlib.pyplot as plt
	import matplotlib.cm as cm

	# ---------------------------------------------------------------------------- %

	between_restart_gens = restart_gens + [len(population_history)]

	new_restarting_gens = []
	starting_gen = 0
	for index in range(len(between_restart_gens)):
		number = between_restart_gens[index]
		ending_gen = number+index
		new_restarting_gens.append((starting_gen,ending_gen))
		starting_gen = number+index+1

	runs = []
	for starting_gen, ending_gen in new_restarting_gens:
		runs.append(population_history[starting_gen:ending_gen+1])

	runs_to_plot = []
	for restart in restarts:
		runs_to_plot.append(runs[restart-1])

	for index in range(len(runs_to_plot)):
		for index_2 in range(len(runs_to_plot[index])):
			runs_to_plot[index][index_2] = runs_to_plot[index][index_2][1]

	clusters_to_record = []
	for run_to_plot in runs_to_plot:
		clusters_to_record.append((min(run_to_plot[0]),max(run_to_plot[-1])))

	# -------------------------------------------------------------------------------- #

	record_data = []
	for record_datum in runs_to_plot:
		record_data.append([])
		for population in record_datum:
			record_data[-1].append([])
			for cluster in population:
				#cluster_no, gen_no, energy = cluster
				cluster_no = cluster
				cluster_energy = database[cluster_no]['cluster_energy']
				cluster_similarity = clusters_similarity[cluster_no]
				#cluster = tuple(cluster_no, gen_no, energy, cluster_similarity)
				cluster = (cluster_energy, cluster_similarity)
				record_data[-1][-1].append(cluster)

	#return record_data, clusters_similarity
	return record_data, min_energy, max_energy

######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################

all_record_data = []

restarts = [7]#,23,42]
record_data, min_energy_1, max_energy_1 = process_data('Energy/Trial17','LJ98_positions_1','energy_data/LJ98_positions_1.txt','LJ98',restarts)
all_record_data.append(record_data)
#restarts = [28,51,85]
#record_data, min_energy_2, max_energy_2 = process_data('Structure_plus_Energy/Trial9','LJ98_positions_1','energy_data/LJ98_positions_1.txt','LJ98',restarts)

all_max_energy, all_min_energy = get_energy_limits([[min_energy_1, max_energy_1]])
#all_max_energy, all_min_energy = get_energy_limits([min_energy_1, min_energy_2, max_energy_1, max_energy_2])

import matplotlib.cm as cm
data = []
for record_datum in record_data:
	all_colors = cm.rainbow(np.linspace(1, 0.1, len(record_datum)))
	colors = []
	energies = []
	similarities = []
	for index in range(len(record_datum)):
		population = record_datum[index]
		color = all_colors[index]
		for cluster in population:
			energy, cluster_similarity = cluster
			colors.append(color)
			energies.append(energy)
			similarities.append(cluster_similarity)
	data.append((energies,similarities,colors))

import matplotlib.pyplot as plt
fig, axs = plt.subplots(2, 3, sharex=True, sharey=True, gridspec_kw={'hspace': 0.1, 'wspace': 0.1}, figsize=(9,6), dpi=300)

column = 0
row = 0
plot_name = ['(a)','(b)','(c)','(d)','(e)','(f)']
for energies, similarities, colors in data:
	axs[row, column].scatter(similarities, energies,s=1,color=colors)
	axs[row, column].set_ylim(all_min_energy, all_max_energy)
	axs[row, column].set_xlim(-1,101)
	axs[row, column].tick_params(axis="x", direction="in")
	axs[row, column].tick_params(axis="y", direction="in")
	axs[row, column].tick_params(right=True, top=True)
	axs[row, column].text(0.2, 0.8, plot_name[row*3+column], fontsize=12, horizontalalignment='center', verticalalignment='center')
	column += 1
	if column == 3:
		row += 1
		column = 0

fig.text(0.5, 0.04, 'Similarity compared to Leary (%)', ha='center', va='center')
fig.text(0.06, 0.5, 'Energy (LJ units)', ha='center', va='center', rotation='vertical')
	
fig.tight_layout()
plt.savefig('./sim_vs_energy_LJ98_full.png')
plt.clf()













