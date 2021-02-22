from ase.db import connect

def processing_genetic_algorithm_data(path_to_ga_trial,cluster_to_compare_against):
	print('Getting energy and similarity data from the GA_Recording_Database')
	# process energy and similarity data from the GA_Recording_Database
	energy_and_similarity_data = path_to_ga_trial+'/Similarity_Data/energy_and_similarity_data.txt'
	if os.path.exists(energy_and_similarity_data):
		data = get_energy_and_similarity_data_from_GA_Recording_Database(path_to_ga_trial,cluster_to_compare_against)
	else:
		data = get_energy_and_similarity_data_from_file(path_to_ga_trial)
	# path to files
	print('Getting data from the GA about clusters in the population and offspring over generation')
	# Getting data about the clusters when they were made over generations
	clusters_made_each_geneneration, restart_gens = get_EnergyProfile(LJ_data_path)
	# Getting data about the clusters in the population over generations
	original_population_history = get_Pop_history(LJ_data_path, give_full_info=True)
	population_history = deepcopy(original_population_history)
	for restart_gen in sorted(restart_gens,reverse=True):
		del population_history[restart_gen]
	# Getting data about the population over generations
	populations_Per_generation = get_collection_data(population_history,database)
	populations_Per_generation = [population for gen, population in populations_Per_generation]
	# Getting data about the offspring made over generations
	offspring_Per_generation = get_offspring_data(clusters_made_each_geneneration,database)
	# Getting the runs of the genetic algorithm between epochs
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