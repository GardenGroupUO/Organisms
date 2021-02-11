import os, sys
from time import time

from Organisms.GA.GA_Setup import GA_Setup
from Organisms.GA.GA_Introducing_Remarks import Introducing_Remarks
from Organisms.GA.GA_Initiate import GA_Initiate
from Organisms.GA.GA_Program_external_methods import if_to_finish_because_found_cluster_energy, check_names_1, check_names_2, add_metadata, floor_float, reset_population, check_files_for_readable_and_writable
from Organisms.GA.Lock import Lock_Check_and_Set #, Lock_Remove

from Organisms.GA.Get_Offspring import Create_An_Offspring

from io import StringIO
import multiprocessing as mp
from Organisms.GA.exitting_procedure import add_to_exitting_procedure

class GA_Program():
	"""
	The Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similarity (Organisms) program has been designed to perform a genetic algorithm for a nanoparticle of any composition and any size. 

	It has been designed for that it can be modified by others in the Garden group after I have left. Hopefully the code is readable and can be tuned, however I have tried to note what is happening during the code and why.
	More notes can be found in the 

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
	def __init__(self,cluster_makeup,pop_size,generations,no_offspring_per_generation,creating_offspring_mode,crossover_type,mutation_types,
		chance_of_mutation,r_ij,vacuum_to_add_length,Minimisation_Function,surface_details=None,epoch_settings={'use epoch': 'off'},
		cell_length='default',memory_operator_information={'perform_memory_operator':'Off'},predation_information={'Predation_Switch':"Off"},
		fitness_information={'Fitness_Switch':"Energy"},ga_recording_information={},force_replace_pop_clusters_with_offspring=True,
		user_initialised_population_folder=None,rounding_criteria=2,print_details=False,no_of_cpus=1,finish_algorithm_if_found_cluster_energy=None,
		total_length_of_running_time=None):

		# Check lock, and if ok to run set a program lock, then
		Lock_Check_and_Set()
		# Check to make sure that all files in the folder are readable and writeable
		check_files_for_readable_and_writable()
		# Set up the genetic algorithm
		GA_Setup(self,cluster_makeup,pop_size,generations,no_offspring_per_generation,creating_offspring_mode,crossover_type,mutation_types,chance_of_mutation,r_ij,vacuum_to_add_length,Minimisation_Function,surface_details,epoch_settings,cell_length,memory_operator_information,predation_information,fitness_information,ga_recording_information,force_replace_pop_clusters_with_offspring,user_initialised_population_folder,rounding_criteria,print_details,no_of_cpus,finish_algorithm_if_found_cluster_energy,total_length_of_running_time)# introduction remarks
		# print introductory notes about your genetic algorithm run
		Introducing_Remarks(self)
		# Check the GA before beginning and initiate the GA program
		GA_Initiate(self)
		# Run the main component of the GA
		self.run_GA()
		##########################################################################################################
		##########################################################################################################
		##########################################################################################################

	def run_GA(self):
		"""
		This definition is the base of the algorithm. Once the algorithm has set itself up, this will run the genetic algorithm
		"""
		print("-----------------------------")
		print("-----------------------------")
		print("Starting Genetic Algorithm")
		print("-----------------------------")
		print("-----------------------------")
		print(" ")
		finish_because_found_cluster_energy = False
		for generation_number in range(self.starting_generation,self.generations+1):
			start_time = time()
			check_names_1(self.population)
			#if if_to_finish_because_found_cluster_energy(self):
			#	finish_because_found_cluster_energy = True
			#	break
			#Create all backup files before the generation begins
			self.population.backup_files()
			self.epoch.backup()
			# -------------------------------------------------------------------------------------------------
			self.ga_program_details.start_clock()
			print('\n')
			print("----------------------------------------------------------")
			generation_wording = "RUNNING GENERATION " + str(generation_number)
			print('#'*len(generation_wording))
			print(generation_wording)
			print('#'*len(generation_wording))
			start_time = time()
			# Get all offspring for this generation
			self.previous_cluster_name = self.get_offsprings(self.previous_cluster_name,generation_number)
			all_energies_of_offpsring = self.offspring_pool.get_cluster_energies()
			check_names_2(self.population,self.offspring_pool)
			# The energy from the offspring clusters are recorded into the energyprofile. 
			self.energyprofile.add_collection(self.offspring_pool,generation_number)
			##############################################################################
			############################# MEMORY OPERATION ###############################
			# remove clusters that are too similar to clusters in the memory
			memory_operator_timer_1_start = time()
			offspring_to_remove_because_too_similar_to_a_cluster_in_memory = self.memory_operator.check_collection(self.offspring_pool)
			clusters_being_removed_by_memory_operator = self.memory_operator.remove_similar_clusters_from_offsprng_pool(self.offspring_pool,offspring_to_remove_because_too_similar_to_a_cluster_in_memory,self.print_details)
			if not len(clusters_being_removed_by_memory_operator) == 0:
				self.ga_recording_system.add_collection(clusters_being_removed_by_memory_operator, [])
			memory_operator_timer_1_end = time()
			##############################################################################
			############################# FITNESS CHECK 1 ################################
			# Assign the fitnesses of each of the offspring. This is done before the predation check 
			# as the predation check may need to use the fitnwss values to make decisions
			# Add offspring information to the fitness operator's database, if it uses one.
			fitness_timer_1_start = time()
			self.fitness_operator.add_to_database(self.offspring_pool)
			# Assign fitnesses
			self.fitness_operator.assign_all_fitnesses_before_assess_against_predation_operator(self.offspring_pool,generation_number)
			fitness_timer_1_end = time()
			##############################################################################
			########################### PREDATION OPERATION ##############################
			predation_timer_1_start = time()
			# Add offspring information to the predation operator's database, if it uses one.
			self.predation_operator.add_to_database(self.offspring_pool)
			# Identify which offspring need to be removed and potentially population that need to be replaced by offspring due to violations in predation.
			offspring_to_remove_violated_predation_operator, population_to_be_replaced_by_offspring = self.predation_operator.assess_for_violations(self.offspring_pool,self.force_replace_pop_clusters_with_offspring)
			# assign cluster information if it was placed in the population and if it was excluded by the predation method. 
			for cluster in self.offspring_pool:
				cluster.ever_in_population = (cluster.name in population_to_be_replaced_by_offspring)
				cluster.excluded_because_violates_predation_operator = (cluster.name in offspring_to_remove_violated_predation_operator)
				cluster.initial_population = False
				cluster.removed_by_memory_operator = False
			# Record clusters that were made during this generation
			self.ga_recording_system.add_collection(self.offspring_pool, offspring_to_remove_violated_predation_operator)
			# Remove offspring that violate the predation operator, and replace clusters in the population with offspring to comply with the predation operator.
			self.predation_operator.remove_offspring_and_replace_with_population_that_violate_predation_operator(self.population, self.offspring_pool, offspring_to_remove_violated_predation_operator, population_to_be_replaced_by_offspring)
			predation_timer_1_end = time()
			##############################################################################
			############################# FITNESS CHECK 2 ################################
			fitness_timer_2_start = time()
			# Remove offspring from the fitness operator's database that were removed by the predation operator during the PREDATION OPERATION.
			offspring_to_remove_violated_predation_operator = [off_name for off_name, off_index in offspring_to_remove_violated_predation_operator]
			population_to_be_replaced_by_offspring = [pop_name for pop_name, off_name in population_to_be_replaced_by_offspring]
			self.fitness_operator.remove_from_database(offspring_to_remove_violated_predation_operator+population_to_be_replaced_by_offspring)
			# Assign fitnesses to the offspring and clusters in the population before natural selection.
			self.fitness_operator.assign_all_fitnesses_after_assess_against_predation_operator(self.offspring_pool, generation_number, offspring_to_remove_violated_predation_operator)
			fitness_timer_2_end = time()
			##############################################################################
			############################# NATURAL SELECTION ##############################
			# Make a backup of the population before offspring are added to the population.
			# This has been added just in case there is a system crash, and the Organisms program needs to be restarted. 
			natural_selection_timer_start = time()
			# Perform the natural selection proceedure.
			clusters_removed_from_the_population = self.natural_selection(self.offspring_pool,generation_number)
			# clear the offspring_pool
			cleaned_offspring_names = self.offspring_pool.clean()
			natural_selection_timer_end = time()
			# Add data to the population history about the clusters in the population after this generation and their energies. 
			self.population.add_to_history_file(generation_number)
			##############################################################################
			################################# EPOCH ######################################
			###################### PREDATION and FITNESS UPDATE ##########################
			ending_timer_start = time()
			# This part of the code will perform an epoch proceedure if required.
			# Four options can occur at this point
			# 1a. If the population has converged energetically and the fitness is based completely or in part on the energy fitness function, 
			#     we will also want to reset the predation and fitness operators as well as restarting the population from fresh.
			# 1b. If the population has converged structurally and the fitness is based completely or in part on the structural component of
			#     the structure + energy fitness function, we will also want to reset the predation and fitness operators as well as 
			#     restarting the population from fresh.
			# 1c. If a epoch occurs, then we want to reset the predation and fitness operators as well as
			#     restarting the population from fresh.
			# 2.  If an epoch does not need to occur, we want to assign a fitness to each cluster in the
			#     population based on only the clusters in the population, as well as update the information 
			#     in the predation operator if needed. 
			is_energy_in_fitness_function = self.fitness_operator.fitness_switch == 'Energy' or (self.fitness_operator.fitness_switch == 'SCM + Energy' and not self.fitness_operator.SCM_fitness_contribution == 1.0)
			is_SCM_in_fitness_function = self.fitness_operator.fitness_switch == 'SCM + Energy' and not self.fitness_operator.SCM_fitness_contribution == 0.0
			if is_energy_in_fitness_function and not self.population.is_there_an_energy_range(self.rounding_criteria):
				reset_population(self,generation_number)
			elif is_SCM_in_fitness_function and not self.fitness_operator.is_there_an_similarity_range(self.similarity_rounding_criteria):
				reset_population(self,generation_number)
			elif self.epoch.should_epoch(self.population,generation_number):
				if self.epoch.first_epoch_to_change_fitness_function:
					perform_reset_population, self.fitness_operator = self.epoch.change_fitness_function(self.fitness_operator)
					if perform_reset_population:
						reset_population(self,generation_number)
				else:
					reset_population(self,generation_number)
				#reset_population(self,generation_number)
			else:
				self.fitness_operator.remove_from_database(clusters_removed_from_the_population+cleaned_offspring_names)
				self.fitness_operator.assign_all_fitnesses_after_natural_selection(generation_number)
				self.predation_operator.remove_from_database(offspring_to_remove_violated_predation_operator+population_to_be_replaced_by_offspring+clusters_removed_from_the_population+cleaned_offspring_names)
			##############################################################################
			# Save a copy of the while population at specified generations that is a complete snapshot of the algorithm at this point. It is different to what is happening with self.ga_recording_system.add_collection
			self.ga_recording_system.record_population_at_generation(self.population,generation_number)
			# Write information about performance of this generation run to ga_program_details
			self.ga_program_details.end_clock(generation_number)
			# This is a hack to get metadata into the databases for Population, Offspring_Pool, and GA_Recording_System.
			if generation_number == 1:
				add_metadata(self)
			# save the current state of the population
			self.population.current_state_file(generation_number)
			if self.print_details:
				print(self.population)
			##############################################################################
			# The generation is now complete, remove all backup files. 
			self.population.remove_backup_files()
			self.epoch.remove_backup()
			##############################################################################
			# End with the amount of time it took to run the generation.
			ending_timer_end = time()
			end_time = time()
			fitness_timer_1 = fitness_timer_1_end - fitness_timer_1_start
			memory_operator_timer_1 = memory_operator_timer_1_end - memory_operator_timer_1_start
			predation_timer_1 = predation_timer_1_end - predation_timer_1_start
			fitness_timer_2 = fitness_timer_2_end - fitness_timer_2_start
			ending_timer = ending_timer_end - ending_timer_start
			print('Time Information')
			print('fitness_timer_1   = '+str(fitness_timer_1)+' seconds')
			print('memory_operator_timer_1   = '+str(memory_operator_timer_1)+' seconds')
			print('predation_timer_1 = '+str(predation_timer_1)+' seconds')
			print('fitness_timer_2   = '+str(fitness_timer_2)+' seconds')
			print('ending_timer      = '+str(ending_timer)+' seconds')
			print('The amount of time required for generation ' + str(generation_number) + ' is ' + str(end_time - start_time)+' seconds')
			print("----------------------------------------------------------")
			if os.path.exists('finish'):
				print('I have found a file called "finish", meaning you want to stop the GA safely')
				print('The GA is stopping now. The generation is '+str(generation_number))
				print('It is possible to resume the genetic algorithm from this point.')
				print('The genetic algorithm will end')
				break
			elif self.timer.has_elapsed_time():
				print('The GA has taken longer than the user intends'+str(self.timer.total_length_of_running_time)+' hrs.')
				print('The GA is stopping now. The generation is '+str(generation_number))
				print('It is possible to resume the genetic algorithm from this point.')
				print('The genetic algorithm will end')
				break
			print('Time elapsed: '+str(self.timer.print_elapsed_time()))
			print('Date and Time: '+str(self.timer.get_time_now()))
			if if_to_finish_because_found_cluster_energy(self,all_energies_of_offpsring):
				finish_because_found_cluster_energy = True
				break
		############################################################################################################################
		if os.path.exists('finish'):
			print('Finishing by finding a "finish" file')
		elif self.timer.has_elapsed_time():
			print('Finishing by going over the elapsed time')
		elif finish_because_found_cluster_energy:
			print('Finishing by finding the energy of the desired LES cluster')
		elif generation_number == self.generations:
			print("----------------------------------------------------------")
			print("----------------------------------------------------------")
			print('The maximum generation set by the user has been reached! The genetic algorithm process has completed!')
			print('The Algorithm will finish now.')
		elif generation_number > self.generations:
			print('Error in def run_GA in class GA_Program, in GAProgram.py')
			print('The number of generations completed is more than what the user has set.')
			print('Current generation number: '+str(generation_number))
			print('Maximum Generation for this GA run: '+str(self.generations))
			print('Check this.')
			import pdb; pdb.set_trace()
			exit()
		#self.ga_recording_system.write_GA_Recording_Database_at_End_of_GA()
		#if not (os.path.exists('finish') or finish_because_found_cluster_energy):
		#	self.remove_cluster_files()
		#self.offspring_pool.close_offspring_pool()
		print("----------------------------------------------------------")
		print('Time elapsed: '+str(self.timer.print_elapsed_time()))
		print('Date and Time: '+str(self.timer.get_time_now()))
		print("----------------------------------------------------------")
		print('Finishing the Garden Group Genetic Algorithm Successfully.')
		print("----------------------------------------------------------")
		print("----------------------------------------------------------")

	#########################################################################################################################
	#########################################################################################################################

	#----------------------------------------------------------------------------#
	#                          Offspring Creation Step                           #
	#            Will create all the clusters desired per generation.            #
	#                   Has been set up for parallelisation.                     #
	#----------------------------------------------------------------------------#

	def get_offsprings(self,previous_cluster_name,generation_number):
		tasks = self.get_tasks(previous_cluster_name,generation_number)
		print('-----------------------')
		print('Making Offspring')
		#print("Made Offspring: ", end = '')
		start_time = time()
		if self.no_of_cpus == 1:
			offsprings = []
			for task in tasks:
				offspring, toString = Create_An_Offspring(task)
				offsprings.append((offspring, toString))
		else:
			with mp.Pool(processes=self.no_of_cpus) as pool: # pool = mp.Pool()
				results = pool.map_async(Create_An_Offspring, tasks)
				results.wait()
			offsprings = results.get()
		end_time = time()
		print('-----------------------')
		print('Time taken to make offspring: '+str(end_time-start_time)+' s.')
		start_time = time()
		if self.print_details:
			print('Details of created offsprings')
		for cluster, toString in offsprings:
			if not toString == '':
				print(toString)
			self.offspring_pool.add('End',cluster) # Place the initialised cluster into the population
		end_time = time()
		print('Time taken to add offspring to Offspring_Pool: '+str(end_time-start_time)+' s.')
		print('-----------------------')
		return self.offspring_pool[-1].name

	def get_tasks(self,previous_cluster_name,generation_number):
		"""
		This provides a generator that contains the inputs needed to create the offspring via parallelisation.
		"""
		def tasks(previous_cluster_name,generation_number,population,offspring_pool_name,chance_of_mutation,r_ij,cell_length,vacuum_to_add_length,creating_offspring_mode,crossover_procedure,mutation_procedure,no_offspring_per_generation,rounding_criteria,Minimisation_Function,surface,place_cluster_where,print_details):
			run_numbers = range(previous_cluster_name+1,previous_cluster_name+self.no_offspring_per_generation+1)
			for run_number in run_numbers:
				yield (run_number,generation_number,population,offspring_pool_name,chance_of_mutation,r_ij,cell_length,vacuum_to_add_length,creating_offspring_mode,crossover_procedure,mutation_procedure,no_offspring_per_generation,rounding_criteria,Minimisation_Function,surface,place_cluster_where,print_details)
		return tasks(previous_cluster_name,generation_number,self.population,self.offspring_pool_name,self.chance_of_mutation,self.r_ij,self.cell_length,self.vacuum_to_add_length,self.creating_offspring_mode,self.crossover_procedure,self.mutation_procedure,self.no_offspring_per_generation,self.rounding_criteria,self.Minimisation_Function,self.surface,self.place_cluster_where,self.print_details)

	#########################################################################################################################
	#########################################################################################################################

	#----------------------------------------------------------------------------#
	#                           Natural Selection Step                           #
	#     Replace clusters in the population with any lower energy offspring.    #
	#----------------------------------------------------------------------------#

	def natural_selection(self,offspring_pool,generation_number):
		"""
		This definition allows the genetic algorithm to perform the natural selection proceedure.

		The algorithm works as follows:

			 - The fitness of the population and the offspring are assessed.
			 - The clusters in the population are ordered from lowest to highest fitness.
			 - The offspring are ordered from highest to lowest fitness.
			 - Replace the clusters in the population with the lowest fitnesses with the offspring with the highest fitnesses.
			 - Once done, the Natural Selection Proceedure is finished.

		:param generation_number: This is the current generation of the genetic algorithm run. This mauy not be 0 if you are restarting the algorithm
		:type  generation_number: int
		:param offspring_pool: This is the offspring pool the GA will be using.
		:type  offspring_pool: Offspring

		This Natural Selection proceedure will update self.population

		"""
		if self.print_details:
			print("-----------------------------")
			print("****---------------------****")
			print("Natural Selection for Generation " + str(generation_number))
			print(self.population.information())
			print(offspring_pool.information())
		# Obtain a list of clusters in order of lowest to highest energy for clusters in the Pool
		fitness_population = []
		for index in range(len(self.population)):
			individual = self.population[index]
			fitness_population.append([individual.fitness,index,individual.name])
		fitness_population.sort(key=lambda x:x[0])
		offspring_pool.sort_by_fitness()
		# take a note of all the clusters in the population that have been removed due to being less fit than an offspring
		clusters_removed_from_the_population = []
		# swap offspring with individuals in the population.
		index_fp = 0
		if self.print_details:
			print('Offspring that replace clusters in population due to fitness.')
		while len(offspring_pool) > 0:
			if offspring_pool[0].fitness < fitness_population[index_fp][0]:
				break
			else:
				offspring = offspring_pool.pop(0)
				index_rc = fitness_population[index_fp][1]
				clusters_removed_from_the_population.append(self.population[index_rc].name)
				if self.print_details:
					print('Replacing Cluster '+str(self.population[index_rc].name)+'(fitness = '+str(floor_float(self.population[index_rc].fitness,3))+') with Offspring '+str(offspring.name)+'(fitness = '+str(floor_float(offspring.fitness,3))+')')
				self.population.replace(index_rc,offspring)
			index_fp += 1
		if self.print_details:
			print("****---------------------****")
		return clusters_removed_from_the_population

	#########################################################################################################################
	#########################################################################################################################