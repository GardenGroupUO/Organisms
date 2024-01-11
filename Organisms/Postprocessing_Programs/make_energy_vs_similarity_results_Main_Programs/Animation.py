import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from math import ceil
from matplotlib.animation import FuncAnimation
from matplotlib import animation#, rc
#animation.rcParams['animation.writer'] = 'ffmpeg'
plt.rcParams['animation.writer'] = 'ffmpeg'
from matplotlib.lines import Line2D

def get_similarities_and_energies_per_generation(Collection_Per_generation):
	all_similarities = []
	all_energies = []
	all_generations = []
	for index in range(len(Collection_Per_generation)):
		#print('generation: '+str(generation))
		generation, collection_data = Collection_Per_generation[index]
		similarities = [cluster['sim'] for cluster in collection_data]
		energies = [cluster['energy'] for cluster in collection_data]
		generations = [generation for Not_Used in range(len(collection_data))]
		if not (len(similarities) == len(energies) == len(generations)):
			print('Error')
			import pdb; pdb.set_trace()
			exit()
		result1 = all(element == generations[0] for element in generations)
		result2 = all(element == generation for element in generations)
		if not (result1 and result2):
			print('Error')
			import pdb; pdb.set_trace()
			exit()
		all_similarities.append(similarities)
		all_energies.append(energies)
		all_generations.append(generation)
	return all_similarities, all_energies, all_generations

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

TIME_DURATION_UNITS = (('week', 60*60*24*7),('day', 60*60*24),('hour', 60*60),('min', 60),('sec', 1))
def human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'.format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)

def get_estimated_max_time(fps,len_full):
	estimated_max_time = float(len_full)/float(fps)
	return estimated_max_time

def AnimatedScatter(Population_Per_generation, Offspring_Per_generation, cluster_folder_path, gps=1, max_time=None, label_generation_no=False, label_no_of_epochs=False, energy_units='eV', keep_past_population=False):
	"""An animated scatter plot using matplotlib.animations.FuncAnimation."""
	all_similarities_pop, all_energies_pop, all_generations_pop = get_similarities_and_energies_per_generation(Population_Per_generation)
	all_similarities_off, all_energies_off, all_generations_off = get_similarities_and_energies_per_generation(Offspring_Per_generation)

	global len_full
	len_full = len(all_similarities_pop+all_similarities_off)
	len_pop  = len(all_similarities_pop)
	len_off  = len(all_similarities_off)
	print('--------------------------------------------------------------------------------')
	print('Obtaining animation of genetic algorithm that shows the population and offspring.')
	print('Total number of frames: '+str(len_full)+'; Number of population frames (no of generations): '+str(len_pop)+'; Number of offspring frames (should also be no of generations): '+str(len_off))
	if not max_time is None:
		gps = ceil(float(len_full)/(max_time*60.0))
		print('The program will restrict the animation of the genetic algorithm to '+str(max_time)+' minutes (gps = '+str(gps)+').')
	else:
		gps = gps*2 # time this by two as a generation here needs to show the population with offspring first, then population without offspring
		estimated_max_time = get_estimated_max_time(fps=gps,len_full=len_full)
		estimated_max_time = human_time_duration(estimated_max_time)
		print('This animation will have an estimated duration (time length) of '+str(estimated_max_time))
	print('--------------------------------------------------------------------------------')
	# delay the end by NN seconds
	NN = 3
	number_of_repeated_end_frames = gps*NN-1
	print('Number of frames added at end to make a delay of '+str(NN)+' seconds: '+str(number_of_repeated_end_frames))

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
	#xdata, ydata = [], []
	#ln, = plt.plot([], [], 'bo' , marker=".", markersize=2)
	ln = ax.scatter([], [], s=4)

	if isinstance(label_generation_no,list):
		gen_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
		label_generation_no = True

	global restarts_list_index
	global restart_gens
	global restarts_list_len
	restarts_list_index = 0
	restart_gens = list(label_no_of_epochs)
	restarts_list_len = len(restart_gens)
	if isinstance(label_no_of_epochs,list):
		global era_value
		global no_of_epoches
		era_value = 1
		no_of_epoches = 0
		if label_generation_no:
			era_text   = ax.text(0.02, 0.90, '', transform=ax.transAxes)
			epoch_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)		
		else:
			era_text   = ax.text(0.02, 0.95, '', transform=ax.transAxes)
			epoch_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)
		label_no_of_epochs = True

	if keep_past_population:
		global past_population_similarities
		global past_population_energies
		past_population_similarities = []
		past_population_energies = []

	def init():
		similarities_pop = all_similarities_pop[0]
		energies_pop = all_energies_pop[0]
		generation_pop = all_generations_pop[0]
		ax.set_xlim(-1, 101)
		ax.set_ylim(all_min_energy, all_max_energy)
		ax.set_xlabel('Similarity (%)')
		ax.set_ylabel('Energy ('+str(energy_units)+')')
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
		if label_generation_no:
			gen_text.set_text('Generation: '+str(generation_pop))
		if label_no_of_epochs:
			global era_value
			global no_of_epoches
			era_text.set_text('Era: '+str(era_value))
			epoch_text.set_text('# epoches: '+str(no_of_epoches))
		return ln,

	global looking_at_population_only
	looking_at_population_only = True
	def update(frame):
		global looking_at_population_only
		global counter_pop
		global counter_off
		if frame%100 == 0:
			print(str(frame)+', ', end='')
		similarities_pop = all_similarities_pop[counter_pop]
		energies_pop = all_energies_pop[counter_pop]
		generation_pop = all_generations_pop[counter_pop]
		if label_generation_no:
			gen_text.set_text('Generation: '+str(generation_pop))
		if label_no_of_epochs:
			global era_value
			global no_of_epoches
			era_text.set_text('Era: '+str(era_value))
			epoch_text.set_text('# epoches: '+str(no_of_epoches))
		if keep_past_population:
			global past_population_similarities
			global past_population_energies
			past_population_similarities += deepcopy(similarities_pop)
			past_population_energies += deepcopy(energies_pop)
			similarities_pop = past_population_similarities
			energies_pop = past_population_energies

		if looking_at_population_only:
			ln.set_offsets(np.c_[similarities_pop, energies_pop])
			#ln.set_color(['b']*len(similarities_pop))
			global restarts_list_index
			global restarts_list_len
			global restart_gens
			if (not restarts_list_index == restarts_list_len) and (generation_pop == (restart_gens[restarts_list_index] - 0)):
				if label_no_of_epochs:
					era_value += 1
					no_of_epoches += 1
					restarts_list_index += 1
				looking_at_population_only = True
			else:
				looking_at_population_only = False
			counter_pop += 1
		else:
			similarities_off = all_similarities_off[counter_off]
			energies_off = all_energies_off[counter_off]
			generation_off = all_generations_pop[counter_pop]
			if not generation_off == generation_pop:
				exit('Error. not generation_off == generation_pop')
			ln.set_offsets(np.c_[similarities_pop+similarities_off, energies_pop+energies_off])
			ln.set_color(['b']*len(similarities_pop)+['orange']*len(similarities_off))
			counter_off += 1
			looking_at_population_only = True
		global len_full
		if frame >= len_full-1:
			looking_at_population_only = True
			counter_pop -= 1
		return ln,

	frames = range(len(all_similarities_pop+all_similarities_off)+number_of_repeated_end_frames)
	print('Frame ', end='')
	ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, repeat=False)

	# Set up formatting for the movie files
	Writer = animation.writers['ffmpeg']
	writer = Writer(fps=gps, metadata=dict(artist='Me'), bitrate=-1)
	ani.save(cluster_folder_path+'/GA_over_generation.mp4', writer=writer)
	print()

def AnimatedScatter_no_offspring(Population_Per_generation, cluster_folder_path, gps=1, max_time=None, label_generation_no=False, label_no_of_epochs=False, energy_units='eV', keep_past_population=False):
	"""An animated scatter plot using matplotlib.animations.FuncAnimation."""
	all_similarities_pop, all_energies_pop, all_generations_pop = get_similarities_and_energies_per_generation(Population_Per_generation)

	global len_pop
	len_pop  = len(all_similarities_pop)
	print('--------------------------------------------------------------------------------')
	print('Obtaining animation of genetic algorithm with only the population.')
	print('Number of population frames (no of generations): '+str(len_pop))
	if not max_time is None:
		gps = ceil(float(len_pop)/(max_time*60.0))
		print('The program will restrict the animation of the genetic algorithm to '+str(max_time)+' minutes (gps = '+str(gps)+').')
	else:
		estimated_max_time = get_estimated_max_time(fps=gps,len_full=len_pop)
		estimated_max_time = human_time_duration(estimated_max_time)
		print('This animation will have an estimated duration (time length) of '+str(estimated_max_time))
	print('--------------------------------------------------------------------------------')
	# delay the end by NN seconds
	NN = 3
	number_of_repeated_end_frames = gps*NN-1
	print('Number of frames added at end to make a delay of '+str(NN)+' seconds: '+str(number_of_repeated_end_frames))

	global counter_pop
	counter_pop = 0

	all_max_energy, all_min_energy = get_energy_limits(all_energies_pop)

	# Setup the figure and axes...
	fig, ax = plt.subplots()
	legend_elements  = [Line2D([0], [0], marker='o', color="white", label='Pop',markerfacecolor='b', markersize=4)]
	ax.legend(handles=legend_elements, loc='upper right', framealpha=0.3)
	#xdata, ydata = [], []
	#ln, = plt.plot([], [], 'bo' , marker=".", markersize=2)
	ln = ax.scatter([], [], s=4)
	#sample_text1 = ax.text(0.5, 0.5, '', transform=ax.transAxes)
	#sample_text1.set_text('Test 1')
	#sample_text2 = ax.text(0.02, 0.5, '', transform=ax.transAxes)
	if isinstance(label_generation_no,list):
		gen_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
		label_generation_no = True
	if isinstance(label_no_of_epochs,list):
		global era_value
		global no_of_epoches
		global restarts_list_index
		global restarts_list_len
		era_value = 1
		no_of_epoches = 0
		restarts_list_index = 0
		global restart_gens
		restart_gens = list(label_no_of_epochs)
		restarts_list_len = len(restart_gens)
		label_no_of_epochs = True
		if label_generation_no:
			era_text   = ax.text(0.02, 0.90, '', transform=ax.transAxes)
			epoch_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)		
		else:
			era_text   = ax.text(0.02, 0.95, '', transform=ax.transAxes)
			epoch_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)

	if keep_past_population:
		global past_population_similarities
		global past_population_energies
		past_population_similarities = []
		past_population_energies = []

	def init():
		similarities_pop = all_similarities_pop[0]
		energies_pop = all_energies_pop[0]
		generation = all_generations_pop[0]
		ax.set_xlim(-1, 101)
		ax.set_ylim(all_min_energy, all_max_energy)
		ax.set_xlabel('Similarity (%)')
		ax.set_ylabel('Energy ('+str(energy_units)+')')
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
		if label_generation_no:
			gen_text.set_text('Generation: '+str(generation))
		if label_no_of_epochs:
			global era_value
			global no_of_epoches
			era_text.set_text('Era: '+str(era_value))
			epoch_text.set_text('# epoches: '+str(no_of_epoches))
		#sample_text2.set_text('test 2: init')
		return ln,

	def update(frame):
		global counter_pop
		if counter_pop%100 == 0:
			print(str(counter_pop)+', ', end='')
		similarities_pop = all_similarities_pop[counter_pop]
		energies_pop = all_energies_pop[counter_pop]
		generation = all_generations_pop[counter_pop]
		if keep_past_population:
			global past_population_similarities
			global past_population_energies
			past_population_similarities += deepcopy(similarities_pop)
			past_population_energies += deepcopy(energies_pop)
			similarities_pop = past_population_similarities
			energies_pop = past_population_energies
		ln.set_offsets(np.c_[similarities_pop, energies_pop])
		if label_generation_no:
			gen_text.set_text('Generation: '+str(generation))
		if label_no_of_epochs:
			global era_value
			global no_of_epoches
			global restarts_list_index
			global restarts_list_len
			global restart_gens
			era_text.set_text('Era: '+str(era_value))
			epoch_text.set_text('# epoches: '+str(no_of_epoches))
			if (not restarts_list_index == restarts_list_len) and (generation == (restart_gens[restarts_list_index])):
				era_value += 1
				no_of_epoches += 1
				restarts_list_index += 1
		counter_pop += 1
		global len_pop
		if frame >= len_pop-1:
			counter_pop -= 1
		#sample_text2.set_text('test 2: update')
		return ln,

	frames = range(len(all_similarities_pop)+number_of_repeated_end_frames)
	print('Frame ', end='')
	ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, repeat=False)
	# Set up formatting for the movie files
	Writer = animation.writers['ffmpeg']
	writer = Writer(fps=gps, metadata=dict(artist='Me'), bitrate=-1)
	ani.save(cluster_folder_path+'/GA_over_generation_only_population.mp4', writer=writer)
	print()
