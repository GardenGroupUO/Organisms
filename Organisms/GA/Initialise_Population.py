from Organisms.GA.Lock import Lock_Remove

def Check_Population_against_predation_operator(population,predation_operator):
	"""
	Checks that all the clusters in this newly initialised population obey the predation operator

	:param population: The population
	:type  population: Organisms.GA.Population
	:param predation_operator: This is the predation operator 
	:type  predation_operator: Organisms.GA.Predation_Operator

	:returns a list of all the clusters that do not obey the predation operator, as well as a report about the issues.
	:rtype   A list of int, and a string
	"""
	# The population will be checked by the Fitness_Factor_Scheme for duplicates. Check_Initial_Population() will delete any clusters that are repeats and present them as cluster_numbers_to_create
	clusters_to_create, removed_clusters_report = predation_operator.check_initial_population(return_report=True)
	# Check to see the number of entries in clusters_to_create is as expected.
	if not population.size-len(population) == len(clusters_to_create):
		print('Error def Initate_New_GAProgram of GAProgram.py: Something weird is going on. The following command: ')
		print('population.size-len(population) == len(clusters_to_create) = False')
		print('It is expected that the difference in the population compared to the maximum number that we want should equal the number of entried in cluster_numbers_to_create')
		print('Not too sure what is going on. Check this.')
		print('population.size = '+str(population.size))
		print('len(population) = '+str(len(population)))
		print('population.size-len(population) = '+str(population.size-len(population)))
		print('len(clusters_to_create) = '+str(len(clusters_to_create)))
		import pdb; pdb.set_trace()
		exit('Program will finish with out completing')

	if len(population) > population.size: 
		print('Error def Initate_New_GAProgram of GAProgram.py: Something weird is going on.')
		print('The population is bigger than the set size by pop_size.')
		print('len(self) (The size of this population) = '+str(len(population)))
		print('self.size  (for class Population) = '+str(population.size))
		print('Check this')
		import pdb; pdb.set_trace()
		exit('Program will finish with out completing')
	elif len(population) < population.size: # If any clusters need to be created to fit inline with the Fitness_Factor_Scheme, repeat the process to get new randomised clusters (repeat while loop).
		if not len(clusters_to_create) > 0:
			print('Error def Initate_New_GAProgram of GAProgram.py: Something weird is going on.')
			print('Shoud not have been caught up in this error. Should have been caught up in the previous error.')
			print('Number of clusters to make = '+str(len(clusters_to_create)))
			print('Check this')
			import pdb; pdb.set_trace()
			exit('Program will finish with out completing')
		print('*****************************')
		print('*****************************')
		print('Diversity Scheme located "duplicates" in creating population.')
		print('Recreating clusters: ' + str([x[1] for x in clusters_to_create]))
		return clusters_to_create, removed_clusters_report
	elif len(population) == population.size:
		return clusters_to_create, removed_clusters_report # Finished initialisation process. The pool is complete and filled with self.size random structures.
	else:
		print('Error in GAProgram, in def Initate_New_GAProgram.')
		print('The population is bigger than its maximum size.')
		print('Check this.')
		print('self.size  (for class Population) = '+str(population.size))
		print('len(self) = ' + str(len(population)))
		import pdb; pdb.set_trace()
		exit('Program will finish with out completing')

# ----------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------------------- #

import os
from ase.io import read as ase_read
from Organisms.GA.Cluster import Cluster
from Organisms.GA.ExternalDefinitions import Exploded
def Place_Already_Created_Clusters_In_Population(population,cluster_makeup,Minimisation_Function,vacuum_to_add_length,r_ij,rounding_criteria,surface,memory_operator,predation_operator,fitness_operator,previous_cluster_name):
	"""
	This method will place any user created clusters into the population.

	:param population: The population
	:type  population: Organisms.GA.Population
	:param cluster_makeup: The makeup of the cluster
	:type  cluster_makeup: dict.
	:param Minimisation_Function: The minimisation function
	:type  Minimisation_Function: __func__
	:param vacuum_to_add_length: The amount of vacuum to place around the cluster
	:type  vacuum_to_add_length: float
	:param r_ij: The maximum distance that should be between atoms to be considered bonded. This value should be as large a possible, to reflected the longest bond possible between atoms in the cluster.
	:type  r_ij: float
	:param rounding_criteria: The number of decimal places to round the energy of clusters to.
	:type  rounding_criteria: int
	:param surface: This is the surface that the cluster is placed on. None means there is no surface.
	:type  surface: Organisms.GA.Surface
	:param memory_operator: The memory operator
	:type  memory_operator: Organisms.GA.Memory_Operator
	:param predation_operator: This is the predation operator 
	:type  predation_operator: Organisms.GA.Predation_Operator
	:param fitness_operator: This is the fitness operator
	:type  fitness_operator: Organisms.GA.Fitness_Operator
	:param previous_cluster_name: This is the name of the last cluster created in the genetic algorithm.
	:type  previous_cluster_name: int

	:returns The name of the most recently created cluster by this method in the population.
	:rtype   int

	"""
	print('Checking to see if the user has any clusters in the folder '+str(population.user_initialised_population_folder)+' that the user would like to have inputted into the initalise population.')
	# First, the definition will check the clusters if there is a population folder. If not, the user does not want to add any clusters to the initial population.
	if population.user_initialised_population_folder == None or population.user_initialised_population_folder == '':
		return 0
	if not os.path.exists(population.user_initialised_population_folder):
		print('Error in def Place_Already_Created_Clusters_In_Population of class Population, in Population.py.')
		print('Yo, The path to the Intialised Population folder that you have specified does not exist.')
		print('Check the path to this folder exists: '+str(population.user_initialised_population_folder))
		print('Note: This variable should include the folder itself as well in the path.')
		exit('This program will end without doing anything.')
	##############################################################################################################################################
	print('################################################################################################################')
	print('################################################################################################################')
	print('Will now initalise the population with clusters from:')
	print(str(population.user_initialised_population_folder))
	print('################################################################################################################')
	print('################################################################################################################')
	##############################################################################################################################################
	# The folder nammed by the variable self.user_initialised_population_folder exists. Lets get whatever clusters are inside this folder.
	cluster_names = [] # holds the cluster dir values, which are equivalent to the number of the folder
	for cluster_name in os.listdir(population.user_initialised_population_folder):
		if cluster_name.startswith('.'):
			continue
		# If the cluster folder exists and the folder is numbered properly, then it is a cluster to be added into the GA program
		if os.path.isdir(os.path.join(population.user_initialised_population_folder, cluster_name)) and cluster_name.isdigit():
			cluster_names.append(int(cluster_name))
		else:
			print('Error in def Place_Already_Created_Clusters_In_Population of class Population, in Population.py.')
			print('Check the Initialised Population folder '+str(population.user_initialised_population_folder)+'. There is a folder which is not an integer')
			print('All folders must be called by an integer as this is how the program names each cluster.')
			print('Check the folder in '+str(population.user_initialised_population_folder)+' to make sure all folders are clusters with integer labels.')
			print('The folder that the GA is specifically having problems with is called '+str(cluster_name))
			print('This program will end without doing anything.')
			exit()
	cluster_names.sort()
	##############################################################################################################################################
	# The clusters that the user has put into the population currently should be in sequential order starting from 1.
	def is_list_sequential(mylist):
		for index in range(0,len(mylist)-1):
		    if not mylist[index+1] == mylist[index]+1:
			    return False
		return True
	if cluster_names == []:
		print('Error in def Place_Already_Created_Clusters_In_Population of class Population, in Population.py.')
		print('There are no clusters in the Initialised Population in the path: '+str(population.user_initialised_population_folder))
		print('Check the Initialised Population folder '+str(population.user_initialised_population_folder))
		print('This program will end without doing anything.')
		exit()
	elif not 1 in cluster_names:
		print('Error in def Place_Already_Created_Clusters_In_Population of class Population, in Population.py.')
		print('One of the clusters in your already created population must have a dir/folder name that is the name "1"')
		print('Check the cluster folders that are in the directory '+str(population.user_initialised_population_folder))
		print('Folder names in '+str(population.user_initialised_population_folder)+' folder: '+str(cluster_names))
		print('This program will end without doing anything.')
		exit()
	elif not is_list_sequential(cluster_names):
		print('Error in def Place_Already_Created_Clusters_In_Population of class Population, in Population.py.')
		print('The names of the clusters/folders in the population folder "'+str(population.user_initialised_population_folder)+'" must be named by numbers in sequential order starting from "1"')
		print('Check the cluster folders that are in the directory '+str(population.user_initialised_population_folder))
		print('Folder names in '+str(population.user_initialised_population_folder)+' folder: '+str(cluster_names))
		print('This program will end without doing anything.')
		exit()
	##############################################################################################################################################
	# The clusters will now be locally minimised as described by the def Minimisation_Function
	for cluster_name in cluster_names:
		##########################################
		# Should be ok, but lets just double check at least that the clusters dir is between 1 and self.size
		if not cluster_name > 0:
			print('Error in def Place_Already_Created_Clusters_In_Population of class Population, in Population.py.')
			print('The dir name of this cluster is less than 0.')
			print('Dir of this cluster: '+str(cluster_name))
			print('Cluster is located in '+str(population.user_initialised_population_folder+'/'+str(cluster_name)))
			print('Check this out')
			import pdb; pdb.set_trace()
			exit()
		elif not cluster_name < population.size+1:
			toStringError = '******************************************************************\n'
			toStringError += 'There are more clusters in '+str(population.user_initialised_population_folder)+' than allowed in this population.\n'
			toStringError += 'The population size for this genetic algorithm run is: '+str(population.size)+'\n'
			toStringError += 'What we are going to do is not import any of the other clusters in the population, only keeping the following clusters\n'
			included_clusters_in_pop = population.get_cluster_names()
			toStringError += str(included_clusters_in_pop)+'\n'
			toStringError += 'We will exclude the following clusters from the population.\n'
			excluded_clusters_in_pop = []
			for cluster_name in cluster_names:
				if not cluster_name in included_clusters_in_pop:
					excluded_clusters_in_pop.append(cluster_name)
			toStringError += str(excluded_clusters_in_pop)+'\n'
			toStringError += 'The genetic algorithm will continue. I hope you know what you are doing.\n'
			toStringError += '******************************************************************\n'
			print(toStringError)
			print(toStringError, file=sys.stderr)
			break
		##########################################
		print('*****************************')
		xyz_files = [file for file in os.listdir(os.path.join(population.user_initialised_population_folder, str(cluster_name))) if file.endswith('.xyz')]
		# Check to find the xyz file that will be used. This xyz file will be considered unoptimsed
		if len(xyz_files) == 0:
			print('Check cluster '+str(cluster_name)+'. There is no .xyz file. The prorgram requires a .xyz file of this cluster so it knows the positions of the atoms in the cluster.')
			exit()
		# File the cluster_name_UnOpt.xyz file. If it cant be found. Tell the user that it doesnt exist 
		# and that this needs to be resolved by them. Note: we want to obtained the "_UnOpt.xyz" file,
		# NOT the _Opt.xyz. This is because we will be optimising it later, and for ease of the programming.
		# I know you might have already use the get_newly initialised_population.py program to get both the 
		# unoptimised and optimised clusters, so you have already optimised the cluster, but this is just easier
		# overall. Take the optimised cluster obtained during the initialised_population.py program as a test to mkae sure 
		# that the unoptimised cluster will not explode before it is used in the GA program. If you want to, you can change
		# this to use the "_Opt.xyz" file, and it probably wont be an issue. You may have to do some changing of the program, 
		# but im sure it will be fine to do.
		for xyz_file in xyz_files:
			if str(cluster_name)+'_UnOpt.xyz' == xyz_file:
				break
		else:
			print('Error in def Place_Already_Created_Clusters_In_Population of class Population, in Population.py.')
			print('There is no .xyz file in Cluster (folder) '+str(cluster_name)+' called " '+str(cluster_name)+'_Opt.xyz.')
			print('This is the cluster xyz file that is used by the genetic algorithm to represent this cluster, as it is assume that it is that cluster, and the "_Opt" indicates that it has been locally optimised.')
			print('Check folder '+str(cluster_name)+' in '+str(population.user_initialised_population_folder)+' for the file "'+str(str(cluster_name)+'_Opt.xyz')+'".')
			print('Ending the genetic algorithm without doing anything.')
			exit()
		# Performed all checks, will now add cluster
		print('Adding Cluster '+str(cluster_name)+' to the population.')
		UnOpt_Cluster = ase_read(population.user_initialised_population_folder+'/'+str(cluster_name)+'/'+xyz_file)
		print('Will locally optimise it as described by your def Minimisation_Function.')
		stdout = sys.stdout; output = StringIO(); sys.stdout = output
		Opt_Cluster, converged, opt_information = Minimisation_Function(UnOpt_Cluster.copy(),population.name,cluster_name) # note, self.name is the population name
		sys.stdout = stdout
		opt_information['output.txt'] = output.getvalue()
		if Exploded(Opt_Cluster,max_distance_between_atoms=r_ij): # make sure the randomised cluster has not split up when optimised.
			print('Error in def Place_Already_Created_Clusters_In_Population of class Population, in Population.py.')
			print("The optimised Cluster exploded. Check out why cluster "+str(cluster_name)+' has exploded by looking at cluster '+str(cluster_name)+'s AfterOpt.traj file.')
			print('The program will now show the optimised and the unoptimised versions of cluster '+str(cluster_name))
			from ase.visualize import view; view(UnOpt_Cluster); view(Opt_Cluster)
			print('This program will end without doing anything.')
			exit()
		elif not converged:
			print('Error in def Place_Already_Created_Clusters_In_Population of class Population, in Population.py.')
			print("This Cluster did not converge when optimised. Check out why cluster "+str(cluster_name)+' did not converge by at the following output from the stdout.')
			print('*******************************************************')
			print(opt_information['output.txt'])
			print('*******************************************************')
			print('The program will also show the optimised and the unoptimised versions of cluster '+str(cluster_name))
			from ase.visualize import view; view(UnOpt_Cluster); view(Opt_Cluster)
			print('This program will end without doing anything.')
			exit()
		elif memory_operator.is_similar_cluster_in_memory_operator(Opt_Cluster):
			print('Error in def Place_Already_Created_Clusters_In_Population, in Initialise_Population.py.')
			print("Cluster "+str(cluster_name)+' in the population is too similar to one of the clusters in your memory operator database.')
			print('Check the clusters that you have included in your population and in the Memory Operator database')
			print('The program will now show the optimised version of cluster '+str(cluster_name))
			from ase.visualize import view; view(Opt_Cluster)
			print('This program will end without doing anything.')
			exit()	
		initialised_cluster = Cluster(Opt_Cluster)
		initialised_cluster.verify_cluster(cluster_name,0,vacuum_to_add_length,rounding_criteria)
		initialised_cluster.remove_calculator()
		# Set some of the details about the cluster that are needed for the population collection to save data to the population database.
		initialised_cluster.ever_in_population = True
		initialised_cluster.excluded_because_violates_predation_operator = False
		initialised_cluster.initial_population = True
		initialised_cluster.removed_by_memory_operator = False
		# Make sure this imported cluster has the correct chemical makeup for this genetic algorithm run.
		if not initialised_cluster.get_elemental_makeup() == cluster_makeup:
			print('Error in def Place_Already_Created_Clusters_In_Population of class Population, in Population.py.')
			print('Cluster '+str(cluster_name)+' does not contain the correct chemical makeup.')
			print('Cluster '+str(cluster_name)+' makeup: '+str(initialised_cluster.get_elemental_makeup()))
			print('Desired makeup: '+str(cluster_makeup))
			print('Check this out.')
			print('This program will end without doing anything')
			exit()
		index = cluster_name - 1
		print('Adding Cluster '+str(cluster_name)+' that the user wants to placed into the population of the GA, before the generation cycles of the GA begins.')
		population.add(index, initialised_cluster) # Place the initialised cluster into the population ## self.Add_ClusterToPopulation(initialised_cluster,index,UnOpt_Cluster=UnOpt_Cluster,Optimisation_Information=opt_information) 
	print('*****************************')
	##############################################################################################################################################
	# Check to make sure that the clusters that have been entered in by the user do not violate the diversity scheme.
	#clusters_removed_from_pop, removed_clusters_report = Fitness_Factor_Scheme.Check_Initial_Population(return_report=True)
	fitness_operator.assign_initial_population_fitnesses()
	clusters_to_create, removed_clusters_report = Check_Population_against_predation_operator(population,predation_operator)
	#import pdb; pdb.set_trace()
	if not len(clusters_to_create) == 0: #len(clusters_removed_from_pop):
		print('Error in def Place_Already_Created_Clusters_In_Population of class Population, in Population.py.')
		print('Some of the clusters that you have placed in the population folder violate the Diversity operator: '+str(predation_operator.Predation_Switch))
		print('Here is a list of the clusters that are the same as other clusters in this population:')
		for cluster_kept_dir, clusters_removed_dirs in sorted(removed_clusters_report,key=lambda x:x[0]):
			clusters_removed_dirs.insert(0,cluster_kept_dir)
			print('Clusters: '+str(clusters_removed_dirs)+' are considered identical by this diversity operator.')
		print('Check this out.')
		print('This program will end without doing anything')
		exit()
	##############################################################################################################################################
	print('Finished importing clusters from '+str(population.user_initialised_population_folder)+' into the population')
	return population[-1].name
	##############################################################################################################################################

# ----------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------------------- #

def get_tasks(population,clusters_to_create,cell_length,vacuum_to_add_length,cluster_makeup,surface,r_ij,rounding_criteria,Minimisation_Function,memory_operator):
	"""
	This is a generator that will allow python to create clusters with multiprocessing.

	:param population: The population
	:type  population: Organisms.GA.Population
	:param clusters_to_create: This is a list of all the names for the clusters to be given.
	:type  clusters_to_create: list of int
	:param cell_length: This is the length of the square unit cell the cluster will be created in.
	:type  cell_length: float
	:param vacuum_to_add_length: The amount of vacuum to place around the cluster
	:type  vacuum_to_add_length: float
	:param cluster_makeup: The makeup of the cluster
	:type  cluster_makeup: dict.
	:param surface: This is the surface that the cluster is placed on. None means there is no surface.
	:type  surface: Organisms.GA.Surface
	:param r_ij: The maximum distance that should be between atoms to be considered bonded. This value should be as large a possible, to reflected the longest bond possible between atoms in the cluster.
	:type  r_ij: float
	:param rounding_criteria: The number of decimal places to round the energy of clusters to.
	:type  rounding_criteria: int
	:param Minimisation_Function: The minimisation function
	:type  Minimisation_Function: __func__
	:param memory_operator: The memory operator
	:type  memory_operator: Organisms.GA.Memory_Operator

	returns list of all the information needed to create a cluster
	rtype   list of Any
	"""
	def tasks(population_name, clusters_to_create, cell_length, vacuum_to_add_length, cluster_makeup, surface, r_ij, rounding_criteria, Minimisation_Function, memory_operator):
		for cluster_to_create in clusters_to_create:
			yield (population_name,cluster_to_create,cell_length,vacuum_to_add_length,cluster_makeup,surface,r_ij,rounding_criteria,Minimisation_Function,memory_operator)
	return tasks(population.name, clusters_to_create,cell_length,vacuum_to_add_length,cluster_makeup,surface,r_ij,rounding_criteria,Minimisation_Function,memory_operator)

import sys
from io import StringIO
from Organisms.GA.Types_Of_Mutations import randomMutate
from Organisms.GA.ExternalDefinitions import Exploded
def create_a_cluster(input_data):
	"""
	This will create a cluster, allowing the user to create cluster via multiprocessing.

	:param input_data: This tuple contains all the information required to create a new randomly generated cluster. 
	:type  input_data: list of Any

	returns tuple of the index to place the cluster into the population, and the optimised cluster
	rtype   (int,Organisms.GA.Cluster)
	"""
	(population_name,cluster_to_create,cell_length,vacuum_to_add_length,cluster_makeup,Surface,r_ij,rounding_criteria,Minimisation_Function,memory_operator) = input_data

	index, cluster_name = cluster_to_create
	#print("Creating Cluster " + str(cluster_name))
	# Make a folder to hold all information about the currently created cluster and move into that folder
	while True: # While statement required for the self.Diversity_switch == "CNA_Full" option and for the Exploded(Opt_Cluster) method
		try:
			UnOpt_Cluster = randomMutate(cell_length,vacuum_to_add_length,cluster_makeup=cluster_makeup)
			stdout = sys.stdout; output = StringIO(); sys.stdout = output
			Opt_Cluster, converged, opt_information = Minimisation_Function(UnOpt_Cluster.deepcopy(),population_name,cluster_name)
			#surface = Surface.get_surface(UnOpt_Cluster)
			#exit('bar1')
			sys.stdout = stdout
			opt_information['output.txt'] = output.getvalue()
		except Exception as exception:
			print('------------------------------------------')
			print('Error during def create_a_cluster in Population.py')
			print(str(exception)+'\n'+'Creating a new cluster.')
			print(str(exception)+'\n'+'Creating a new cluster.', file=sys.stderr)
			print('------------------------------------------')
			continue
		if Exploded(Opt_Cluster,max_distance_between_atoms=r_ij): # make sure the randomised cluster has not split up when optimised.
			print("Cluster exploded. Will obtain a new cluster " + str(cluster_name))
			continue # Since the cluster has exploded, we throw it out and repeat the process by making a new randomised cluster 
		elif not converged:
			print("Cluster did not converge. Will obtain a new cluster " + str(cluster_name))
			continue # Since the cluster did not converge, the cluster is not in a local minimum. This can be a problem its not what we want, and two atoms can be too close to eachother. 
		elif memory_operator.is_similar_cluster_in_memory_operator(Opt_Cluster):
			print("Cluster is too similar to a cluster in Memory Operator. Will obtain a new cluster " + str(cluster_name))
			continue
		else:
			break # break out of this cycle of for loop as we have found a cluster that satifsies the Explosion criteria and self.Diversity_switch is not == to "CNA_Full"

	Opt_Cluster.verify_cluster(cluster_name,0,vacuum_to_add_length,rounding_criteria)
	Opt_Cluster.remove_calculator()
	#print("Finished Creating Cluster " + str(cluster_name))
	return (index,Opt_Cluster)

# ----------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------------------- #

import multiprocessing as mp
def Initialise_Population_with_Randomly_Generated_Clusters(population,cluster_makeup,surface,Minimisation_Function,cell_length,vacuum_to_add_length,r_ij,rounding_criteria,no_of_cpus,memory_operator,predation_operator,fitness_operator,previous_cluster_name):
	"""
	This method will place a number of randomly generated clusters into the population until it is at the desired size.

	:param population: The population
	:type  population: Organisms.GA.Population
	:param cluster_makeup: The makeup of the cluster
	:type  cluster_makeup: dict.
	:param surface: This is the surface that the cluster is placed on. None means there is no surface.
	:type  surface: Organisms.GA.Surface
	:param Minimisation_Function: The minimisation function
	:type  Minimisation_Function: __func__
	:param cell_length: This is the length of the square unit cell the cluster will be created in.
	:type  cell_length: float
	:param vacuum_to_add_length: The amount of vacuum to place around the cluster
	:type  vacuum_to_add_length: float
	:param r_ij: The maximum distance that should be between atoms to be considered bonded. This value should be as large a possible, to reflected the longest bond possible between atoms in the cluster.
	:type  r_ij: float
	:param rounding_criteria: The number of decimal places to round the energy of clusters to.
	:type  rounding_criteria: int
	:param no_of_cpus: The number of cpus available to create clusters 
	:type  no_of_cpus: int
	:param predation_operator: This is the predation operator 
	:type  predation_operator: Organisms.GA.Predation_Operator
	:param fitness_operator: This is the fitness operator
	:type  fitness_operator: Organisms.GA.Fitness_Operator
	:param memory_operator: The memory operator
	:type  memory_operator: Organisms.GA.Memory_Operator
	:param previous_cluster_name: This is the name of the last cluster created in the genetic algorithm.
	:type  previous_cluster_name: int

	returns The name of the most recently created cluster by this method in the population.
	rtype   int

	"""
	##############################################################################################################################################
	# get the dirs of the clusters that need to be populated.
	clusters_to_create = list(zip(range(population.size),range(previous_cluster_name+1,previous_cluster_name+population.size+1)))
	# This part is to prevent the population making new clusters that override the clusters that the user placed into the original population.
	current_cluster_names = population.get_cluster_names() # The current Dir tag of the cluster being inputted or created in the GA. Initially use to record all cluster Dir in run folder. Will be turned into an int once all original clusters in the population have been recorded into the GA program.
	for index in range(len(clusters_to_create)-1,-1,-1):
		if clusters_to_create[index][1] in current_cluster_names:
			del clusters_to_create[index]
	########################################################################################################
	# Initalise the rest of the population by creating randomised clusters using the InitaliseCluster method
	# from InitaliseCluster.py. The name of the dir tags will be those in the clusters_to_create list.
	while True:
		# This will create the required number of clusters to complete the population
		tasks = get_tasks(population,clusters_to_create,cell_length,vacuum_to_add_length,cluster_makeup,surface,r_ij,rounding_criteria,Minimisation_Function,memory_operator)
		'''
		with mp.Pool(processes=no_of_cpus) as pool: # pool = mp.Pool()
			results = pool.map_async(self.create_a_cluster, tasks)
			results.wait()
		made_clusters = results.get()
		'''
		# If you want to do work in serial rather than parallel
		made_clusters = []
		for task in tasks:
			try:
				made_cluster = create_a_cluster(task)
				made_clusters.append(made_cluster)
			except Exception as exception:
				print('Error in def Initialise_Population_with_Randomly_Generated_Clusters, in Initialise_Population.py')
				print('There was an issue with initialising the population with randomly generated clusters.')
				print('The issue was with the following cluster')
				print('\t --> '+str(task))
				print('Check this out, see the following exception for details')
				Lock_Remove()
				raise exception

		for made_cluster in made_clusters:
			index, Opt_Cluster = made_cluster
			Opt_Cluster.ever_in_population = True
			Opt_Cluster.excluded_because_violates_predation_operator = False
			Opt_Cluster.initial_population = True
			Opt_Cluster.removed_by_memory_operator = False
			population.add(index,Opt_Cluster) # Place the initialised cluster into the population
		#except:
		#	print('Weird error happening here? 2')
		#	import pdb; pdb.set_trace()
		#	exit()
		print("-----------------------------")
		# Assign fitnesses to clusters.
		fitness_operator.assign_initial_population_fitnesses()
		print('Checking that the clusters in the population satisfies the Diversity Scheme')
		# Check that the population does not violate the diversity scheme
		clusters_to_create, removed_clusters_report = Check_Population_against_predation_operator(population,predation_operator)
		if clusters_to_create == []:
			break
	return population[-1].name

# ----------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------------------- #
# Initialise the population

def Initialise_Population(population,cluster_makeup,surface,Minimisation_Function,memory_operator,predation_operator,fitness_operator,epoch,cell_length,vacuum_to_add_length,r_ij,rounding_criteria,no_of_cpus,previous_cluster_name=0,generation=0,get_already_created_clusters=True,is_epoch=False,epoch_due_to_population_energy_convergence=None):
	"""
	This method will initalise the Population by
		1. Placing clusters that the user would like in the initial population
		2. Generate a number of extra clusters so that the population has the desired number of clusters in it.

	This method is used when the population is first created when the genetic algorithm is just starting, and when an epoch method is resetting the population with a new population of randomly generated clusters.

	:param population: The population
	:type  population: Organisms.GA.Population
	:param cluster_makeup: The makeup of the cluster
	:type  cluster_makeup: dict.
	:param surface: This is the surface that the cluster is placed on. None means there is no surface.
	:type  surface: Organisms.GA.Surface
	:param Minimisation_Function: The minimisation function
	:type  Minimisation_Function: __func__	
	:param memory_operator: The memory operator
	:type  memory_operator: Organisms.GA.Memory_Operator
	:param epoch: The epoch method
	:type  epoch: Organisms.GA.Epoch	
	:param predation_operator: This is the predation operator 
	:type  predation_operator: Organisms.GA.Predation_Operator
	:param fitness_operator: This is the fitness operator
	:type  fitness_operator: Organisms.GA.Fitness_Operator
	:param cell_length: This is the length of the square unit cell the cluster will be created in.
	:type  cell_length: float
	:param vacuum_to_add_length: The amount of vacuum to place around the cluster
	:type  vacuum_to_add_length: float
	:param r_ij: The maximum distance that should be between atoms to be considered bonded. This value should be as large a possible, to reflected the longest bond possible between atoms in the cluster.
	:type  r_ij: float
	:param rounding_criteria: The number of decimal places to round the energy of clusters to.
	:type  rounding_criteria: int
	:param no_of_cpus: The number of cpus available to create clusters 
	:type  no_of_cpus: int
	:param previous_cluster_name: This is the name of the last cluster created in the genetic algorithm.  Default: 0
	:type  previous_cluster_name: int
	:param generation: The number of generations that have been performed. Default: 0
	:type  generation: int
	:param get_already_created_clusters: Are there clusters that the user created in the population. True if yes, False if no. Default: True
	:type  get_already_created_clusters: bool.
	:param is_epoch: Has the genetic algorithm just epoched. Default: False
	:type  is_epoch: bool.
	:param epoch_due_to_population_energy_convergence: Did the genetic algorithm epochbecause the energies of the clusters in the last populatino converge. Default: None
	:type  epoch_due_to_population_energy_convergence: bool.

	:returns previous_cluster_name: This is the name of the last cluster created by this method
	:rtype   previous_cluster_name: int

	"""
	print('################################################################################################################')
	print('################################################################################################################')
	print("Initalising a Starting Population of Clusters if required to take pool up to a size of " + str(population.size))
	if get_already_created_clusters:
		print("Pool size to begin = " + str(population.get_pool_folder_size(population.user_initialised_population_folder)))
		previous_cluster_name = Place_Already_Created_Clusters_In_Population(population,cluster_makeup,Minimisation_Function,vacuum_to_add_length,r_ij,rounding_criteria,surface,memory_operator,predation_operator,fitness_operator,previous_cluster_name)
	print('################################################################################################################')
	if len(population) < population.size:
		print('Will now population the next '+str(population.size - len(population))+' with randomly generated clusters.')
		previous_cluster_name = Initialise_Population_with_Randomly_Generated_Clusters(population,cluster_makeup,surface,Minimisation_Function,cell_length,vacuum_to_add_length,r_ij,rounding_criteria,no_of_cpus,memory_operator,predation_operator,fitness_operator,previous_cluster_name)
		print('Have finished populating the rest of the population with '+str(population.size - len(population))+' randomly generated clusters.')
	# setting up the epoch and making sure initial population setup is all good
	if not is_epoch:
		if epoch.should_epoch(population,0):
			print('Error in def Initialise_Population in Initialise_Population.py')
			print('Your initial population without any generations somehow has epoched? Not sure how? Check this out')
			exit('Program will finish without completing')
	print('The population has been successfully initialised.')
	print('################################################################################################################')
	print('################################################################################################################')
	population.add_to_history_file(generation,is_epoch=is_epoch,epoch_due_to_population_energy_convergence=epoch_due_to_population_energy_convergence)
	population.current_state_file(generation)
	return previous_cluster_name
