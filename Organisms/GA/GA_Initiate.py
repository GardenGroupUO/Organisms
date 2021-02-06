# ---------------------------------------------------------------------------------------------------
def get_resume_from_generation(self):
	"""
	Will determine what the clusters in the population are, and the current generation, if the Organisms program is being restarted or if the number of generations is being increased.

	Will get this information for files in the Population folder.

	:returns: current_generation: The current generation that the Organisms program is being restarted from, or otherwise None if this is a new Organisms program run.
	:rtype: int or None
	:returns: clusters: The clusters in the population. In the formation of [(name of cluster, energy of cluster)]
	:rtype: [(int, float), ...]

	"""
	current_generation, clusters, cluster_energies, got_information_from_backup_state_file = self.population.get_current_generation_from_state_file()
	return current_generation, clusters, cluster_energies, got_information_from_backup_state_file
	#current_generation, clusters = self.population.get_current_generation_from_collection_history()
	#return current_generation, clusters

def Initial_ProgramChecking(self):
	"""
	This definition will check data from files and from that obtained self.get_resume_from_generation() and check to whether
	the program can continue or not.
	"""
	def EndProgram():
		print('The program will end')
		exit()
	if self.resume_from_generation == None:
		return
	if self.resume_from_generation >= self.generations:
		print('The Genetic Algorithm program has already completed the maximum number of generations desired.')
		EndProgram()

# ---------------------------------------------------------------------------------------------------
from Organisms.GA.Initialise_Population import Initialise_Population
def Initate_New_GAProgram(self):
	"""
	Set up the Organisms program to perform a new genetic algorithm run.

	returns: the name of the last cluster that was created.
	rtype: int
	"""
	previous_cluster_name = 0
	generation = 0
	self.epoch.setting_up_for_new_GA()
	self.memory_operator.setup_from_database(0,self.resume_from_generation)
	last_cluster_number = Initialise_Population(self.population,self.cluster_makeup,self.surface,self.Minimisation_Function,self.memory_operator,self.predation_operator,self.fitness_operator,self.epoch,self.cell_length,self.vacuum_to_add_length,self.r_ij,self.rounding_criteria,self.no_of_cpus,previous_cluster_name=previous_cluster_name,generation=generation)
	self.ga_recording_system.record_initial_populations(self.population) # self.ga_recording_system.record_initial_populations(self.population)
	self.ga_recording_system.add_collection(self.population,[])
	self.energyprofile.add_collection(self.population,generation)
	return last_cluster_number

# ---------------------------------------------------------------------------------------------------
import os, sys, time
from Organisms.GA.GA_Program_external_methods import convert_seconds_to_normal_time
def Resume_GAProgram(self, resume_from_generation, clusters_in_resumed_population, clusters_in_resumed_population_energies):
	"""
	This definition initalises all python variables and rewrites and modifies all files to the point when the
	generation self.resume_from_generation finished and the next generation began.

	:param resume_from_generation: the generation the genetic algorithm is resuming from. 
	:type  resume_from_generation: int
	:param clusters_in_resumed_population: list of the name of the clusters in the population to resume from. 
	:type  clusters_in_resumed_population: list of int
	:param clusters_in_resumed_population_energies: list of the name of the clusters in the population to resume from 
	:type  clusters_in_resumed_population_energies: list of float

	returns: the name of the last cluster that was created.
	rtype:   int

	"""
	self.epoch.setting_up_epoch_to_resume_GA()
	if not self.population.have_database:
		print('Error: You are wanting to resume this genetic algorithm, however the population is not recording a database to store the last generation of clusters')
		print('The genetic algorithm is unable to resume without the database of clusters.')
		print('Check this out and restart this genetic algorithm from beginning.')
		exit('This program will finish without completing')
	if not (self.population.does_contain_database(backup=False) or self.population.does_contain_database(backup=True)):
		print('Error: You are wanting to resume this genetic algorithm.')
		print('However, there is no database in the Population folder.')
		print('The genetic algorithm is unable to resume without the database of clusters.')
		print('Check this out and restart this genetic algorithm from beginning.')
		exit('This program will finish without completing')
	if not self.epoch.information_from_the_same_generation(resume_from_generation):
		print('Error in resuming the genetic algorithm')
		print('The current generation is: '+str(resume_from_generation))
		print('However, the information from the epoch is from generation: '+str(self.epoch.initial_generation))
		print('Check this')
		exit('This program will end without doing anything')
	print('----------------------------------------------')
	print('Loading Population stored on disk into program')
	print('----------------------------------------------')
	used_backup = self.population.import_clusters_from_database_to_memory(resume_from_generation, clusters_in_resumed_population, clusters_in_resumed_population_energies, self.rounding_criteria)
	self.population.check_historyfile(resume_from_generation)
	##################################################################################################
	# create folders EnergyProfile and PoolHistory with included files, PoolProfile.txt and EnergyProfile.txt files and get them ready to use.
	self.energyprofile.check(resume_from_generation, self.no_offspring_per_generation)
	# assign fitnesses to the clusters in the population
	self.fitness_operator.assign_resumed_population_fitnesses(resume_from_generation=resume_from_generation)
	##################################################################################################
	# get previous cluster name
	generation, last_cluster_generated_name = self.energyprofile.get_current_generation_and_last_cluster_generated_from_EnergyProfile()
	if not resume_from_generation == generation:
		print('Error at def Resume_GAProgram in GA_Program, in GA_Program.py')
		print('Check')
		import pdb; pdb.set_trace()
		exit()
	##################################################################################################
	# Check that the population obeys the predation operator
	print('----------------------------------------------')
	print('Checking for any predation violation between clusters in the population.')
	print('----------------------------------------------')
	clusters_removed_from_pop, removed_clusters_report = self.predation_operator.check_initial_population(return_report=True)
	if len(clusters_removed_from_pop):
		print('Error in def Place_Already_Created_Clusters_In_Population, in GA_Initiate.py.')
		print('Some of the clusters that you have placed in the population folder violate the Predation Operator: '+str(Fitness_Factor_Operator.Predation_Switch))
		print('Here is a list of the clusters that are the same as other clusters in this population:')
		for cluster_kept_dir, clusters_removed_dirs in sorted(removed_clusters_report.iteritems(),key=lambda x:x[0]):
			clusters_removed_dirs.insert(0,cluster_kept_dir)
			print('Clusters: '+str(clusters_removed_dirs)+' have the same energy.')
		print('Check this out.')
		print('This program will end without doing anything')
		exit()
	##################################################################################################
	# Set up the memory_operator
	self.memory_operator.setup_from_database(last_cluster_generated_name,resume_from_generation)
	for cluster in self.population:
		if self.memory_operator.is_similar_cluster_in_memory_operator(cluster):
			print('Error in def Place_Already_Created_Clusters_In_Population, in GA_Initiate.py.')
			exit('This program will end without doing anything')
	##################################################################################################
	# Check the GA_Recording_Database database
	print('----------------------------------------------')
	print('Checking the GA_Recording_Database database.')
	print('Note that if you have a big database with over 100,000 files, this may take a bit of time.')
	start_checking_ga_recording_system_database = time.time()
	self.ga_recording_system.resume_ga_recording_system_from_current_generation(resume_from_generation)
	end_checking_ga_recording_system_database = time.time()
	print('Checking the GA_Recording_System database took '+convert_seconds_to_normal_time(end_checking_ga_recording_system_database-start_checking_ga_recording_system_database)+'.')
	print('----------------------------------------------')
	##################################################################################################
	if used_backup:
		self.population.move_backup_database_to_normal_backup()
	else:
		self.population.remove_backup_database_if_exists()
	print('----------------------------------------------')
	print('Finished resetting the population.')
	print('Will continue from generation '+str(resume_from_generation+1))
	print('----------------------------------------------')
	return last_cluster_generated_name

# ---------------------------------------------------------------------------------------------------
def add_metadata(self):
	"""
	This is included as this seems to not be added to the collections database when it is first created. Fixing an issue with ASE.
	"""
	self.ga_recording_system.add_metadata()
	self.population.add_metadata()

# ---------------------------------------------------------------------------------------------------
from Organisms.GA.GA_Program_Details import GA_Program_Details
def GA_Initiate(self):
	"""
	This definition provides the details to how to run the genetic algorithm. The program has the ability to restart if required.
	"""
	########################################################
	# Will find out if the program has been run previously and if so, provide details about the generation, the clusters and their energies in the population to resume from.
	#self.resume_from_generation, clusters_in_resumed_population = get_resume_from_generation(self)
	self.resume_from_generation, clusters_in_resumed_population, clusters_in_resumed_population_energies, got_information_from_backup_state_file = get_resume_from_generation(self)
	Initial_ProgramChecking(self)
	#import pdb; pdb.set_trace()
	########################################################
	# Set the Organisms program up so that it ready to begin a new genetic algorithm run, or continue the original genetic algorithm run.
	if self.resume_from_generation == None:
		self.previous_cluster_name = Initate_New_GAProgram(self)
		self.starting_generation = 0
		self.ga_program_details = GA_Program_Details(self, True) # Set up the GA details program to write information about how performance of the genetic algorithm
	elif self.resume_from_generation >= 0: # Continue from the generation that you left off from.
		#import pdb; pdb.set_trace()
		#self.previous_cluster_name, self.resume_from_generation = Resume_GAProgram(self,self.resume_from_generation,clusters_in_resumed_population)
		self.previous_cluster_name = Resume_GAProgram(self,self.resume_from_generation,clusters_in_resumed_population,clusters_in_resumed_population_energies)
		if got_information_from_backup_state_file == True:
			self.population.move_backup_to_current_files()
		self.starting_generation = self.resume_from_generation
		self.ga_program_details = GA_Program_Details(self, False) # Set up the GA details program to write information about how performance of the genetic algorithm
	else:
		exit('Error with resuming genetic algorithm in GA_Initiate.py, def GA_Initiate(self)')
	# The population has been initised either from anew or from some generation, perform the offspring generation and natural selection processes.
	self.starting_generation += 1
	add_metadata(self)
	print('Time elapsed: '+str(self.timer.print_elapsed_time()))
	print('Date and Time: '+str(self.timer.get_time_now()))
