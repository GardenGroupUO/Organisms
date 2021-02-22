import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import animation, rc
animation.rcParams['animation.writer'] = 'ffmpeg'
from matplotlib.lines import Line2D

def get_similarities_and_energies_per_generation(Collection_Per_generation):
	all_similarities = []
	all_energies = []
	#all_generations = []
	for generation in range(len(Collection_Per_generation)):
		print('generation: '+str(generation))
		collection_data = Collection_Per_generation[generation]
		#import pdb; pdb.set_trace()
		similarities = [cluster['half_sim'] for cluster in collection_data]
		energies = [cluster['cluster_energy'] for cluster in collection_data]
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

def AnimatedScatter(Population_Per_generation, Offspring_Per_generation, LJ_data_path, cluster_type):
	"""An animated scatter plot using matplotlib.animations.FuncAnimation."""
	all_similarities_pop, all_energies_pop = get_similarities_and_energies_per_generation(Population_Per_generation)
	all_similarities_off, all_energies_off = get_similarities_and_energies_per_generation(Offspring_Per_generation)

	print(len(all_similarities_pop+all_similarities_off))
	print(len(all_similarities_pop))
	print(len(all_similarities_off))

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

	def init():
		similarities_pop = all_similarities_pop[0]
		energies_pop = all_energies_pop[0]
		ax.set_xlim(-1, 101)
		ax.set_ylim(all_min_energy, all_max_energy)
		ax.set_xlabel('Similarity compared to the GM (%)')
		ax.set_ylabel('Energy (LJ units)')
		ln.set_offsets(np.c_[similarities_pop, energies_pop])
		#ln.set_data(similarities_pop, energies)
		ln.set_color(['b']*len(similarities_pop))
		return ln,

	def update(frame):
		global counter_pop
		global counter_off
		print((frame,counter_pop,counter_off))
		if frame%2 == 0:
			similarities_pop = all_similarities_pop[counter_pop]
			energies_pop = all_energies_pop[counter_pop]
			ln.set_offsets(np.c_[similarities_pop, energies_pop])
			#ln.set_color(['b']*len(similarities_pop))
			counter_pop += 1
		else:
			similarities_pop = all_similarities_pop[counter_pop]
			energies_pop = all_energies_pop[counter_pop]
			similarities_off = all_similarities_off[counter_off]
			energies_off = all_energies_off[counter_off]
			ln.set_offsets(np.c_[similarities_pop+similarities_off, energies_pop+energies_off])
			ln.set_color(['b']*len(similarities_pop)+['orange']*len(similarities_off))
			counter_off += 1
		return ln,

	frames = range(len(all_similarities_pop+all_similarities_off))
	ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, repeat=False)

	# Set up formatting for the movie files
	Writer = animation.writers['ffmpeg']
	writer = Writer(fps=2, metadata=dict(artist='Me'), bitrate=1800)
	ani.save(LJ_data_path+'/GA_over_generation_'+str(cluster_type)+'.mp4', writer=writer)

