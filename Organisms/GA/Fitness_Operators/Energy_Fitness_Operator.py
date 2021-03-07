from Organisms.GA.Fitness_Operators.Fitness_Operator import Fitness_Operator
from Organisms.GA.Fitness_Operators.Fitness_Function import Fitness_Function
from Organisms.GA.Fitness_Operators.Energetic_Fitness_Contribution import get_lowest_and_highest_energies_from_collections, get_energetic_fitness_contribution

class Energy_Fitness_Operator(Fitness_Operator):
	"""
	The Fitness class is designed to determine and assign the appropriate fitness value to clusters created during the genetic algorithm. 
	The fitnesses are based on the energies of the clusters in the offspring and the population. 

	There are only two methods that need to be written for the predation operator that is to be used. These are:
		* assign_population_fitnesses
		* assign_all_fitnesses

	:param fitness_information: This is all the information that is needed about the fitness class
	:type fitness_information: dict.
	:param predation_operator: This is the predation operator that this fitness class will take information from if needed to obtain a fitness.
	:type  predation_operator: Organisms.GA.Predation_Operator
	:param population: The population to assign fitnesses to
	:type population: Organisms.GA.Population
	:param print_details: Print the details of the energy fitness operator. True if yes, False if no
	:type  print_details: bool

	"""
	def __init__(self, fitness_information, predation_operator, population, print_details):
		super().__init__(fitness_information, population, print_details)
		self.energy_fitness_options(fitness_information, predation_operator)

	def energy_fitness_options(self, fitness_information, predation_operator):
		"""
		This method is designed to set the variables requires for this fitness.

		:param fitness_information: This is all the information that is needed about the fitness class
		:type fitness_information: dict.
		:param predation_operator: This is the predation operator that this fitness class will take information from if needed to obtain a fitness.
		:type  predation_operator: Organisms.GA.Predation_Operator
		
		"""
		#self.predation_switch = predation_operator.Predation_Switch

		self.fitness_switch = fitness_information['Fitness Operator']
		#self.use_predation_information = fitness_information['Use Predation Information']

		self.previous_max_energy = -float('inf')
		self.previous_min_energy = float('inf')
		self.energy_fitness_function = Fitness_Function(**fitness_information['fitness_function'])

	####################################################################################
	################## Method for assign_initial_population_fitnesses ##################
	####################################################################################

	def assign_initial_population_fitnesses(self):
		"""
		This method is designed to assign fitness values to the clusters of the population only at the start of the GA, when the population has been initialised

		"""
		self.__assign_population_fitnesses(0)

	####################################################################################
	################## Method for assign_resumed_population_fitnesses ##################
	####################################################################################

	def assign_resumed_population_fitnesses(self,resume_from_generation): 
		"""
		This method is designed to assign fitness values to the clusters of the population only at the beginning of a resumed GA. 

		:param resume_from_generation: The current generation to resume from.
		:type  resume_from_generation: int
		
		"""
		self.__assign_population_fitnesses(resume_from_generation)

	############################################################################################################
	################## Method for assign_all_fitnesses_before_assess_against_predation_operator ##################
	############################################################################################################

	def assign_all_fitnesses_before_assess_against_predation_operator(self,all_offspring_pools,current_generation_no):
		"""
		This method is to be used in the GA program. 
		This will assign all the fitnesses of all clusters in the current generation (population and offspring) before the offspring are assessed to understand if they violate the predation operator (i.e. an offspring is Class 1 similar to a cluster in the population, or another offspring).

		See the description given for the "assign_all_fitnesses" def on what the crux of this method is.

		If you write your own diversiy and fitness classes, you do not need to implement this method in your fitness class.

		:param all_offspring_pools: list of all the offspring pools of offspring to assign fitness values to.
		:type  all_offspring_pools: list of Organisms.GA.Offspring_Pool
		:param current_generation_no: The current generation
		:type  current_generation_no: int

		"""
		# At this point:
		#	- self.previous_max_energy = -float('inf'), and 
		#	- self.previous_min_energy = float('inf')
		# Meaning that the fitnesses of all clusters in the population, and all the offspring in the all_offspring_pools, will be calculated and assigned to all clusters.
		self.__assign_all_fitnesses(all_offspring_pools)

	###########################################################################################################
	################## Method for assign_all_fitnesses_after_assess_against_predation_operator ##################
	###########################################################################################################

	def assign_all_fitnesses_after_assess_against_predation_operator(self,all_offspring_pools,current_generation_no, offspring_to_remove):
		"""
		This method is to be used in the GA program. 
		This will assign all the fitnesses of all clusters in the current generation (population and offspring) after the offspring are assessed to understand if they violate the predation operator (i.e. an offspring is Class 1 similar to a cluster in the population, or another offspring).

		See the description given for the "assign_all_fitnesses" def on what the crux of this method is.

		If you write your own diversiy and fitness classes, you do not need to implement this method in your fitness class.

		:param all_offspring_pools: All of the offspring_pools
		:type  all_offspring_pools: list of Organisms.GA.Offspring_Pool
		:param current_generation_no: The current generation
		:type  current_generation_no: int
		:param offspring_to_remove: a list of all the names of clusters in the offspring that will be removed.
		:type  offspring_to_remove: list of int

		"""
		# At this point:
		#	- self.previous_max_energy may not be equal to -float('inf'), and 
		#	- self.previous_min_energy may not be equal to float('inf')
		# Meaning that the fitnesses of all clusters in the population, and all the offspring in the all_offspring_pools, may be recalculated if these energy value have changed by removing clusters due to violating the predation operator
		self.__assign_all_fitnesses(all_offspring_pools)

	#############################################################################################
	################## Method for assign_all_fitnesses_after_natural_selection ##################
	#############################################################################################

	def assign_all_fitnesses_after_natural_selection(self,current_generation_no):
		"""
		This method is to be used in the GA program. 
		This will assign all the fitnesses to all the clusters in the population before the offspring are assessed to understand if they violate the predation operator (i.e. an offspring is Class 1 similar to a cluster in the population, or another offspring).

		See the description given for the "assign_population_fitnesses" def on what the crux of this method is.

		If you write your own diversiy and fitness classes, you do not need to implement this method in your fitness class.

		:param current_generation_no: The current generation
		:type  current_generation_no: int

		"""
		# At this point:
		#	- self.previous_max_energy may not be equal to -float('inf'), and 
		#	- self.previous_min_energy may not be equal to float('inf')
		# Meaning that the fitnesses of all clusters in the population, and all the offspring in the all_offspring_pools, may be recalculated if these energy value have changed by removing clusters due to natural selection.
		self.__assign_population_fitnesses(current_generation_no)
		self.previous_max_energy = -float('inf')
		self.previous_min_energy = float('inf')


	#####################################################################################
	################## Subsidiary Methods for the Energy Fitness Class ##################
	#####################################################################################

	def __assign_population_fitnesses(self,current_generation): 
		"""
		This method is designed to assign fitness values to the clusters of the population only. 

		:param current_generation_no: The current generation.
		:type  current_generation_no: int
		
		"""
		min_energy, max_energy = get_lowest_and_highest_energies_from_collections(self.population,None)
		if not ((min_energy == self.previous_min_energy) and (max_energy == self.previous_max_energy)):
			self.__assign_fitnesses_to_clusters_in_collection(self.population, min_energy, max_energy)

	def __assign_all_fitnesses(self,all_offspring_pools): 
		"""
		This method is designed to assign fitness values of the clusters that need to be assigned or reassigned a new fitness value to what it 
		should be between the processes of creating the offspring and the natrual selection processes. 

		:param all_offspring_pools: This has been designed in advance to be able to process all the different offspring pool if ever the genetic algorithm is designed with multiple offspring_pools. Therefore, this is a list of all the offspring_pools created during a single generation.
		:type  all_offspring_pools: [list of offspring_pool]
		:param current_generation_no: The current generation.
		:type  current_generation_no: int

		"""
		if not isinstance(all_offspring_pools,list):
			all_offspring_pools = [all_offspring_pools]
		min_energy, max_energy = get_lowest_and_highest_energies_from_collections(self.population, all_offspring_pools)
		if not ((min_energy == self.previous_min_energy) and (max_energy == self.previous_max_energy)):
			self.__assign_fitnesses_to_clusters_in_collection(self.population, min_energy, max_energy)
			for offspring_pool in all_offspring_pools:
				self.__assign_fitnesses_to_clusters_in_collection(offspring_pool, min_energy, max_energy)
			self.previous_max_energy = max_energy
			self.previous_min_energy = min_energy

			
	def __assign_fitnesses_to_clusters_in_collection(self, collection, min_energy, max_energy):
		"""
		This definition will attach the fitness value associated to each cluster in the collection object provided by the user.

		See `Theoretical study of Cu-Au nanoalloy clusters using a genetic algorithm, Darby et al., 116, 1536 (2002); doi: 10.1063/1.1429658 <http://dx.doi.org/10.1063/1.1429658>`_, page 1538 about this fitness equation, including the definition of max_energy and min_energy.

		:param collection: This is the collection object that we would like to assign.
		:type  collection: Organisms.GA.Collection
		:param min_energy: This is the lowest energy of the current lowest energetic structure across all the collections in the GA (e.g. [population, offspring]).
		:type  min_energy: float
		:param max_energy: This is the highest energy of the current highest energetic structure across all the collections in the GA (e.g. [population, offspring]).
		:type  max_energy: float

		At the end of this method, all the cluster in the collection will have a fitness value attached to them.
		You can see the fitness value that is attahced to a cluster by looking for th "fitness" variable attached to the cluster.

		"""
		for cluster in collection:
			cluster_fitness = get_energetic_fitness_contribution(cluster, max_energy, min_energy, self.energy_fitness_function)
			cluster.fitness = cluster_fitness		

	def add_to_database(self, collection):
		"""
		This method is required by Organisms.GA.Fitness_Operators.Fitness_Operator, but does not do anything

		:param collection: update the fitnesses of clusters in the collection.
		:type  collection: Organisms.GA.Collection.Collection

		"""
		pass

	def remove_from_database(self, cluster_names_to_remove):
		"""
		This method is required by Organisms.GA.Fitness_Operators.Fitness_Operator, but does not do anything.

		:param cluster_names_to_remove: A list of the names of all the clusters to remove from the CNA database
		:type  cluster_names_to_remove: list of ints
		
		"""
		pass

	def reset(self):
		"""
		This method is required by Organisms.GA.Fitness_Operators.Fitness_Operator, but does not do anything
		"""
		return
