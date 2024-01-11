import os, shutil
import numpy as np

import matplotlib.cm as cm
from math import floor, ceil
import matplotlib.pyplot as plt

def get_energy_limits(all_energies):
	all_max_energy = -float('inf')
	all_min_energy = float('inf')
	for energies in all_energies:
		if len(energies) == 0:
			continue
		max_energy = max(energies)
		if max_energy > all_max_energy:
			all_max_energy = max_energy
		min_energy = min(energies)
		if min_energy < all_min_energy:
			all_min_energy = min_energy

	energy_diff = all_max_energy - all_min_energy
	new_energy_diff = (102.0/100.0)*energy_diff
	energy_lim_offset = new_energy_diff - energy_diff
	all_max_energy += energy_lim_offset
	all_min_energy -= energy_lim_offset
	return all_max_energy, all_min_energy

def make_energy_vs_similatity_plot_without_generations(folder_path, energy_and_ga_data, similarity_datum, name_cluster, make_svg_files, energy_units='eV'):
	print('========================= MAKING ENERGY VS SIMILARITY PLOT WITHOUT GENERATION ============================')
	similarities = []
	energies = []
	for name in range(1,len(energy_and_ga_data)+1):
		similarity = similarity_datum[name]
		similarities.append(similarity)
		energy = energy_and_ga_data[name]['energy']
		energies.append(energy)
	plt.scatter(similarities,energies,s=2)
	plt.xlabel('Similarity (%)')
	plt.xlim(-1,101)
	plt.ylabel('Energy ('+str(energy_units)+')')
	all_max_energy, all_min_energy = get_energy_limits([energies])
	plt.ylim((all_min_energy, all_max_energy))
	plt.savefig(folder_path+'/energy_vs_sim_ref_cluster_'+str(name_cluster)+'.png')
	if make_svg_files:
		plt.savefig(folder_path+'/energy_vs_sim_ref_cluster_'+str(name_cluster)+'.svg')
	plt.clf()
	print('==========================================================================================================')
	print('=================== MAKING ENERGY VS SIMILARITY PLOT WITHOUT GENERATION WITH COLOUR ======================')
	plt.scatter(similarities,energies,s=2,)
	plt.xlabel('Similarity (%)')
	plt.xlim(-1,101)
	plt.ylabel('Energy ('+str(energy_units)+')')
	all_max_energy, all_min_energy = get_energy_limits([energies])
	plt.ylim((all_min_energy, all_max_energy))
	plt.savefig(folder_path+'/energy_vs_sim_with_colour_ref_cluster_'+str(name_cluster)+'.png')
	if make_svg_files:
		plt.savefig(folder_path+'/energy_vs_sim_with_colour_ref_cluster_'+str(name_cluster)+'.svg')
	plt.clf()
	print('==========================================================================================================')

def get_plots_for_each_epoch(populations_Per_generation, restart_gens, path, folder_name, make_svg_files, energy_units='eV'):
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
	last_gen = -1
	for gen_NOT_USED, population in populations_Per_generation:
		print(gen_NOT_USED)
		if gen_NOT_USED == last_gen:
			generation -= 1
			if not ((generation in restart_gens) and (gen_NOT_USED in restart_gens)): # and (not found_epoch):
				print('Current epoch error')
				import pdb; pdb.set_trace()
				exit()
			data_plots.append(list(populations_over_an_epoch))
			populations_over_an_epoch = []
		data_population = []
		for cluster in population:
			cluster_energy = cluster['energy']
			max_sim = cluster['sim']
			data_population.append((cluster_energy, max_sim))
			if cluster_energy > max_energy:
				max_energy = cluster_energy
			if cluster_energy < min_energy:
				min_energy = cluster_energy
		data_population = tuple(data_population)
		populations_over_an_epoch.append(data_population)
		last_gen = gen_NOT_USED
		generation += 1
	data_plots.append(list(populations_over_an_epoch))
	for index in range(1,len(data_plots)-1):
		del data_plots[index][-1]
	print('There are '+str(len(data_plots))+' Population optimisations')

	max_no_of_plots_width = 3
	max_no_of_plots_length = 4

	all_energies = [[max_energy],[min_energy]]
	max_energy, min_energy = get_energy_limits(all_energies)

	energy_diff = max_energy - min_energy
	energy_point = min_energy + (95.0/102.0)*energy_diff
	#new_energy_diff = energy_diff*(102.0/100.0)
	#new_energy_diff = (new_energy_diff - energy_diff)/2.0
	#max_energy = max_energy + new_energy_diff
	#min_energy = min_energy - new_energy_diff

	#print(max_energy)
	#print(min_energy)
	#print(energy_diff)
	#print(energy_point)

	def making_plots(data_plots, Per_epoch_folder_path, reverse=False, make_svg_files=False, energy_units='eV'):
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
					axs[plots_length_no, plots_width_no].set_ylabel('Energy ('+str(energy_units)+')')
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
					axs[plots_width_no].set_ylabel('Energy ('+str(energy_units)+')')
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
					if make_svg_files:
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
						axs[plots_length_no, plots_width_no].set_ylabel('Energy ('+str(energy_units)+')')
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
						axs[plots_width_no].set_ylabel('Energy ('+str(energy_units)+')') 
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
		if make_svg_files:
			fig.savefig(Per_epoch_folder_path+'/Energy_vs_Similarity_for_each_epoch_'+plotting_direction+'_page_'+str(pages)+'.svg', dpi=300)
		print('Making population plots per epoch')
		print('-------------------------------------------------------------------')

	def make_individual_plots(data_plots, Per_epoch_folder_path_individual, reverse=False, save_data=False, make_svg_files=False, energy_units='eV'):
		if os.path.exists(Per_epoch_folder_path_individual):
			shutil.rmtree(Per_epoch_folder_path_individual)
		os.makedirs(Per_epoch_folder_path_individual)
		print('-------------------------------------------------------------------')
		print('Making Individual Plots')
		plotting_direction = 'forward' if not reverse else 'reversed'
		#pages = 0
		#plots_length_no = 0
		#plots_width_no = 0
		#for data_plot_counter in range(len(data_plots)):
		#	populations = data_plots[data_plot_counter]
		#data_plot_counter = 1
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

			plt.figure(figsize=(4.0,4.0), dpi=300)
			plt.scatter(similarities, energies, c=colors_for_scatterplot, s=1)
			plt.ylim((min_energy, max_energy))
			plt.xlim((-1,101))
			plt.gca().set_aspect(1.0*abs(101.0--1.0)/abs(float(max_energy) - float(min_energy)), adjustable='box')
			#plt.text(6.0, energy_point, 'Epoch '+str(data_plot_counter) , fontsize=16)
			plt.ylabel('Energy ('+str(energy_units)+')')
			plt.xlabel('Similarity (%)')
			plt.tight_layout()
			plt.savefig(Per_epoch_folder_path_individual+'/Energy_vs_Similarity_per_individual_epoch_'+str(plotting_direction)+'_Epoch_'+str(epoch_no+1)+'.png')
			if make_svg_files:
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
	making_plots(data_plots, Per_epoch_folder_path, reverse=False, make_svg_files=make_svg_files, energy_units=energy_units)

	Per_epoch_folder_path = path+'/'+folder_name+'/'+'energy_per_similarity_for_each_epoch_reversed'
	making_plots(data_plots, Per_epoch_folder_path, reverse=True, make_svg_files=make_svg_files, energy_units=energy_units)

	Per_epoch_folder_path_individual = path+'/'+folder_name+'/'+'energy_per_similarity_for_each_epoch_individual_plots'
	make_individual_plots(data_plots, Per_epoch_folder_path_individual, reverse=False, save_data=True, make_svg_files=make_svg_files, energy_units=energy_units)

	Per_epoch_folder_path_individual = path+'/'+folder_name+'/'+'energy_per_similarity_for_each_epoch_individual_plots_reversed'
	make_individual_plots(data_plots, Per_epoch_folder_path_individual, reverse=True, make_svg_files=make_svg_files, energy_units=energy_units)


from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.Animation import AnimatedScatter
def perform_animations(Population_Per_generation, Offspring_Per_generation, cluster_folder_path, gps=1, max_time=None, label_generation_no=False, label_no_of_epochs=False, energy_units='eV'):
	print('============================== MAKING PLOTTING ANIMATIONS ================================================')
	AnimatedScatter(Population_Per_generation, Offspring_Per_generation, cluster_folder_path, gps=gps, max_time=max_time, label_generation_no=label_generation_no, label_no_of_epochs=label_no_of_epochs, energy_units=energy_units)
	print('==========================================================================================================')


from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.Animation import AnimatedScatter_no_offspring
def perform_animations_no_offspring(Population_Per_generation, cluster_folder_path, gps=1, max_time=None, label_generation_no=False, label_no_of_epochs=False, energy_units='eV'):
	print('============================== MAKING PLOTTING ANIMATIONS ================================================')
	AnimatedScatter_no_offspring(Population_Per_generation, cluster_folder_path, gps=gps, max_time=max_time, label_generation_no=label_generation_no, label_no_of_epochs=label_no_of_epochs, energy_units=energy_units)
	print('==========================================================================================================')
