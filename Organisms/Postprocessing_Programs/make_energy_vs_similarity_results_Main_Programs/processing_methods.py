from ase.db import connect

from make_energy_vs_similarity_results_Main_Programs.data_from_GA_methods import get_cluster_to_compare_against, get_similarity_value_for_half
from make_energy_vs_similarity_results_Main_Programs.data_from_GA_methods import get_EnergyProfile, get_Pop_history, get_collection_data, get_offspring_data

# ------------------------------------------------------------------------------------------------------------------------- %
# ------------------------------------------------------------------------------------------------------------------------- %
# ------------------------------------------------------------------------------------------------------------------------- %
# ------------------------------------------------------------------------------------------------------------------------- %
# The following methods are used to obtain the clusters obtained during the genetic algorithm from the GA_Recording_Database
def get_energy_and_similarity_data_from_GA_Recording_Database(path_to_ga_trial,cluster_to_compare_against):
	# files needed to be used and written to
	databaseDB = path_to_ga_trial+'/Recorded_Data/GA_Recording_Database.db'
	energy_and_similarity_data = path_to_ga_trial+'/Similarity_Data/energy_and_similarity_data.txt'
	energy_and_similarity_dataTXT = open(energy_and_similarity_data,'w')
	cluster_to_compare_against_CNA_profile = get_cluster_to_compare_against(cluster_to_compare_against)
	# compare the clusters in the database to the cluster to compare against
	data = {}
	with connect(databaseDB) as db:
		for row in db.select():
			# make the cluster
			cluster = row.toatoms()
			cluster.center(vacuum=1000)
			# record the important data from the row
			datum = {}
			datum['name'] = int(row['name'])
			datum['gen'] = row['gen_made']
			datum['energy'] = row['cluster_energy']
			datum['id'] = int(row['id'])
			#datum['cluster'] = cluster
			# get CNA profile and similarity data
			CNA_profile = get_CNA_profile(cluster, rCuts)
			datum['CNA_profile'] = CNA_profile
			max_sim, half_sim = get_similarity_value_for_max_and_half(cluster_to_compare_against_CNA_profile,CNA_profile,rCuts)
			#datum['max_sim'] = max_sim
			#datum['half_sim'] = half_sim
			datum['sim'] = sim
			# write data from database to the text file. 
			energy_and_similarity_dataTXT.write(str(datum)+'\n')
			del datum['id']; del datum['name']
			data[row['name']] = datum
	energy_and_similarity_dataTXT.write('Finished\n')
	energy_and_similarity_dataTXT.close()
	return data

# --------------------------------------------------------------------------------------------------------- %
# Get data that has already been analysed and the analysed results recorded to energy_and_similarity_data.txt
def get_energy_and_similarity_data_from_file(path_to_ga_trial):
	energy_and_similarity_data = path_to_ga_trial+'/Similarity_Data/energy_and_similarity_data.txt'
	data = {}
	with open(energy_and_similarity_data) as energy_and_similarity_dataTXT:
		counter = 1
		for line in energy_and_similarity_dataTXT:
			if line.startswith('Finished'):
				break
			if counter%100 == 0:
				print(counter)
			datum = eval(line.rstrip())
			name = datum['name']
			del datum['id']; del datum['name']
			data[row['name']] = datum
			counter += 1
		else:
			print('Error')
			exit()
	return data

# ------------------------------------------------------------------------------------------------------------------------- %
# ------------------------------------------------------------------------------------------------------------------------- %
# ------------------------------------------------------------------------------------------------------------------------- %
# ------------------------------------------------------------------------------------------------------------------------- %
# The following method is designed to obtain the information about when clusters were created during the genetic algorithm. 
def get_information_about_when_clusters_were_created_during_the_GA(path_to_ga_trial,data):
	# Getting data about the clusters when they were made over generations
	clusters_made_each_geneneration, restart_gens = get_EnergyProfile(LJ_data_path)
	# Getting data about the clusters in the population over generations
	original_population_history = get_Pop_history(LJ_data_path, give_full_info=True)
	population_history = deepcopy(original_population_history)
	for restart_gen in sorted(restart_gens,reverse=True):
		del population_history[restart_gen]
	# Getting data about the population over generations
	populations_Per_generation = get_collection_data(population_history,data)
	populations_Per_generation = [population for gen, population in populations_Per_generation]
	# Getting data about the offspring made over generations
	offspring_Per_generation = get_offspring_data(clusters_made_each_geneneration,data)
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
	return all_similarities, all_energies, all_generations

# ------------------------------------------------------------------------------------------------------------------------- %
# ------------------------------------------------------------------------------------------------------------------------- %
# ------------------------------------------------------------------------------------------------------------------------- %
# ------------------------------------------------------------------------------------------------------------------------- %
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
	all_similarities, all_energies, all_generations = get_information_about_when_clusters_were_created_during_the_GA(path_to_ga_trial,data)
	return all_similarities, all_energies, all_generations








