




# ---------------------------------------------------------------------------- %

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

# ---------------------------------------------------------------------------- %

def make_file():
	LJ_gm_cluster = Atoms()
	with open(LJ_gm_minTXT,'r') as LJ_positions:
		for line in LJ_positions:
			xx, yy, zz = line.rstrip().split()
			atom = Atom(symbol='Au', position=(xx, yy, zz))
			LJ_gm_cluster.append(atom)

def get_cluster_to_compare_against(cluster_to_compare_against):
	# get the CNA prfile of the cluster to compare against
	cluster_to_compare_against = minimise(cluster_to_compare_against)
	rCuts = get_rCuts()
	cluster_to_compare_against_CNA_profile = get_CNA_profile(cluster_to_compare_against, rCuts)
	return cluster_to_compare_against_CNA_profile


from ase.db import connect
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

def get_data(LJ_data,LJ_gm_minTXT,cluster_type):

	LJ_dataTXT = LJ_data+'/population_results_'+str(cluster_type)+'.txt'
	databaseDB = LJ_data+'/Recorded_Data/GA_Recording_Database.db'





	# ---------------------------------------------------------------------------- %
	
	db = connect(databaseDB)
	rCuts = get_rCuts()

	resultsTXT = open(LJ_dataTXT,'w')
	for row in db.select():
		numbers = row['numbers']
		positions = row['positions']
		cell = (1000,1000,1000)
		pbc = row['pbc']
		cluster = Atoms()
		for index in range(len(numbers)):
			cluster.append(Atom('Ne', position=list(positions[index]))) # numbers[index]
		cluster.set_cell(cell)
		cluster.center()
		#cluster = minmise(cluster)

		datum = {}
		#datum['cluster'] = cluster
		datum['name'] = row['name']
		datum['gen_made'] = row['gen_made']
		datum['cluster_energy'] = row['cluster_energy']
		datum['id'] = row['id']
		print(datum['id'])

		CNA_profile = get_CNA_profile(cluster, rCuts)
		datum['CNA_profile'] = CNA_profile
		max_sim, half_sim = get_similarity_value_for_max_and_half(LJ_gm_cluster_CNA_profile,CNA_profile,rCuts)
		datum['max_sim'] = max_sim
		datum['half_sim'] = half_sim

		resultsTXT.write(str(datum)+'\n')

	resultsTXT.close()




























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