import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from math import ceil
from matplotlib.animation import FuncAnimation
from matplotlib import animation, rc
#animation.rcParams['animation.writer'] = 'ffmpeg'
plt.rcParams['animation.writer'] = 'ffmpeg'
from matplotlib.lines import Line2D

def get_similarities_and_energies_per_generation(Collection_Per_generation):
	all_similarities = []
	all_energies = []
	#all_generations = []
	for generation in range(len(Collection_Per_generation)):
		print('generation: '+str(generation))
		collection_data = Collection_Per_generation[generation]
		#import pdb; pdb.set_trace()
		similarities = [cluster['sim'] for cluster in collection_data]
		energies = [cluster['energy'] for cluster in collection_data]
		generations = [generation for Not_Used in range(len(collection_data))]
		if not (len(similarities) == len(energies) == len(generations)):
			print('Error')
			import pdb; pdb.set_trace()
		all_similarities.append(similarities)
		all_energies.append(energies)
		#all_generations += generations
	return all_similarities, all_energies #, all_generations

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

def AnimatedScatter(Population_Per_generation, Offspring_Per_generation, cluster_folder_path, gps=2, max_time=None, label_no_of_epochs=False, keep_past_population=False):
	"""An animated scatter plot using matplotlib.animations.FuncAnimation."""
	all_similarities_pop, all_energies_pop = get_similarities_and_energies_per_generation(Population_Per_generation)
	all_similarities_off, all_energies_off = get_similarities_and_energies_per_generation(Offspring_Per_generation)

	len_full = len(all_similarities_pop+all_similarities_off)
	len_pop  = len(all_similarities_pop)
	len_off  = len(all_similarities_off)
	print('--------------------------------------------------------------------------------')
	print('Obtaining animation of genetic algorithm that shows the population and offspring.')
	print('Total number of frames: '+str(len_full)+'; Number of population frames (no of generations): '+str(len_pop)+'; Number of offspring frames (should also be no of generations): '+str(len_off))
	if not max_time == None:
		gps = ceil(float(len_full)/(max_time*60.0))
		print('The program will restrict the animation of the genetic algorithm to '+str(max_time)+' minutes (gps = '+str(gps)+').')
	gps = gps*2 # time this by two as a generation here needs to show the population with offspring first, then population without offspring
	gps = gps*4 # dont know why you have to do this but it make sure you do not exceed the time
	print('--------------------------------------------------------------------------------')

	global counter_pop
	counter_pop = 0
	global counter_off
	counter_off = 0

	all_max_energy, all_min_energy = get_energy_limits(all_energies_pop+all_energies_off)

	# Setup the figure and axes...
	fig, ax = plt.subplots()
	legend_elements  = [Line2D([0], [0], marker='o', color="white", label='Pop',markerfacecolor='b', markersize=4)]
	legend_elements += [Line2D([0], [0], marker='o', color="white", label='Off',markerfacecolor='orange', markersize=4)]
	ax.legend(handles=legend_elements, loc='upper right', framealpha=0.3)
	xdata, ydata = [], []
	#ln, = plt.plot([], [], 'bo' , marker=".", markersize=2)
	ln = ax.scatter([], [], s=4)
	if not label_no_of_epochs:
		global era_value
		global no_of_epoches
		global restarts_list_index
		global restarts_list_len
		era_value = 1
		no_of_epoches = 0
		restarts_list_index = 0
		restarts_list_len = len(restarts_list_len)
		era_text   = ax.text(0.02, 0.95, '', transform=ax.transAxes)
		epoch_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
		global restart_gens
		restart_gens = label_no_of_epochs

	if keep_past_population:
		global past_population_similarities
		global past_population_energies
		past_population_similarities = []
		past_population_energies = []

	def init():
		similarities_pop = all_similarities_pop[0]
		energies_pop = all_energies_pop[0]
		ax.set_xlim(-1, 101)
		ax.set_ylim(all_min_energy, all_max_energy)
		ax.set_xlabel('Similarity (%)')
		ax.set_ylabel('Energy (eV)')
		if keep_past_population:
			global past_population_similarities
			global past_population_energies
			past_population_similarities += deepcopy(similarities_pop)
			past_population_energies += deepcopy(energies_pop)
			similarities_pop = past_population_similarities
			energies_pop = past_population_energies
		ln.set_offsets(np.c_[similarities_pop, energies_pop])
		#ln.set_data(similarities_pop, energies)
		ln.set_color(['b']*len(similarities_pop))
		if not label_no_of_epochs:
			global era_value
			global no_of_epoches
			era_text.set_text('Era: '+str(era_value))
			epoch_text.set_text('# epoches: '+str(no_of_epoches))
		return ln,

	def update(frame):
		global counter_pop
		global counter_off
		if frame%100 == 0:
			print(str(frame)+', ', end='')
		similarities_pop = all_similarities_pop[counter_pop]
		energies_pop = all_energies_pop[counter_pop]
		if not label_no_of_epochs:
			global era_value
			global no_of_epoches
		if keep_past_population:
			global past_population_similarities
			global past_population_energies
			past_population_similarities += deepcopy(similarities_pop)
			past_population_energies += deepcopy(energies_pop)
			similarities_pop = past_population_similarities
			energies_pop = past_population_energies
		if frame%2 == 0:
			ln.set_offsets(np.c_[similarities_pop, energies_pop])
			#ln.set_color(['b']*len(similarities_pop))
			if not label_no_of_epochs:
				global restarts_list_index
				global restarts_list_len
				global restart_gens
				if (not restarts_list_len == restarts_list_index) and counter_pop == restart_gens[restarts_list_index]+1:
					era_value += 1
					no_of_epoches += 1
			counter_pop += 1
		else:
			similarities_off = all_similarities_off[counter_off]
			energies_off = all_energies_off[counter_off]
			ln.set_offsets(np.c_[similarities_pop+similarities_off, energies_pop+energies_off])
			ln.set_color(['b']*len(similarities_pop)+['orange']*len(similarities_off))
			counter_off += 1
		if not label_no_of_epochs:
			era_text.set_text('Era: '+str(era_value))
			epoch_text.set_text('# epoches: '+str(no_of_epoches))
		return ln,

	frames = range(len(all_similarities_pop+all_similarities_off))
	print('Frame ', end='')
	ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, repeat=False)

	# Set up formatting for the movie files
	Writer = animation.writers['ffmpeg']
	writer = Writer(fps=gps, metadata=dict(artist='Me'), bitrate=1800)
	ani.save(cluster_folder_path+'/GA_over_generation.mp4', writer=writer)
	print()

def AnimatedScatter_no_offspring(Population_Per_generation, cluster_folder_path, gps=2, max_time=None, label_no_of_epochs=False, keep_past_population=False):
	"""An animated scatter plot using matplotlib.animations.FuncAnimation."""
	all_similarities_pop, all_energies_pop = get_similarities_and_energies_per_generation(Population_Per_generation)

	len_pop  = len(all_similarities_pop)
	print('--------------------------------------------------------------------------------')
	print('Obtaining animation of genetic algorithm with only the population.')
	print('Number of population frames (no of generations): '+str(len_pop))
	if not max_time == None:
		gps = ceil(float(len_pop)/(max_time*60.0))
		print('The program will restrict the animation of the genetic algorithm to '+str(max_time)+' minutes (gps = '+str(gps)+').')
	gps = gps*4 # dont know why you have to do this but it make sure you do not exceed the time
	print('--------------------------------------------------------------------------------')

	global counter_pop
	counter_pop = 0

	all_max_energy, all_min_energy = get_energy_limits(all_energies_pop)

	# Setup the figure and axes...
	fig, ax = plt.subplots()
	legend_elements  = [Line2D([0], [0], marker='o', color="white", label='Pop',markerfacecolor='b', markersize=4)]
	ax.legend(handles=legend_elements, loc='upper right', framealpha=0.3)
	xdata, ydata = [], []
	#ln, = plt.plot([], [], 'bo' , marker=".", markersize=2)
	ln = ax.scatter([], [], s=4)
	if not label_no_of_epochs:
		global era_value
		global no_of_epoches
		global restarts_list_index
		global restarts_list_len
		era_value = 1
		no_of_epoches = 0
		restarts_list_index = 0
		restarts_list_len = len(restarts_list_len)
		era_text   = ax.text(0.02, 0.95, '', transform=ax.transAxes)
		epoch_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
		global restart_gens
		restart_gens = label_no_of_epochs

	if keep_past_population:
		global past_population_similarities
		global past_population_energies
		past_population_similarities = []
		past_population_energies = []

	def init():
		similarities_pop = all_similarities_pop[0]
		energies_pop = all_energies_pop[0]
		ax.set_xlim(-1, 101)
		ax.set_ylim(all_min_energy, all_max_energy)
		ax.set_xlabel('Similarity (%)')
		ax.set_ylabel('Energy (eV)')
		if keep_past_population:
			global past_population_similarities
			global past_population_energies
			past_population_similarities += deepcopy(similarities_pop)
			past_population_energies += deepcopy(energies_pop)
			similarities_pop = past_population_similarities
			energies_pop = past_population_energies
		ln.set_offsets(np.c_[similarities_pop, energies_pop])
		#ln.set_data(similarities_pop, energies)
		ln.set_color(['b']*len(similarities_pop))
		if not label_no_of_epochs:
			global era_value
			global no_of_epoches
			era_text.set_text('Era: '+str(era_value))
			epoch_text.set_text('# epoches: '+str(no_of_epoches))
		return ln,

	def update(frame):
		global counter_pop
		if counter_pop%100 == 0:
			print(str(counter_pop)+', ', end='')
		similarities_pop = all_similarities_pop[counter_pop]
		energies_pop = all_energies_pop[counter_pop]
		if keep_past_population:
			global past_population_similarities
			global past_population_energies
			past_population_similarities += deepcopy(similarities_pop)
			past_population_energies += deepcopy(energies_pop)
			similarities_pop = past_population_similarities
			energies_pop = past_population_energies
		ln.set_offsets(np.c_[similarities_pop, energies_pop])
		if not label_no_of_epochs:
			global era_value
			global no_of_epoches
			global restarts_list_index
			global restarts_list_len
			global restart_gens
			if (not restarts_list_len == restarts_list_index) and counter_pop == restart_gens[restarts_list_index]+1:
				era_value += 1
				no_of_epoches += 1
			era_text.set_text('Era: '+str(era_value))
			epoch_text.set_text('# epoches: '+str(no_of_epoches))
		counter_pop += 1
		return ln,

	frames = range(len(all_similarities_pop))
	print('Frame ', end='')
	ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, repeat=False)
	# Set up formatting for the movie files
	Writer = animation.writers['ffmpeg']
	writer = Writer(fps=gps, metadata=dict(artist='Me'), bitrate=1800)
	ani.save(cluster_folder_path+'/GA_over_generation_only_population.mp4', writer=writer)
	print()
