'''
No_Predation_Operator.py, Geoffrey Weal, 28/10/2018

This is one of the Predation Operators that can be used by the genetic algorithm program. 

'''

from Organisms.GA.Predation_Operators.Predation_Operator import Predation_Operator

class No_Predation_Operator(Predation_Operator):
	"""
	This is one of the Predation Operators that can be used by the genetic algorithm program. 

	This Predation Operator will not do anything. It is the option to pick if you do not want to remove offspring or clusters from the population due to being energetically or strucutrally similar.

	:param Predation_Information: This contains all the information needed by the Predation Operator you want to use to run.
	:type  Predation_Information: dict.
	:param population: This is the population that this Operator will be controlling to make sure that no two clusters in the population have the same energy.
	:type  population: Organisms.GA.Population
	:param print_details: Print details of the predation operator, like verbose
	:type  print_details: bool

	"""
	def __init__(self,Predation_Information,population,print_details):
		super().__init__(Predation_Information,population,print_details)
		if not Predation_Information['Predation Operator'] == 'Off':
			print('Error in class No_Predation_Operator, in No_Predation_Operator.py')
			print('The Predation Operator "No_Predation_Operator" has been initialised.')
			print("However, Predation_Information['Predation Operator'] is not 'Off''")
			print("Predation_Information['Predation Operator'] = "+str(Predation_Information['Predation_Operator']))
			print('Check this out.')
			import pdb; pdb.set_trace()
			exit()

	###########################################################################################################
	########################## Methods Required for the def check_initial_population ##########################
	###########################################################################################################

	def check_initial_population(self,return_report=False):
		"""
		This definition is responsible for making sure that the initialised population obeys the Energy Predation Operator. 

		Since this 'Operator' does nothing, this def will not do anything. It will report back that it has not removed any cluster

		:param return_report: Will return a dict with all the information about what clusters are similar to what other clusters in the population. 
		:type  return_report: bool.

		returns:
			* **clusters_to_remove** (*list of ints*): a list of the clusters to remove from the population as they violate the Predation Operator. Format is [(index in population, name fo cluster),...]
			* **CNA_report** (*dict.*): a dictionary with information on the clusters being removed and the other clusters in the population which have caused the violation to the SCM Predation Operator. This information is only used to display information so they know why there are violations to the Predation Operator when they occur. For is {removed cluster: [list of clusters that this cluster is similar to in the population.]}
		
		"""
		if return_report:
			return [], {}
		else:
			return []

	########################################################################################################
	########################## Methods Required for the def assess_for_violations ##########################
	########################################################################################################

	def assess_for_violations(self,offspring_pool,force_replace_pop_clusters_with_offspring):
		"""
		This definition is designed to determine which offspring (and the clusters in the population) violate the predation Operator. 
		It will not remove or change any clusters in the offspring or population, but instead will record which offspring violate the 
		predation Operator. 

		Since this 'Operator' does nothing, this def will not do anything. 

		It will return two tuples with nothing in them, as required by this def. 

		:param offspring_pool: This is the collection of offspring to assess for violations to the Predation Operator.
		:type  offspring_pool: Organisms.GA.Offspring_Pool.Offspring_Pool
		:param force_replace_pop_clusters_with_offspring: This will tell the genetic algorithm whether to swap clusters in the population with offspring if the predation operator indicates they are the same but the predation operator has a better fitness value than the cluster in the population. 
		:type  force_replace_pop_clusters_with_offspring: bool.

		returns:
			* **offspring_to_remove** (*tuple of ints*): A list of the names of the offspring to be removed
			* **force_replacement** (*tuple of (int, int)*): A list of the clusters in the population that should be replaced, and the offspring they should be replaced by.

		"""
		return [], []

	########################################################################################################
	########################################################################################################
	########################################################################################################

	def add_to_database(self, collection):
		'''
		Add clusters similarities to the CNA database to be stored for future generations. 

		This does not do anything since this predation method does notthing

		:param collection: update the fitnesses of clusters in the collection.
		:type  collection: Organisms.GA.Collection.Collection
		'''
		pass

	def remove_from_database(self, cluster_names_to_remove):
		'''
		Clusters to remove from the CNA database

		This does not do anything since this predation method does notthing

		:param cluster_names_to_remove: A list of the names of all the clusters to remove from the CNA database
		:type  cluster_names_to_remove: list of ints
		'''
		pass

	def reset(self):
		'''
		Reset the CNA database with no inputs

		This does not do anything since this predation method does notthing
		'''
		pass
