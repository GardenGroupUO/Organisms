
def dot(v1, v2):
	return sum(x*y for x,y in zip(v1,v2))

from abc import ABC, abstractmethod
class Fitness_Operator(ABC):
	"""
	The Fitness class is designed to determine and assign the appropriate fitness value to clusters created during the genetic algorithm. 
	This class can be thought as an extension of the predation Operator. This class contains all the appropriate steps that are needed for 
	the fitnesses to be efficiency assigned to created clusters. 

	There are only two methods that need to be written for the predation Operator that is to be used. These are:
		* assign_population_fitnesses
		* assign_all_fitnesses

	Note: This class is intended to work as an interface only. Refer to the instruction manual as to how to use this interface to build your own predation Operator.

	:param fitness_information: The informatino needed by the Fitness_Operator
	:type  fitness_information: dict.
	:param population: The population to assign fitnesses to
	:type population: Organisms.GA.Population
	:param print_details: Print the details of the energy fitness operator. True if yes, False if no
	:type  print_details: bool
	"""
	def __init__(self, fitness_information, population, print_details):
		self.fitness_switch = fitness_information['Fitness Operator']
		self.fitness_information = fitness_information
		self.population = population
		self.print_details = print_details
		self.check()

	def check(self):
		"""
		This method will check that the self.fitness_switch is an available fitness operator. 
		"""
		if not self.fitness_switch in ['Energy','SCM + Energy']:
			error_string =  'Error in choosing Fitness Operators.\n'
			error_string += 'Predation_Operator must be either:\n'
			error_string += '\t"Energy" - The fitness of a cluster is based on its energy only.\n'
			error_string += '\t"SCM + Energy" - The fitness of a cluster is based on its energy and structural diversity as determined by the SCM.\n'
			error_string += 'Check this.\n'
			error_string += 'Fitness Operator = ' + str(fitness_switch)+'\n'
			#import pdb, traceback, sys
			#extype, value, tb = sys.exc_info()
			#traceback.print_exc()
			#pdb.post_mortem(tb)
			print(error_string,file=sys.stderr)
			import pdb; pdb.set_trace()
			exit()

	def __repr__(self):
		return str(self.__dict__)

	@abstractmethod
	def assign_initial_population_fitnesses(self):
		"""
		This method is designed to assign fitness values to the clusters of the population only at the start of the GA, when the population has been initialised

		This is an abstract method. 
		If you write your own diversiy and fitness classes, you MUST write something for this method.
		
		"""
		pass

	@abstractmethod
	def assign_resumed_population_fitnesses(self,resume_from_generation): 
		"""
		This method is designed to assign fitness values to the clusters of the population only at the beginning of a resumed GA. 

		This is an abstract method. 
		If you write your own diversiy and fitness classes, you MUST write something for this method.

		:param resume_from_generation: The current generation to resume from.
		:type  resume_from_generation: int
		
		"""
		pass

	@abstractmethod
	def assign_all_fitnesses_before_assess_against_predation_operator(self,all_offspring_pools,current_generation_no):
		"""
		This method is to be used in the GA program. 
		This will assign all the fitnesses of all clusters in the current generation (population and offspring) before the offspring are assessed to understand if they violate the predation scheme (i.e. an offspring is Class 1 similar to a cluster in the population, or another offspring).

		See the description given for the "assign_all_fitnesses" def on what the crux of this method is.

		If you write your own diversiy and fitness classes, you do not need to implement this method in your fitness class.

		:param all_offspring_pools: All of the offspring_pools
		:type  all_offspring_pools: list of Organisms.GA.Offspring_Pool
		:param current_generation_no: The current generation
		:type  current_generation_no: int
		"""
		pass

	@abstractmethod
	def assign_all_fitnesses_after_assess_against_predation_operator(self,all_offspring_pools,current_generation_no, offspring_to_remove):
		"""
		This method is to be used in the GA program. 
		This will assign all the fitnesses of all clusters in the current generation (population and offspring) after the offspring are assessed to understand if they violate the predation scheme (i.e. an offspring is Class 1 similar to a cluster in the population, or another offspring).

		See the description given for the "assign_all_fitnesses" def on what the crux of this method is.

		If you write your own diversiy and fitness classes, you do not need to implement this method in your fitness class.

		:param all_offspring_pools: All of the offspring_pools
		:type  all_offspring_pools: list of Organisms.GA.Offspring_Pool
		:param current_generation_no: The current generation
		:type  current_generation_no: int
		:param offspring_to_remove: a list of all the names of clusters in the offspring that will be removed.
		:type  offspring_to_remove: list of int
		"""
		pass

	@abstractmethod
	def assign_all_fitnesses_after_natural_selection(self,current_generation_no):
		"""
		This method is to be used in the GA program. 
		This will assign all the fitnesses to all the clusters in the population before the offspring are assessed to understand if they violate the predation operator (i.e. an offspring is Class 1 similar to a cluster in the population, or another offspring).

		See the description given for the "assign_population_fitnesses" def on what the crux of this method is.

		If you write your own diversiy and fitness classes, you do not need to implement this method in your fitness class.

		:param current_generation_no: The current generation
		:type  current_generation_no: int
		"""
		pass
