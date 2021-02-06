import os

from Organisms.GA.Surface import Surface

from Organisms.GA.Population import Population
from Organisms.GA.Offspring_Pool import Offspring_Pool

from Organisms.GA.Crossover import Crossover
from Organisms.GA.Mutation import Mutation

from Organisms.GA.Memory_Operator import Memory_Operator
from Organisms.GA.Get_Predation_and_Fitness_Operators import get_predation_and_fitness_operators
from Organisms.GA.Epoch import Epoch

from Organisms.GA.GA_Recording_System import GA_Recording_System
from Organisms.GA.EnergyProfile import EnergyProfile
from Organisms.GA.Timer import Timer

def GA_Setup(self,cluster_makeup,pop_size,generations,no_offspring_per_generation,creating_offspring_mode,crossover_type,mutation_types,
	chance_of_mutation,r_ij,vacuum_to_add_length,Minimisation_Function,surface_details,epoch_settings,cell_length,memory_operator_information,
	predation_information,fitness_information,ga_recording_information,force_replace_pop_clusters_with_offspring,user_initialised_population_folder,
	rounding_criteria,print_details,no_of_cpus,finish_algorithm_if_found_cluster_energy,total_length_of_running_time):
	"""
	This method will set up the genetic algorithm.

	:param cluster_makeup: This contains the information on the makeup of the cluster you would like to optimise for. Format is a dictionary in the form of: {element: number of that element}
	:type  cluster_makeup: {str: int, ...}
	:param pop_size: The size of the population
	:type  pop_size: int
	:param generations: The number of generations that are run
	:type  generations: int
	:param no_offspring_per_generation: The number of offspring that are created per generation
	:type  no_offspring_per_generation: int
	:param creating_offspring_mode: This indicates how the offspring are created, either via the mating method 'followed' by the mutation method, or by only perform the mating method 'or' mutation method, or (i.e. either mating and/or mutation). See manual for how to set this.
	:type  creating_offspring_mode: str.
	:param crossover_type: This is the type of crossover that you would like to use. See the manual for more information.
	:type  crossover_type: str.
	:param mutation_types: This is a list that contains all the information about the mutation methods you would like to use. 
	:type  mutation_types: list of (str., float)
	:param chance_of_mutation: This indicates the change of a mutation occuring. See the manual on specifically how this works.
	:type  chance_of_mutation: float
	:param r_ij: This is the maximum bond distance that we would expect in this cluster. See the manual for more information. 
	:type  r_ij: float
	:param vacuum_to_add_length: This is the amount of vacuum to place around the cluster.
	:type  vacuum_to_add_length: float
	:param Minimisation_Function: This is a function that determines how to locally minimise clusters. See manual for more information.
	:type  Minimisation_Function: __func__
	:param surface_details: This functionality has not been designed yet. Default: None
	:type  surface_details: None
	:param epoch_settings: This is designed to hold the information about the epoch method. 
	:type  epoch_settings: dict.
	:param cell_length: This is the length of the cubic unit cell to construct clusters in. See manual for more information. Default: 'default'
	:type  cell_length: float
	:param predation_information: This holds all the information about the predation operator. Default: {'Predation Operator':"Off"}
	:type  predation_information: dict.
	:param fitness_information: This holds all the information about the fitness operator. Default: {'Fitness Operator':"Off"}
	:type  fitness_information: dict.
	:param ga_recording_information: Default: {}
	:type  ga_recording_information: dict.
	:param force_replace_pop_clusters_with_offspring: This will tell the genetic algorithm whether to swap clusters in the populatino with offspring if the predation operator indicates they are the same but the predation operator has a better fitness value than the cluster in the population. 
	:type  force_replace_pop_clusters_with_offspring: bool.
	:param user_initialised_population_folder: This is the directory to a folder containing any custom made clusters you would like to include in the initial population. Set this to None if you do not have any initial clusters to add into the population. Default: None
	:type  user_initialised_population_folder: str. or None
	:param rounding_criteria: The number of decimal places to round the energies of clusters made during the genetic algorithm to. Default: 2
	:type  rounding_criteria: int
	:param print_details: Verbose for this algorithm.
	:type  print_details: bool.
	:param no_of_cpus: The number of cpus that the algorithm can use via multiprocessing. Default: 1
	:type  no_of_cpus: int
	:param finish_algorithm_if_found_cluster_energy: If desired, the algorithm can finish if the LES is located. This is useful to use for methods testing. The algorithm will determine that the LES is found when the genetic algorithm locates the energy of the LES. Read the manual on how to use this. Default: None
	:type  finish_algorithm_if_found_cluster_energy: dict. or None
	:param total_length_of_running_time: The total amount of time to run the genetic algorithm for. If the algorithm is still running after this time, the algorithm will safety finish. Time given in hours. None means no limit on time, Default: None.
	:type  total_length_of_running_time: int or None

	"""
	self.timer = Timer(total_length_of_running_time)
	self.Run_path = os.getcwd()
	# set_number_of_cpus
	self.no_of_cpus = no_of_cpus
	##########################################################################################################
	################################# Variables for the Genetic Algorithm ####################################
	##########################################################################################################
	# This details the elemental and number of atom composition of cluster that the user would like to investigate
	self.cluster_makeup = cluster_makeup
	# Surface Details
	self.surface_details = surface_details
	self.surface = Surface(surface_details)
	self.place_cluster_where = None
	# These are the main variables of the genetic algorithm that with changes could affect the results of the Genetic Algorithm.
	self.population_name = 'Population'
	self.pop_size = pop_size
	self.user_initialised_population_folder = user_initialised_population_folder
	# ------------------------------------------------------------------------------------------- #
	self.population = Population(self.population_name,self.pop_size,user_initialised_population_folder=self.user_initialised_population_folder)
	self.energyprofile = EnergyProfile(self.population)
	if self.energyprofile.is_LES_note_in_EnergyProfile():
		print("Found the note, 'Finished prematurely as LES energy found.', in the populations energyprofile.")
		print('This means you have located the LES that you desired.')
		print('Program will end')
		exit()
	# ------------------------------------------------------------------------------------------- #
	#self.energyprofile_backup = EnergyProfile(self.population)
	self.offspring_pool_name = 'Offspring'
	self.generations = generations
	self.no_offspring_per_generation = no_offspring_per_generation
	self.offspring_pool = Offspring_Pool(self.offspring_pool_name,self.no_offspring_per_generation)
	# These are variables used by the algorithm to make and place clusters in. Variables of the cell to generate offspring
	# ------------------------------------------------------------------------------------------- #
	self.r_ij = r_ij
	self.cell_length = cell_length
	if self.cell_length in ['default','Default','DEFAULT']:
		self.cell_length = self.r_ij * (sum([float(noAtoms) for noAtoms in self.cluster_makeup.values()]) ** (1.0/3.0))
	elif isinstance(self.cell_length,float):
		pass
	else:
		print('Error in your GA Run.py script.')
		print('Your "cell_length" variable is not a float, nor is "default"')
		print('cell_length = '+str(self.cell_length))
		print('Check this. THis program will end without doing anything.')
		exit()
	self.vacuum_to_add_length = vacuum_to_add_length
	# These setting indicate how offspring should be made using the Mating and Mutation Proceedures
	self.creating_offspring_mode = creating_offspring_mode 
	self.crossover_type = crossover_type
	self.mutation_types = mutation_types
	self.chance_of_mutation = chance_of_mutation
	self.crossover_procedure = Crossover(self.crossover_type,self.r_ij,self.vacuum_to_add_length,sum(self.cluster_makeup.values()))
	self.mutation_procedure  = Mutation(self.mutation_types,self.r_ij,self.vacuum_to_add_length)
	# ------------------------------------------------------------------------------------------- #
	# This object will remember any clusters to avoid in the population
	self.memory_operator_information = memory_operator_information
	self.memory_operator = Memory_Operator(self.memory_operator_information)
	# ------------------------------------------------------------- #
	# This contains all the informatino about the predation operator and fitness operator that will be used.
	self.predation_information = predation_information 
	self.fitness_information = fitness_information
	self.predation_operator, self.fitness_operator = get_predation_and_fitness_operators(self.predation_information, self.fitness_information, self.population, self.generations, self.no_of_cpus, False)
	self.force_replace_pop_clusters_with_offspring = force_replace_pop_clusters_with_offspring
	# ------------------------------------------------------------------------------------------- #
	# Create and set the conditions for performing an epoch
	self.epoch = Epoch(epoch_settings,self.Run_path,self.fitness_operator,self.population)
	# ------------------------------------------------------------- #
	# The RunMinimisation.py algorithm is one set by the user. It contain the def Minimisation_Function
	# That is used for local optimisations. This can be written in whatever way the user wants to perform
	# the local optimisations. This is meant to be as free as possible.
	# Variable which provides the directory for the script or program for running the local
	# optimisation method.
	import inspect
	if not inspect.isfunction(Minimisation_Function):
		exit('Error: Minimisation_Function must be a function/def (definition)')
	self.Minimisation_Function = Minimisation_Function
	# These are last techinical points that the algorithm is designed in mind
	if rounding_criteria > 12:
		print('Error, the maximum decimal place rounding, to avoid numerical errors, is 12.')
		print('rounding_criteria: '+str(rounding_criteria))
		exit('Check this out. This program will finish without completing.')
	self.rounding_criteria = rounding_criteria
	self.similarity_rounding_criteria = 10
	# Variables required for the Recording_Cluster.py class/For recording the history as required of the genetic algorithm.
	# For recording the details of the clusters. Recording_Clusters is designed to 
	# keep a history of clusters that have been created during the genetic algorithm.
	self.ga_recording_information = ga_recording_information
	self.ga_recording_system = GA_Recording_System(self.ga_recording_information)
	# For Info.txt
	self.noOfForceCalls = []
	self.timeForForceCalls = []
	##########################################################################################################
	# Set for debugging options
	self.print_details = print_details
	#self.debug = True
	##########################################################################################################
	if finish_algorithm_if_found_cluster_energy == None:
		self.finish_algorithm_if_found_cluster_energy = None
	else:
		if finish_algorithm_if_found_cluster_energy['cluster energy'] == None:
			self.finish_algorithm_if_found_cluster_energy = None
		else:
			self.finish_algorithm_if_found_cluster_energy = finish_algorithm_if_found_cluster_energy['cluster energy']
			self.finish_algorithm_if_found_cluster_rounding = finish_algorithm_if_found_cluster_energy['round']