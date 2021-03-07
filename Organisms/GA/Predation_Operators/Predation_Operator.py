import sys
from abc import ABC, abstractmethod

class Predation_Operator(ABC):
	"""
	This is an abstract class to act as the skeleton of the Predation_Operator class.

	:param Predation_Information: This contains all the information needed by the Predation Operator you want to use to run.
	:type  Predation_Information: dict.
	:param population: This is the population that this Operator will be controlling to make sure that no two clusters in the population have the same energy.
	:type  population: Organisms.GA.Population
	:param print_details: Print details of the predation operator, like verbose
	:type  print_details: bool

	"""
	def __init__(self,predation_information, population, print_details):
		self.predation_information = predation_information
		self.Predation_Switch = predation_information['Predation Operator']
		self.population = population
		self.print_details = print_details
		self.check()

	def check(self):
		"""
		This method will check to make sure that the predation operator is available.
		"""
		if not self.Predation_Switch in ['Off','Energy','IDCM','SCM']:
			error_string =  'Error in Predation_Operator, in __init__ definition.\n'
			error_string += 'Predation_Operator must be either:'
			error_string += '\t"Off" - No Predation Operator is used.\n'
			error_string += '\t"Energy" - Based on no two clusters can have the same energy in the population.\n'
			error_string += '\t"IDCM" - Based on no two clusters can be structurally identical in the population based on the comparison of those two structuress EDM\'. See Manual for more information.\n'
			error_string += '\t"SCM" - No two structures can be Geometrically Similar based on the Structral Comarison Method. See Manual for more information.\n'
			error_string += 'Check this.\n'
			error_string += 'Predation_Operator = ' + str(self.Predation_Switch)+'\n'
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
	def check_initial_population(self,return_report=False):
		"""
		This definition is responsible for making sure that the initialised population obeys the Predation Operator of interest.

		:param return_report: Will return a dict with all the information about what clusters are similar to what other clusters in the population. 
		:type  return_report: bool.

		returns:
			* **clusters_to_remove** (*list of ints*): a list of the clusters to remove from the population as they violate the Predation Operator. Format is [(index in population, name fo cluster),...]
			* **CNA_report** (*dict.*): a dictionary with information on the clusters being removed and the other clusters in the population which have caused the violation to the SCM Predation Operator. This information is only used to display information so they know why there are violations to the Predation Operator when they occur. For is {removed cluster: [list of clusters that this cluster is similar to in the population.]}
		
		"""
		pass

	@abstractmethod
	def assess_for_violations(self,offspring_pool,force_replace_pop_clusters_with_offspring):
		"""
		This definition is designed to determine which offspring (and the clusters in the population) violate the Predation Operator. 
		It will not remove or change any clusters in the offspring or population, but instead will record which offspring violate the 
		Predation Operator. 

		It will also recommend which clusters in the population should be removed and be replaced by which offspring prior to the 
		natural selection process. Here, the cluster in the population and the offspring will be in violation of each other, however it 
		may be advantageous to keep the offspring rather than the cluster in the population as the offspring is fitter than the cluster
		in the offspring

		:param offspring_pool: This is the collection of offspring to assess for violations to the Predation Operator.
		:type  offspring_pool: Organisms.GA.Offspring_Pool.Offspring_Pool
		:param force_replace_pop_clusters_with_offspring: This will tell the genetic algorithm whether to swap clusters in the population with offspring if the predation operator indicates they are the same but the predation operator has a better fitness value than the cluster in the population. 
		:type  force_replace_pop_clusters_with_offspring: bool.

		returns:
			* **offspring_to_remove** (*tuple of ints*): A list of the names of the offspring to be removed
			* **force_replacement** (*tuple of (int, int)*): A list of the clusters in the population that should be replaced, and the offspring they should be replaced by.

		"""
		pass

	@abstractmethod
	def add_to_database(self, collection):
		'''
		Add clusters similarities to the CNA database to be stored for future generations. 

		:param collection: update the fitnesses of clusters in the collection.
		:type  collection: Organisms.GA.Collection.Collection
		'''
		pass

	@abstractmethod
	def remove_from_database(self, cluster_names_to_remove):
		'''
		Clusters to remove from the CNA database

		:param cluster_names_to_remove: A list of the names of all the clusters to remove from the CNA database
		:type  cluster_names_to_remove: list of ints
		'''
		pass

	@abstractmethod
	def reset(self):
		'''
		Reset the CNA database with no inputs
		'''
		pass

	def remove_offspring_and_replace_with_population_that_violate_predation_operator(self, population, offspring_pool, offspring_to_remove, population_to_be_replaced_by_offspring):
		"""
		This method will remove similar offspring in the offspring_pool, and replace any offspring with clusters in the population (if desired).

		:param population: This is the population.
		:type  population: Organisms.GA.Population.Population
		:param offspring_pool: This is all the offspring.
		:type  offspring_pool: Organisms.GA.Offspring_Pool.Offspring_Pool
		:param offspring_to_remove: These are all the offspring to remove from the offspring_pool. 
		:type  offspring_to_remove: list of int
		:param population_to_be_replaced_by_offspring: These are the names of the clusters in the population to be replaced by offspring in the offspring_pool. This is a list of (name of cluster in population to be replaced, name of offsring to replaced that cluster). 
		:type  population_to_be_replaced_by_offspring: list of (int, int)

		"""
		# Remove offspring that violate the predation Operator
		self.remove_offspring_that_violate_the_predation_operator(offspring_pool, offspring_to_remove)
		# Replace clusters in the population with offspring to comply with the predation Operator.
		self.replace_population_with_offspring(population, offspring_pool, population_to_be_replaced_by_offspring)
		#import pdb; pdb.set_trace()

	def remove_offspring_that_violate_the_predation_operator(self,offspring_pool,offspring_to_remove):
		"""
		Remove offspring from the Offspring_Pool

		:param offspring_pool: This is all the offspring.
		:type  offspring_pool: Organisms.GA.Offspring_Pool.Offspring_Pool
		:param offspring_to_remove: These are all the offspring to remove from the offspring_pool. 
		:type  offspring_to_remove: list of int

		"""
		offspring_to_remove.sort(key=lambda x:x[1],reverse=True)
		for offspring_name, offspring_index in offspring_to_remove:
			del offspring_pool[offspring_index]

	def replace_population_with_offspring(self, population, offspring_pool, population_to_be_replaced_by_offspring):
		"""
		Replace clusters in the population with offspring in the offspring_pool. These population clusters are replaced by similar offspring that have higher fitnesses than the offspring in the Offspring_Pool.
		
		:param population: This is the population.
		:type  population: Organisms.GA.Population.Population
		:param offspring_pool: This is all the offspring.
		:type  offspring_pool: Organisms.GA.Offspring_Pool.Offspring_Pool
		:param population_to_be_replaced_by_offspring: These are the names of the clusters in the population to be replaced by offspring in the offspring_pool. This is a list of (name of cluster in population to be replaced, name of offsring to replaced that cluster). 
		:type  population_to_be_replaced_by_offspring: list of (int, int)

		"""
		population_to_be_replaced_by_offspring.sort(key=lambda x:x[1],reverse=True) # not needed if the population_to_be_replaced_by_offspring list has already been sorted beforehand.
		for pop_cluster_name, offspring_name in population_to_be_replaced_by_offspring:
			pop_to_swap_out_index = population.get_index(pop_cluster_name)
			off_to_swap_in_index = offspring_pool.get_index(offspring_name)
			offspring = offspring_pool.pop(off_to_swap_in_index)
			population.replace(pop_to_swap_out_index, offspring)

