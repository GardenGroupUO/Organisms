from Organisms.GA.SCM_Scripts.T_SCM_Methods import get_CNA_profile, get_CNA_similarities

# ------------------------------------------------------------------------------------------------------------------------- %
# Supplementary methods for reading data from the GA_Recording_Database

def Minimisation_Function(cluster,calculator):
	cluster.pbc = False
	cluster.set_calculator(calculator)
	from ase.optimize import FIRE
	dyn = FIRE(cluster,logfile=None)
	try:
		dyn.run(fmax=0.01,steps=5000)
		converged = dyn.converged()
		if not converged:
			errorMessage = 'The optimisation of cluster ' + str(cluster_name) + ' did not optimise completely.'
			print(errorMessage, file=sys.stderr)
			print(errorMessage)
	except:
		print('Local Optimiser Failed for some reason.')
	return cluster

def minimise(cluster,calculator):
	cluster.set_cell((1000,1000,1000))
	cluster.center()
	cluster = Minimisation_Function(cluster,calculator)
	cluster.center(vacuum=100)
	return cluster

def minimise_cluster(cluster_to_compare_against,calculator=None):
	# get the CNA prfile of the cluster to compare against
	if not calculator is None:
		cluster_to_compare_against = minimise(cluster_to_compare_against,calculator)
	return cluster_to_compare_against

def get_CNA_Profile_custom(cluster_to_compare_against,rCut):
	cluster_to_compare_against.name = 'test'
	input_data = (cluster_to_compare_against, [rCut])
	name, CNA_profile = get_CNA_profile(input_data)
	return CNA_profile

#def get_similarity_value_for_max_and_half(cluster_1_CNA_profile,cluster_2_CNA_profile):   
def get_similarity_value_for_half(cluster_1_CNA_profile,cluster_2_CNA_profile):
	input_data = ('cluster1','cluster2',cluster_1_CNA_profile,cluster_2_CNA_profile)
	_, _, similarity_values = get_CNA_similarities(input_data)
	return similarity_values[0]
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
	restarts = []
	with open(path_to_Population_history,'r') as Pop_historyTXT:
		for line in Pop_historyTXT:
			if line.startswith('# -> Reset population as reached epoch'):
				restarts.append(generation)
			elif line.startswith('GA Iteration:'):
				generation = int(line.rstrip().replace('GA Iteration: ',''))
			elif line.startswith('Clusters in Pool'):
				clusters_in_pop = line.strip().replace('Clusters in Pool:\t','').split('\t')
				clusters_in_pop = [int(cluster.split('(')[0]) for cluster in clusters_in_pop]
				if give_full_info:
					population_history.append((generation,clusters_in_pop))
				else:
					population_history.append(clusters_in_pop)
	return population_history

def get_population_data(collection_history,energy_and_ga_data,similarity_datum):
	collection_Per_generation = []
	previous_gen = -1
	for gen, col in collection_history:
		collection = []
		for cluster_name in col:
			datum_temp = energy_and_ga_data[cluster_name]
			datum = {}
			datum['name'] = cluster_name
			datum['gen'] = datum_temp['gen']
			datum['energy'] = datum_temp['energy']
			datum['sim'] = similarity_datum[cluster_name] 
			collection.append(datum)
		collection_Per_generation.append((gen,collection))
		if not (previous_gen+1 == gen or previous_gen == gen):
			exit('process get_population_data error')
		previous_gen = gen
	return collection_Per_generation

def get_offspring_data(clusters_made_each_geneneration,energy_and_ga_data,similarity_datum):
	previous_gen = 0
	generation = 1
	offspring_Per_generation = []
	while generation < len(clusters_made_each_geneneration):
		if not (generation in clusters_made_each_geneneration):
			exit('Error, offspring data is missing a generation on offspring information.')
		off = clusters_made_each_geneneration[generation]
		offsprings = []
		for cluster_name in off:
			datum_temp = energy_and_ga_data[cluster_name]
			datum = {}
			datum['name'] = cluster_name
			datum['gen'] = datum_temp['gen']
			datum['energy'] = datum_temp['energy']
			datum['sim'] = similarity_datum[cluster_name] 
			offsprings.append(datum)
		offspring_Per_generation.append((generation,offsprings))
		if not (previous_gen+1 == generation or previous_gen == generation):
			exit('process get_population_data error')
		previous_gen = generation
		generation += 1
	return offspring_Per_generation

# ------------------------------------------------------------------------------------------------------------------------- %

import mmap
def mapcount(filename):
	lines = 0
	if os.stat(filename).st_size == 0:
		return lines
	with open(filename, "r+") as f:
		buf = mmap.mmap(f.fileno(), 0)
		readline = buf.readline
		while readline():
			lines += 1
	return lines

def remove_last_line_of_text(filename,next_cluster_line_counter):
	number_of_lines = mapcount(filename)
	number_of_lines_to_remove = number_of_lines - next_cluster_line_counter + 1
	if number_of_lines_to_remove == 0:
		return
	count = 0
	#save_stdout = sys.stdout
	#sys.stdout = io.BytesIO()
	# determine if a newline \n is at the end of the document
	add_newline_to_end_of_document = False
	with open(filename,'r+b', buffering=0) as f:
		f.seek(0, os.SEEK_END)
		#end = f.tell()
		f.seek(-1, os.SEEK_CUR)
		char = f.read(1)
		if char != b'\n': # and f.tell() == end:
			add_newline_to_end_of_document = True
	# if the text file does not end with \n, add a \n to the end of the text file.
	if add_newline_to_end_of_document:
		with open(filename,'a') as file:
			file.write('\n')
	# remove the appropriate number of line from text. 
	with open(filename,'r+b', buffering=0) as f:
		f.seek(0, os.SEEK_END)
		end = f.tell()
		while f.tell() > 0:
			f.seek(-1, os.SEEK_CUR)
			#print(f.tell())
			char = f.read(1)
			if char != b'\n' and f.tell() == end:
				#sys.stdout = save_stdout
				print("No change: file does not end with a newline")
				exit(1)
			if char == b'\n':
				count += 1
			if count == number_of_lines_to_remove + 1:
				f.truncate()
				#sys.stdout = save_stdout
				#print ("Removed " + str(number_of_lines_to_remove) + " lines from end of file")
				break
			f.seek(-1, os.SEEK_CUR)
	#sys.stdout = save_stdout
	if count < number_of_lines_to_remove + 1:
		print("No change: requested removal would leave empty file")
		exit(3)