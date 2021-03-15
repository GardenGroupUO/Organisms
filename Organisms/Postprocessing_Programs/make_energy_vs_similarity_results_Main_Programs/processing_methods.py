from collections import Counter

# ------------------------------------------------------------------------------------------------------------------------- %
# ------------------------------------------------------------------------------------------------------------------------- %
# The following methods are used to obtain the clusters obtained during the genetic algorithm from the GA_Recording_Database
def get_filenames(path_to_ga_trial):
	energy_and_GA_data_filename = path_to_ga_trial+'/Similarity_Investigation_Data/energy_and_GA_data.txt'
	CNA_Profile_data_filename   = path_to_ga_trial+'/Similarity_Investigation_Data/CNA_Profile_data.txt'
	databaseDB_filename = path_to_ga_trial+'/Recorded_Data/GA_Recording_Database.db'
	return energy_and_GA_data_filename, CNA_Profile_data_filename, databaseDB_filename

class Signaller:
	def __init__(self,start_from=1):
		self.cluster_counter = start_from
	def get_signal(self):
		return self.cluster_counter
	def raise_counter(self):
		self.cluster_counter += 1

from Organisms.GA.SCM_Scripts.T_SCM_Methods import get_CNA_profile
def get_energy_and_CNA_profile_data_from_GA_Recording_Database_single(row,rCut,signaller,energy_and_GA_data_filename,CNA_Profile_data_filename):
	name = int(row['name'])
	# make the cluster
	cluster = row.toatoms()
	cluster.center(vacuum=1000)
	# record the important data from the row
	datum_GA = {}
	datum_GA['gen'] = row['gen_made']
	datum_GA['energy'] = row['cluster_energy']
	# get CNA profile and similarity data
	cluster.name = name
	print(str(name)+', ', end='')
	input_data = (cluster, [rCut])
	name, CNA_profile = get_CNA_profile(input_data)
	datum_CNA = {}
	datum_CNA['CNA_profile'] = CNA_profile
	# write data from database to the text file. 
	datum_GA['name'] = name
	datum_CNA['name'] = name
	# files needed to be used and written to
	while not signaller.get_signal() == name:
		pass
	with open(energy_and_GA_data_filename,'a') as energy_and_GA_dataTXT:
		energy_and_GA_dataTXT.write(str(datum_GA)+'\n')
	with open(CNA_Profile_data_filename,'a') as CNA_Profile_dataTXT:
		CNA_Profile_dataTXT.write(str(datum_CNA)+'\n')
	signaller.raise_counter()

from ase.db import connect
from multiprocessing import Pool 
def get_energy_and_CNA_profile_data_from_GA_Recording_Database(energy_and_GA_data_filename,CNA_Profile_data_filename,databaseDB_filename,rCut,no_issues=False,start_from=1,no_of_cpus=1):
	if no_issues:
		return
	# compare the clusters in the database to the cluster to compare against
	print('=============================== ANALYSE CLUSTERS AND CNA PROFILES =======================================')
	print('Cluster Analysed: ', end='')
	signaller = Signaller(start_from)
	with connect(databaseDB_filename) as databaseDB:
		length_of_database = len(databaseDB)
		if no_of_cpus == 1:	
			#for row in databaseDB.select():
			for id_index in range(start_from,length_of_database+1):
				row = databaseDB.get(id=id_index)
				id_index = int(row['id'])
				name = int(row['name'])
				if not id_index == name:
					exit('Error. make a proper thing here')
				get_energy_and_CNA_profile_data_from_GA_Recording_Database_single(row,rCut,signaller,energy_and_GA_data_filename,CNA_Profile_data_filename)
		else:
			results = []
			#for row in databaseDB.select():
			pool = Pool(no_of_cpus)
			for name in range(start_from,length_of_database+1):
				row = databaseDB.get(name=name)
				id_index = int(row['id'])
				name = int(row['name'])
				if not id_index == name:
					exit('Error. make a proper thing here')
				# Run processes in parallel
				task = (row,rCut,signaller,energy_and_GA_data_filename,CNA_Profile_data_filename)
				r = pool.apply_async(get_energy_and_CNA_profile_data_from_GA_Recording_Database_single, task)
				results.append(r)
				# don't let the queue grow too long
				if len(results) == 1000:
					results[0].wait()
			for r in results:
				r.wait()
	with open(energy_and_GA_data_filename,'a') as energy_and_GA_dataTXT:
		energy_and_GA_dataTXT.write('Finished\n')
	with open(CNA_Profile_data_filename,'a') as CNA_Profile_dataTXT:
		CNA_Profile_dataTXT.write('Finished\n')
	print()
	print('==========================================================================================================')

from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.data_from_genetic_algorithm_methods import get_CNA_Profile_custom, get_similarity_value_for_half
def get_similarity_data(path_to_ga_trial,cluster_to_compare_against,rCut,similarity_data_filename,no_issues=False,start_from=1):
	if no_issues:
		return
	cluster_to_compare_against_CNA_profile = get_CNA_Profile_custom(cluster_to_compare_against,rCut)
	# compare the clusters in the database to the cluster to compare against
	_, CNA_Profile_filename, _ = get_filenames(path_to_ga_trial)
	print('=============================== ANALYSE SIMILARITIES ======================================================')
	print('Similarities Analysed: ', end='')
	with open(CNA_Profile_filename,'r') as CNA_Profile_dataTXT:
		for _ in range(start_from-1):
			CNA_Profile_dataTXT.readline()
		for line in CNA_Profile_dataTXT:
			if line.startswith('Finished'):
				continue
			datum = eval(line.rstrip())
			name = datum['name']
			if name%5000 == 0:
				print(str(name)+', ', end='')
			CNA_profile = datum['CNA_profile']
			sim = get_similarity_value_for_half(cluster_to_compare_against_CNA_profile,CNA_profile)
			# write data from database to the text file. 
			with open(similarity_data_filename,'a') as similarity_dataTXT:
				similarity_dataTXT.write(str(name)+': '+str(sim)+'\n')
	with open(similarity_data_filename,'a') as similarity_dataTXT:
		similarity_dataTXT.write('Finished\n')
	print()
	print('==========================================================================================================')

# --------------------------------------------------------------------------------------------------------- %
# Get data that has already been analysed and the analysed results recorded to energy_and_similarity_data.txt

def look_through_file(filename):
	found_finish = False
	next_cluster_line_counter = 1
	with open(filename) as filenameTXT:
		for line in filenameTXT:
			try:
				if line.startswith('Finished'):
					found_finish = True
					break
				datum = eval(line.rstrip())
				name = datum['name']
				if not next_cluster_line_counter == name:
					break
				if next_cluster_line_counter%1000 == 0:
					print(str(next_cluster_line_counter)+', ', end='')
				next_cluster_line_counter += 1
			except:
				break
	return found_finish, next_cluster_line_counter

from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.data_from_genetic_algorithm_methods import remove_last_line_of_text
def check_energy_and_CNA_profile_data_in_file(energy_and_GA_data_filename, CNA_Profile_data_filename):
	no_issues = True
	if os.path.exists(energy_and_GA_data_filename) and os.path.exists(CNA_Profile_data_filename):
		print('=================================== CHECKING CLUSTERS ====================================================')
		print('Cluster Checked: ', end='')
		found_finish_GA,  next_cluster_line_counter_GA  = look_through_file(energy_and_GA_data_filename)
		print()
		print('==========================================================================================================')
		print('=================================== CHECKING CNA PROFILES ================================================')
		print('Cluster Checked: ', end='')
		found_finish_CNA, next_cluster_line_counter_CNA = look_through_file(CNA_Profile_data_filename)
		print()
		print('==========================================================================================================')
		next_cluster_line_counter = min([next_cluster_line_counter_GA,next_cluster_line_counter_CNA])
		if (not found_finish_GA) or (not found_finish_CNA):
			no_issues = False
			print('==========================================================================================================')
			print('Everything is ok until up to line '+str(next_cluster_line_counter)+' of file(s):')
			if next_cluster_line_counter == next_cluster_line_counter_GA:
				print('   * '+str(energy_and_GA_data_filename))
			if next_cluster_line_counter == next_cluster_line_counter_CNA:
				print('   * '+str(CNA_Profile_data_filename))
			print('Will delete everything up to this line in both the '+str(energy_and_GA_data_filename.split('/')[-1])+' and '+str(CNA_Profile_data_filename.split('/')[-1])+' for consistancy and beginning processing the genetic algrorithm data from there.')
			remove_last_line_of_text(energy_and_GA_data_filename,next_cluster_line_counter)
			remove_last_line_of_text(CNA_Profile_data_filename,  next_cluster_line_counter)
			print('==========================================================================================================')
	else:
		if os.path.exists(energy_and_GA_data_filename):
			shutil.rmtree(energy_and_GA_data_filename)
		if os.path.exists(CNA_Profile_data_filename):
			shutil.rmtree(CNA_Profile_data_filename)
		next_cluster_line_counter = 1
		no_issues = False
	return no_issues, next_cluster_line_counter

def check_similarity_data_in_file(similarity_data_filename):
	found_finish = False
	next_cluster_line_counter = 1
	if os.path.exists(similarity_data_filename):
		with open(similarity_data_filename) as similarity_dataTXT:
			print('================================= CHECKING SIMILARITIES ==================================================')
			print('Similarities Checked: ', end='')
			for line in similarity_dataTXT:
				try:
					if line.startswith('Finished'):
						found_finish = True
						break
					name, similarity = line.rstrip().split(':')
					name = int(name)
					if not next_cluster_line_counter == name:
						break
					if next_cluster_line_counter%5000 == 0:
						print(str(next_cluster_line_counter)+', ', end='')
					if not isinstance(similarity,float):
						print('Error in check_similarity_data_in_file in processing_methods.py')
						print('A similarity is not given as a float in '+str(similarity_data_filename))
						print('Cluster name: '+str(name))
						print('Similarity: '+str(similarity))
						print('Check this out.')
						exit('This program will finish without completing.')
					next_cluster_line_counter += 1
				except:
					break
			print()
			print('==========================================================================================================')
		if not found_finish:
			print('==========================================================================================================')
			print('Everything is ok until up to line '+str(next_cluster_line_counter)+' of '+str(similarity_data_filename)+'.')
			print('Will delete everything in '+str(similarity_data_filename.split('/')[-1])+' up to this line.')
			remove_last_line_of_text(similarity_data_filename,next_cluster_line_counter)
			print('==========================================================================================================')
	return found_finish, next_cluster_line_counter

# ------------------------------------------------------------------------------------------------------------------------- %
# ------------------------------------------------------------------------------------------------------------------------- %
# The following methods are designed to obtain energy+GA data as well as similarity data from files
def get_energy_and_CNA_profile_data_from_file(path_to_ga_trial):
	energy_and_GA_data_filename, _, _ = get_filenames(path_to_ga_trial)
	data = {}
	print('===================== ADDING CLUSTERS TO MEMORY ==========================================================')
	print('Adding Clusters to Memory: ', end='')
	with open(energy_and_GA_data_filename) as energy_and_GA_dataTXT:
		for line in energy_and_GA_dataTXT:
			if line.startswith('Finished'):
				continue
			datum = eval(line.rstrip())
			name = datum['name']
			if name%5000 == 0:
				print(str(name)+', ', end='')
			del datum['name']
			data[name] = datum
	print()
	print('==========================================================================================================')
	return data

def get_similarity_data_from_file(similarity_data_filename,cluster_to_compare_number):
	similarity_data = {}
	print('========================= ADDING SIMILARITIES TO MEMORY ==================================================')
	print('Adding Similarities to Memory: ', end='')
	with open(similarity_data_filename) as similarity_dataTXT:
		for line in similarity_dataTXT:
			if line.startswith('Finished'):
				continue
			name, similarity = line.rstrip().split(':')
			name = int(name)
			if name%5000 == 0:
				print(str(name)+', ', end='')
			similarity = float(similarity)
			similarity_data[name] = similarity
	print()
	print('==========================================================================================================')
	return similarity_data

# ------------------------------------------------------------------------------------------------------------------------- %
# ------------------------------------------------------------------------------------------------------------------------- %
# The following method is designed to obtain the information about when clusters were created during the genetic algorithm. 
from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.data_from_genetic_algorithm_methods import get_EnergyProfile, get_Pop_history, get_population_data, get_offspring_data
def get_information_about_when_clusters_were_created_during_the_GA(path_to_ga_trial,energy_and_ga_data,similarity_datum):
	print('========================== PROCESS ENERGY VS SIMILARITY RESULTS OVER GENERATIONS =========================')
	# Getting data about the clusters when they were made over generations
	clusters_made_each_geneneration, restart_gens = get_EnergyProfile(path_to_ga_trial)
	# Getting data about the clusters in the population over generations
	original_population_history = get_Pop_history(path_to_ga_trial, give_full_info=True)
	##########################################################################################
	#population_history = deepcopy(original_population_history)
	#for restart_gen in sorted(restart_gens,reverse=True):
	#	del population_history[restart_gen]
	population_history = original_population_history
	##########################################################################################
	# Getting data about the population over generations
	populations_Per_generation = get_population_data(population_history,energy_and_ga_data,similarity_datum)
	#populations_Per_generation = [population for gen, population in populations_Per_generation]
	# Getting data about the offspring made over generations
	offspring_Per_generation = get_offspring_data(clusters_made_each_geneneration,energy_and_ga_data,similarity_datum)
	# Getting the runs of the genetic algorithm between epochs
	runs_between_epochs = []
	between_restart_gens = [0] + restart_gens + [len(population_history)]
	for index in range(len(between_restart_gens)-1):
		starting_gen = between_restart_gens[index]
		ending_gen   = between_restart_gens[index+1]
		runs_between_epochs.append([x[1] for x in population_history[starting_gen:ending_gen]])

	#clusters_to_record_full = []
	#for run_between_epochs in runs_between_epochs:
	#	clusters_to_record_full.append((min(run_between_epochs[0]), max(run_between_epochs[-1])))

	#clusters_to_record = []
	#for restart in restarts:
	#	clusters_to_record.append(clusters_to_record_full[restart-1])
	#import pdb; pdb.set_trace()

	all_similarities = []
	all_energies = []
	all_generations = []
	#print('Generations: ', end='')
	for index in range(len(populations_Per_generation)):
		#print(str(generation)+', ',end='')
		generation, population_data = populations_Per_generation[index]
		similarities = [cluster['sim'] for cluster in population_data]
		energies = [cluster['energy'] for cluster in population_data]
		generations = [generation for Not_Used in range(len(population_data))]
		if not (len(similarities) == len(energies) == len(generations)):
			print('Error')
			import pdb; pdb.set_trace()
		all_similarities += similarities
		all_energies += energies
		all_generations += generations
	#print()
	print('==========================================================================================================')
	return all_similarities, all_energies, all_generations, populations_Per_generation, offspring_Per_generation, restart_gens, between_restart_gens, runs_between_epochs
