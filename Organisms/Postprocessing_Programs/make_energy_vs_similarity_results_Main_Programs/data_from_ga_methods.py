from make_energy_vs_similarity_results_Main_Programs.T_SCM_Method import get_CNA_profile

# ------------------------------------------------------------------------------------------------------------------------- %
# Supplementary methods for reading data from the GA_Recording_Database

def get_cluster_to_compare_against(cluster_to_compare_against):
	# get the CNA prfile of the cluster to compare against
	cluster_to_compare_against = minimise(cluster_to_compare_against)
	rCuts = get_rCuts()
	cluster_to_compare_against_CNA_profile = get_CNA_profile(cluster_to_compare_against, rCuts)
	return cluster_to_compare_against_CNA_profile

def minimise(cluster):
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

def get_similarity_value_for_max_and_half(cluster_1_CNA_profile,cluster_2_CNA_profile):   #def get_similarity_value_for_half(cluster_1_CNA_profile,cluster_2_CNA_profile):
	get_similarity_values = get_CNA_similarities(cluster_1_CNA_profile,cluster_2_CNA_profile)
	#return max(get_similarity_values), get_similarity_values[int(len(get_similarity_values)/2)]
	return get_similarity_values[int(len(get_similarity_values)/2)]
# ------------------------------------------------------------------------------------------------------------------------- %
# Supplementary methods for obtaining the information about when clusters were created during the genetic algorithm. 

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

def get_Pop_history(path_to, give_full_info=False):
	path_to_Population_history = path_to+'/Population/Population_history.txt'
	population_history = []
	with open(path_to_Population_history,'r') as Pop_historyTXT:
		for line in Pop_historyTXT:
			if line.startswith('GA Iteration:'):
				generation = int(line.rstrip().replace('GA Iteration: ',''))
			elif line.startswith('Clusters in Pool'):
				clusters_in_pop = line.strip().replace('Clusters in Pool:\t','').split('\t')
				clusters_in_pop = [int(cluster.split('(')[0]) for cluster in clusters_in_pop]
				if give_full_info:
					population_history.append((generation,clusters_in_pop))
				else:
					population_history.append(clusters_in_pop)
	return population_history

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

# ------------------------------------------------------------------------------------------------------------------------- %


