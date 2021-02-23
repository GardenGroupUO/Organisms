# This was check_LJ_Sims_Process_results_v4.py

import os
import shutil
import numpy as np
from ase import Atom, Atoms
from ase.io import read, write
from ase.visualize import view
from Check_LJ_Sims_Programs.RunMinimisation import Minimisation_Function
from Check_LJ_Sims_Programs.T_SCM_Method import get_CNA_profile, get_CNA_similarities
from copy import deepcopy
from collections import Counter
import matplotlib as mpl
import matplotlib.pyplot as plt
#print(mpl.get_backend())
plt.switch_backend('Agg')

# ---------------------------------------------------------------------------- %
def get_Pop_history(path_to, give_full_info=False, last_gen_to_record=-1):
	path_to_Population_history = path_to+'/Population/Population_history.txt'
	population_history = []
	with open(path_to_Population_history,'r') as Pop_historyTXT:
		for line in Pop_historyTXT:
			if line.startswith('GA Iteration:'):
				generation = int(line.rstrip().replace('GA Iteration: ',''))
				if generation > last_gen_to_record:
					break
			elif line.startswith('Clusters in Pool'):
				clusters_in_pop = line.strip().replace('Clusters in Pool:\t','').split('\t')
				clusters_in_pop = [int(cluster.split('(')[0]) for cluster in clusters_in_pop]
				if give_full_info:
					population_history.append((generation,clusters_in_pop))
				else:
					population_history.append(clusters_in_pop)
	return population_history

def get_EnergyProfile(path_to, last_gen_to_record=-1):
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
				if generation > last_gen_to_record:
					break
				cluster_history.setdefault(generation,[]).append(cluster_name)
	return cluster_history, restart_gens

# ---------------------------------------------------------------------------- %

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
# energy_per_similarity_for_each_epoch

def get_plots_for_each_epoch(populations_Per_generation, restart_gens, path, folder_name):
	'''
	print('-------------------------------------------------------------------')
	print('Making population plots per epoch')
	restart_gens = []
	with open(path+'/Population/EnergyProfile.txt') as EnergyProfileTXT:
		for line in EnergyProfileTXT:
			if 'Restarting due to epoch.' in line:
				restart_gens.append(generation_no)
				continue
			if 'Finished prematurely as LES energy found.' in line:
				break
			cluster_no, generation_no, energy = line.rstrip().split()
			generation_no = int(generation_no)
	'''

	data_plots = []
	populations_over_an_epoch = []
	generation = 0
	#found_epoch = False
	print('Epoch occurs at: '+str(restart_gens))
	#restart_gens = [restart_gens[index]-1 for index in range(len(restart_gens))]

	max_energy = -float('inf')
	min_energy = float('inf')
	for population in populations_Per_generation:
		data_population = []
		for cluster in population:
			cluster_energy = cluster['cluster_energy']
			max_sim = cluster['max_sim']
			data_population.append((cluster_energy, max_sim))
			if cluster_energy > max_energy:
				max_energy = cluster_energy
			if cluster_energy < min_energy:
				min_energy = cluster_energy
		data_population = tuple(data_population)
		populations_over_an_epoch.append(data_population)
		if (generation+1 in restart_gens): # and (not found_epoch):
			data_plots.append(list(populations_over_an_epoch))
			populations_over_an_epoch = []
		generation += 1
	data_plots.append(list(populations_over_an_epoch))
	for index in range(1,len(data_plots)-1):
		del data_plots[index][-1]
	print('There are '+str(len(data_plots))+' Population optimisations')

	max_no_of_plots_width = 3
	max_no_of_plots_length = 4

	import matplotlib.cm as cm
	from math import floor, ceil
	import matplotlib.pyplot as plt

	energy_diff = max_energy - min_energy
	energy_point = min_energy + (95.0/102.0)*energy_diff
	new_energy_diff = energy_diff*(102.0/100.0)
	new_energy_diff = (new_energy_diff - energy_diff)/2.0
	max_energy = max_energy + new_energy_diff
	min_energy = min_energy - new_energy_diff

	print(max_energy)
	print(min_energy)
	print(energy_diff)
	print(energy_point)

	def making_plots(data_plots, Per_epoch_folder_path, reverse=False):
		if os.path.exists(Per_epoch_folder_path):
			shutil.rmtree(Per_epoch_folder_path)
		os.makedirs(Per_epoch_folder_path)
		plotting_direction = 'forward' if not reverse else 'reversed'
		pages = 0
		plots_length_no = 0
		plots_width_no = 0
		#for data_plot_counter in range(len(data_plots)):
		#	populations = data_plots[data_plot_counter]
		data_plot_counter = 1
		for populations in data_plots:
			if plots_width_no == 0 and plots_length_no == 0:
				no_of_plots_length = float(len(data_plots) - pages*max_no_of_plots_width*max_no_of_plots_length)/float(max_no_of_plots_width)
				no_of_plots_length = int(floor(no_of_plots_length) + ceil(no_of_plots_length%1))
				no_of_plots_length = max_no_of_plots_length if no_of_plots_length > max_no_of_plots_length else no_of_plots_length
				print((no_of_plots_length, max_no_of_plots_width))
				gs_kw = dict(width_ratios=[1]*max_no_of_plots_width, height_ratios=[1]*no_of_plots_length)
				size = 4.0
				fig, axs = plt.subplots(no_of_plots_length, max_no_of_plots_width, constrained_layout=True, gridspec_kw=gs_kw, figsize=(max_no_of_plots_width*size, no_of_plots_length*size))
			#colors = cm.viridis(np.linspace(1, 0, len(populations)))
			colors = cm.rainbow(np.linspace(0.9, 0.1, len(populations)))
			energies = []
			similarities = []
			colors_for_scatterplot = []
			for index_pops in range(len(populations)):
				population = populations[index_pops]
				for energy, similarity in population:
					energies.append(energy)
					similarities.append(similarity)
					colors_for_scatterplot.append(colors[index_pops])

			if reverse:
				similarities = similarities[::-1]
				energies = energies[::-1]
				colors_for_scatterplot = colors_for_scatterplot[::-1]

			if no_of_plots_length > 1:
				print(plots_length_no, plots_width_no)
				axs[plots_length_no, plots_width_no].scatter(similarities, energies, c=colors_for_scatterplot, s=1)
				axs[plots_length_no, plots_width_no].set_ylim((min_energy, max_energy))
				axs[plots_length_no, plots_width_no].set_xlim((-1,101))
				axs[plots_length_no, plots_width_no].set_aspect(1.0*abs(101.0--1.0)/abs(float(max_energy) - float(min_energy)))
				axs[plots_length_no, plots_width_no].text(6.0, energy_point, 'Epoch '+str(data_plot_counter) , fontsize=16)
				if plots_width_no == 0:
					axs[plots_length_no, plots_width_no].set_ylabel('Energy (eV)')
				else:
					axs[plots_length_no, plots_width_no].set_yticklabels(['']*len(axs[plots_length_no, plots_width_no].get_yticklabels()))
				if plots_length_no+1 == no_of_plots_length:
					axs[plots_length_no, plots_width_no].set_xlabel('Similarity (%)')
				else:
					axs[plots_length_no, plots_width_no].set_xticklabels(['']*len(axs[plots_length_no, plots_width_no].get_xticklabels()))
			else:
				print(plots_width_no)
				axs[plots_width_no].scatter(similarities, energies, c=colors_for_scatterplot, s=1)
				axs[plots_width_no].set_ylim((min_energy, max_energy))
				axs[plots_width_no].set_xlim((-1,101))
				axs[plots_width_no].set_aspect(1.0*abs(101.0--1.0)/abs(float(max_energy) - float(min_energy)))
				axs[plots_width_no].text(6.0, energy_point, 'Epoch '+str(data_plot_counter) , fontsize=16)
				if plots_width_no == 0:
					axs[plots_width_no].set_ylabel('Energy (eV)')
				else:
					axs[plots_width_no].set_yticklabels(['']*len(axs[plots_width_no].get_yticklabels()))
				if plots_length_no+1 == no_of_plots_length:
					axs[plots_width_no].set_xlabel('Similarity (%)')
				else:
					axs[plots_width_no].set_xticklabels(['']*len(axs[plots_width_no].get_xticklabels()))

			plots_width_no += 1
			if plots_width_no == max_no_of_plots_width:
				plots_width_no = 0
				plots_length_no += 1
				if plots_length_no == max_no_of_plots_length:
					plots_length_no = 0
					pages += 1
					#fig.tight_layout()
					fig.savefig(Per_epoch_folder_path+'/Energy_vs_Similarity_for_each_epoch_'+plotting_direction+'_page_'+str(pages)+'.png', dpi=300)
					fig.savefig(Per_epoch_folder_path+'/Energy_vs_Similarity_for_each_epoch_'+plotting_direction+'_page_'+str(pages)+'.svg', dpi=300)
			data_plot_counter += 1

		plots_width_no_end = plots_width_no
		if not plots_width_no_end == 0:
			for plots_width_no in range(plots_width_no_end, max_no_of_plots_width):
				if no_of_plots_length > 1:
					print(plots_length_no, plots_width_no)
					axs[plots_length_no, plots_width_no].scatter([], [])
					axs[plots_length_no, plots_width_no].set_ylim((min_energy, max_energy))
					axs[plots_length_no, plots_width_no].set_xlim((-1,101))
					axs[plots_length_no, plots_width_no].set_aspect(1.0*abs(101.0--1.0)/abs(float(max_energy) - float(min_energy)))
					if plots_width_no == 0:
						axs[plots_length_no, plots_width_no].set_ylabel('Energy (eV)')
					else:
						axs[plots_length_no, plots_width_no].set_yticklabels(['']*len(axs[plots_length_no, plots_width_no].get_yticklabels()))
					if plots_length_no+1 == no_of_plots_length:
						axs[plots_length_no, plots_width_no].set_xlabel('Similarity (%)')
					else:
						axs[plots_length_no, plots_width_no].set_xticklabels(['']*len(axs[plots_length_no, plots_width_no].get_xticklabels()))
				else:
					print(plots_width_no)
					axs[plots_width_no].scatter([], [])
					axs[plots_width_no].set_ylim((min_energy, max_energy))
					axs[plots_width_no].set_xlim((-1,101))
					axs[plots_width_no].set_aspect(1.0*abs(101.0--1.0)/abs(float(max_energy) - float(min_energy)))
					if plots_width_no == 0:
						axs[plots_width_no].set_ylabel('Energy (eV)')
					else:
						axs[plots_width_no].set_yticklabels(['']*len(axs[plots_width_no].get_yticklabels()))
					if plots_length_no+1 == no_of_plots_length:
						axs[plots_width_no].set_xlabel('Similarity (%)')
					else:
						axs[plots_width_no].set_xticklabels(['']*len(axs[plots_width_no].get_xticklabels()))
		pages += 1
		#import pdb; pdb.set_trace()
		#ax.set_box_aspect(1)
		#fig.tight_layout()
		fig.savefig(Per_epoch_folder_path+'/Energy_vs_Similarity_for_each_epoch_'+plotting_direction+'_page_'+str(pages)+'.png', dpi=300)
		fig.savefig(Per_epoch_folder_path+'/Energy_vs_Similarity_for_each_epoch_'+plotting_direction+'_page_'+str(pages)+'.svg', dpi=300)
		print('Making population plots per epoch')
		print('-------------------------------------------------------------------')

	def make_individual_plots(data_plots, Per_epoch_folder_path_individual, reverse=False, save_data=False):
		if os.path.exists(Per_epoch_folder_path_individual):
			shutil.rmtree(Per_epoch_folder_path_individual)
		os.makedirs(Per_epoch_folder_path_individual)
		print('-------------------------------------------------------------------')
		print('Making Individual Plots')
		plotting_direction = 'forward' if not reverse else 'reversed'
		pages = 0
		plots_length_no = 0
		plots_width_no = 0
		#for data_plot_counter in range(len(data_plots)):
		#	populations = data_plots[data_plot_counter]
		data_plot_counter = 1
		for epoch_no in range(len(data_plots)):
			print('Making plot for epoch '+str(epoch_no+1))
			populations = data_plots[epoch_no]
			#colors = cm.viridis(np.linspace(1, 0, len(populations)))
			colors = cm.rainbow(np.linspace(0.9, 0.1, len(populations)))
			energies = []
			similarities = []
			colors_for_scatterplot = []
			for index_pops in range(len(populations)):
				population = populations[index_pops]
				for energy, similarity in population:
					energies.append(energy)
					similarities.append(similarity)
					colors_for_scatterplot.append(colors[index_pops])

			if reverse:
				similarities = similarities[::-1]
				energies = energies[::-1]
				colors_for_scatterplot = colors_for_scatterplot[::-1]

			fig = plt.figure(figsize=(4.0,4.0), dpi=300)
			plt.scatter(similarities, energies, c=colors_for_scatterplot, s=1)
			plt.ylim((min_energy, max_energy))
			plt.xlim((-1,101))
			plt.gca().set_aspect(1.0*abs(101.0--1.0)/abs(float(max_energy) - float(min_energy)), adjustable='box')
			#plt.text(6.0, energy_point, 'Epoch '+str(data_plot_counter) , fontsize=16)
			plt.ylabel('Energy (eV)')
			plt.xlabel('Similarity (%)')
			plt.tight_layout()
			plt.savefig(Per_epoch_folder_path_individual+'/Energy_vs_Similarity_per_individual_epoch_'+str(plotting_direction)+'_Epoch_'+str(epoch_no+1)+'.png')
			plt.savefig(Per_epoch_folder_path_individual+'/Energy_vs_Similarity_per_individual_epoch_'+str(plotting_direction)+'_Epoch_'+str(epoch_no+1)+'.svg')
			plt.cla(); plt.clf(); plt.close()

			if save_data:
				with open(Per_epoch_folder_path_individual+'/Energy_vs_Similarity_per_individual_epoch_'+str(plotting_direction)+'_Epoch_'+str(epoch_no+1)+'.txt','w') as DataTXT:
					DataTXT.write(str(similarities)+'\n')
					DataTXT.write(str(energies)+'\n')
					DataTXT.write(str(colors_for_scatterplot)+'\n')
		print('Finished making individual energy vs. similarity plots.')
		print('-------------------------------------------------------------------')

	#def make_individual_data(data_plots, Per_epoch_folder_path_individual):
	#	with open() as dataTXT:
	#		pass

	#import pdb; pdb.set_trace()
	Per_epoch_folder_path = path+'/'+folder_name+'/'+'energy_per_similarity_for_each_epoch'
	making_plots(data_plots, Per_epoch_folder_path, reverse=False)

	Per_epoch_folder_path = path+'/'+folder_name+'/'+'energy_per_similarity_for_each_epoch_reversed'
	making_plots(data_plots, Per_epoch_folder_path, reverse=True)

	Per_epoch_folder_path_individual = path+'/'+folder_name+'/'+'energy_per_similarity_for_each_epoch_individual_plots'
	make_individual_plots(data_plots, Per_epoch_folder_path_individual, reverse=False, save_data=True)

	Per_epoch_folder_path_individual = path+'/'+folder_name+'/'+'energy_per_similarity_for_each_epoch_individual_plots_reversed'
	make_individual_plots(data_plots, Per_epoch_folder_path_individual, reverse=True)
			
# ---------------------------------------------------------------------------- %

def process_data(data_path,gm_min_XYZ,cluster_type,calculator,rCuts,energy_of_global_minimum,energy_decimal_places):

	print('Processing Data')
	#original_population_history = get_Pop_history(data_path, give_full_info=True)
	#clusters_made_each_geneneration, restart_gens = get_EnergyProfile(data_path)
	#import pdb; pdb.set_trace()

	compared_cluster_name = gm_min_XYZ.split('.')[0].split('/')[-1]
	folder_name = 'Similarity_Investigation_Data'+'/'+compared_cluster_name

	if not os.path.exists(data_path+'/'+folder_name):
		exit('Error')

	LJ_dataTXT = data_path+'/'+str(folder_name)+'/population_results_'+str(cluster_type)+'.txt'
	databaseDB = data_path+'/'+str(folder_name)+'/Recorded_Data/GA_Recording_Database.db'

	LJ_gm_cluster = read(gm_min_XYZ)
	LJ_gm_cluster = minimise(LJ_gm_cluster,calculator)
	tetrahedral_energy = LJ_gm_cluster.get_potential_energy()
	#rCuts = get_rCuts()
	LJ_gm_cluster_CNA_profile = get_CNA_profile(LJ_gm_cluster, rCuts)

	# ---------------------------------------------------------------------------- %
	#from ase.db import connect

	#db = connect(databaseDB)
	#rCuts = get_rCuts()
	data = []
	database = {}

	finishing_generation = float('inf')
	with open(LJ_dataTXT,'r') as resultsTXT:
		counter = 1
		for line in resultsTXT:
			if counter%500 == 0:
				print(counter)
			datum = eval(line.rstrip())
			if round(datum['cluster_energy'],energy_decimal_places) == energy_of_global_minimum:
				finishing_generation = datum['gen_made']
			if datum['gen_made'] > finishing_generation:
				continue
			data.append(datum)
			name = datum['name']
			#import pdb; pdb.set_trace()
			del datum['CNA_profile']
			database[name] = datum
			counter += 1

			# Debugging issue
			#if counter == 25000:
			#	break
	final_gen = data[-1]['gen_made']

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
	#from Check_LJ_Sims_Programs.Animation import get_energy_limits
	from Check_LJ_Sims_Programs.get_energy_limits import get_energy_limits

	all_max_energy, all_min_energy = get_energy_limits([energies])
	#import pdb; pdb.set_trace()
	colors = cm.rainbow(np.linspace(1, 0.1, len(energies)))

	plt.scatter(energies,sim_halfs,s=2,color=colors)
	plt.xlabel('Energy (LJ units)')
	plt.xlim(all_min_energy, all_max_energy)
	plt.ylabel('Similarity (%)')
	plt.ylim(-1,101)
	plt.savefig(data_path+'/'+str(folder_name)+'/sim_vs_energy_'+str(cluster_type)+'.png')
	plt.clf()

	plt.scatter(sim_halfs,energies,s=2,color=colors)
	plt.xlabel('Similarity (%)')
	plt.xlim(-1,101)
	plt.ylabel('Energy (LJ units)')
	plt.ylim(all_min_energy, all_max_energy)
	plt.savefig(data_path+'/'+str(folder_name)+'/energy_vs_sim_'+str(cluster_type)+'.png')
	plt.clf()

	# ---------------------------------------------------------------------------- %
	'''
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
	'''
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

	original_population_history = get_Pop_history(data_path, give_full_info=True, last_gen_to_record=final_gen)
	clusters_made_each_geneneration, restart_gens = get_EnergyProfile(data_path, last_gen_to_record=final_gen)
	#clusters_made_each_geneneration[0]
	population_history = deepcopy(original_population_history)

	for restart_gen in sorted(restart_gens,reverse=True):
		del population_history[restart_gen]

	populations_Per_generation = get_collection_data(population_history,database)
	for index in range(len(populations_Per_generation)):
		gen, population = populations_Per_generation[index]
		populations_Per_generation[index] = population
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
		#populations_Per_generation[generation] = []

	all_max_energy, all_min_energy = get_energy_limits([all_energies])
	colors = cm.rainbow(np.linspace(1, 0.1, all_generations[-1]+1))
	generation_colors = [colors[generation] for generation in all_generations]

	plt.scatter(all_energies,all_similarities,s=1,color=generation_colors)
	plt.xlabel('Energy (LJ units)')
	plt.xlim(all_min_energy, all_max_energy)
	plt.ylabel('Similarity (%)')
	plt.ylim(-1,101)
	plt.savefig(data_path+'/'+str(folder_name)+'/sim_vs_energy-population_over_generations_'+str(cluster_type)+'.png')
	plt.clf()

	from matplotlib import pyplot
	from mpl_toolkits.mplot3d import Axes3D
	fig = pyplot.figure()
	ax = Axes3D(fig)
	ax.scatter(all_energies,all_similarities,all_generations,s=1,color=generation_colors)
	ax.set_xlabel('Energy (LJ units)')
	plt.xlim(all_max_energy, all_min_energy)
	ax.set_ylabel('Similarity (%)')
	ax.set_ylim(-1,101)
	ax.set_zlabel('Generations')
	pyplot.savefig(data_path+'/'+str(folder_name)+'/sim_vs_energy_vs_generations-3D-population_over_generations_'+str(cluster_type)+'.png')
	pyplot.clf()

	# ------------------------------------------------------------------------------------------ #
	
	n_pop = len(populations_Per_generation[0])
	n_off = len(offspring_Per_generation[0])
	restart_points = [0] + [n_pop*(gen) for gen in restart_gens] + [len(all_energies)]
	max_restart_length = 0
	for index in range(len(restart_points)-1):
		restart_length = restart_points[index+1] - restart_points[index]
		if restart_length > max_restart_length:
			max_restart_length = restart_length
	color_range = cm.rainbow(np.linspace(1, 0.1, max_restart_length,endpoint=True))
	del restart_points[-1]
	colors_to_use = []
	counter = 0
	for index in range(len(all_energies)):
		colors_to_use.append(color_range[counter])
		counter += 1
		if index in restart_points:
			counter = 0
	plt.scatter(all_similarities,all_energies,s=1,color=colors_to_use)
	plt.xlabel('Similarity (%)')
	plt.xlim(-1,101)
	plt.ylabel('Energy (LJ units)')
	plt.ylim(all_min_energy, all_max_energy)
	#norm = mpl.colors.Normalize(vmin=0, vmax=max_restart_length)
	#plt.pcolor(np.random.rand(10,10),cmap=my_cmap)
	#plt.colorbar()
	plt.savefig(data_path+'/'+str(folder_name)+'/energy_vs_sim-population_over_generations-epoch_reset_color1_'+str(cluster_type)+'.png')
	plt.clf()

	# ------------------------------------------------------------------------------------------ #

	n_pop = len(populations_Per_generation[0])
	n_off = len(offspring_Per_generation[0])
	color_range = cm.rainbow(np.linspace(1, 0.1, len(restart_points),endpoint=True))
	colors_to_use = []
	counter = 0
	for index in range(len(all_energies)):
		colors_to_use.append(color_range[counter])
		if index in restart_points and not index == 0:
			counter += 1
	plt.scatter(all_similarities,all_energies,s=1,color=colors_to_use)
	plt.xlabel('Similarity (%)')
	plt.xlim(-1,101)
	plt.ylabel('Energy (LJ units)')
	plt.ylim(all_min_energy, all_max_energy)
	#norm = mpl.colors.Normalize(vmin=0, vmax=max_restart_length)
	#plt.pcolor(np.random.rand(10,10),cmap=my_cmap)
	#plt.colorbar()
	plt.savefig(data_path+'/'+str(folder_name)+'/energy_vs_sim-population_over_generations-epoch_reset_color2_'+str(cluster_type)+'.png')
	plt.clf()

	# ------------------------------------------------------------------------------------------ #
	# ------------------------------------------------------------------------------------------ #

	#original_populations_Per_generation = get_collection_data(original_population_history,database)
	#get_plots_for_each_epoch(original_populations_Per_generation, restart_gens, all_min_energy, all_max_energy, data_path, str(folder_name))
	#import pdb; pdb.set_trace()
	get_plots_for_each_epoch(populations_Per_generation, restart_gens, data_path, str(folder_name))
	exit()
	# ------------------------------------------------------------------------------------------ #
	# ------------------------------------------------------------------------------------------ #

	# For if you want animated plots -> This does work for Geoff, but not for Frank, Note: GRW 27/8/2020
	#from Check_LJ_Sims_Programs.Animation import AnimatedScatter
	#AnimatedScatter(populations_Per_generation,offspring_Per_generation,data_path+'/'+str(folder_name),cluster_type)

# ------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------ #
'''
LJ_data = 'Tesing_Sim_Theory/LJ38_Test/Epoch_D_Energy_F_Energy/Trial'
gm_min_XYZ = 'data/LJ38_positions_1.txt'
for trial_no in range(1,101):
	print(LJ_data+str(trial_no))
	process_data(LJ_data+str(trial_no),gm_min_XYZ,'LJ38')
'''
# ------------------------------------------------------------------------------------------ #
'''
LJ_data = 'Tesing_Sim_Theory/LJ98_Test/Epoch_D_Energy_F_Energy/Trial'
gm_min_XYZ = 'data/LJ98_positions_1.txt'
for trial_no in range(1,11):
	print(LJ_data+str(trial_no))
	process_data(LJ_data+str(trial_no),gm_min_XYZ,'LJ98')
'''
# ------------------------------------------------------------------------------------------ #






