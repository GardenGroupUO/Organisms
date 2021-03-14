






def process_data(data_path,gm_min_XYZ,cluster_type,calculator,rCuts,energy_of_global_minimum,energy_decimal_places):

	print('Processing Data')
	#original_population_history = get_Pop_history(data_path, give_full_info=True)
	#clusters_made_each_geneneration, restart_gens = get_EnergyProfile(data_path)
	#import pdb; pdb.set_trace()

	compared_cluster_name = gm_min_XYZ.split('.')[0].split('/')[-1]
	folder_name = 'Similarity_Investigation_Data'+'/'+compared_cluster_name

	if not os.path.exists(data_path+'/'+folder_name):
		exit('Error')

	#LJ_dataTXT = data_path+'/'+str(folder_name)+'/population_results_'+str(cluster_type)+'.txt'
	#databaseDB = data_path+'/'+str(folder_name)+'/Recorded_Data/GA_Recording_Database.db'

	LJ_gm_cluster = read(gm_min_XYZ)
	LJ_gm_cluster = minimise(LJ_gm_cluster,calculator)
	#tetrahedral_energy = LJ_gm_cluster.get_potential_energy()
	#rCuts = get_rCuts()
	#LJ_gm_cluster_CNA_profile = get_CNA_profile(LJ_gm_cluster, rCuts)

	# ---------------------------------------------------------------------------- %
	#from ase.db import connect

	# #db = connect(databaseDB)
	# #rCuts = get_rCuts()
	# data = []
	# database = {}

	# finishing_generation = float('inf')
	# with open(LJ_dataTXT,'r') as resultsTXT:
	# 	counter = 1
	# 	for line in resultsTXT:
	# 		if counter%500 == 0:
	# 			print(counter)
	# 		datum = eval(line.rstrip())
	# 		if round(datum['cluster_energy'],energy_decimal_places) == energy_of_global_minimum:
	# 			finishing_generation = datum['gen_made']
	# 		if datum['gen_made'] > finishing_generation:
	# 			continue
	# 		data.append(datum)
	# 		name = datum['name']
	# 		#import pdb; pdb.set_trace()
	# 		del datum['CNA_profile']
	# 		database[name] = datum
	# 		counter += 1

	# 		# Debugging issue
	# 		#if counter == 25000:
	# 		#	break
	# final_gen = data[-1]['gen_made']

	# ---------------------------------------------------------------------------- %

	# energies = []
	# max_sims = []
	# sim_halfs = []
	# counter = 0
	# for cluster_datum in data:
	# 	if counter%100 == 0:
	# 		print((counter,cluster_datum['id']))
	# 	energies.append(cluster_datum['cluster_energy'])
	# 	max_sims.append(cluster_datum['max_sim'])
	# 	sim_halfs.append(cluster_datum['half_sim'])
	# 	counter += 1

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
	#n_off = len(offspring_Per_generation[0])
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
	#n_off = len(offspring_Per_generation[0])
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