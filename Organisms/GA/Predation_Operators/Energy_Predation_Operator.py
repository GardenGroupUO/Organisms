'''
Eenrgy_Predation_Operator.py, Geoffrey Weal, 28/10/2018

This is one of the Predation Operators that can be used by the genetic algorithm program. 

'''

from Organisms.GA.Predation_Operators.Predation_Operator import Predation_Operator

class Energy_Predation_Operator(Predation_Operator):
	"""
	This is one of the Predation Operators that can be used by the genetic algorithm program. 

	This class will allow the genetic algorithm to procedure without any Predation Operator. Instead, this class provide a way to use
	the energetic fitness to obtain a fitness for each cluster. This Operator will not remove any clusters from the population or 
	the offspring pool.

	:param Predation_Information: This contains all the information needed by the Predation Operator you want to use to run.
	:type  Predation_Information: dict.
	:param population: This is the population that this Operator will be controlling to make sure that no two clusters in the population have the same energy.
	:type  population: Organisms.GA.Population
	:param print_details: Print details of the predation operator, like verbose
	:type  print_details: bool

	"""
	def __init__(self,predation_information,population,print_details):
		super().__init__(predation_information,population,print_details)
		self.Energy_Predation_Operators_Options(predation_information)
		self.get_energy_predation_methods()

	def Energy_Predation_Operators_Options(self,predation_information):
		"""
		This method is designed to add and check the options that you have placed in to 
		the predation_information dictionary for the Energy Predation Operator

		:param predation_information: This contains all the information needed by the Predation Operator you want to use to run.
		:type  predation_information: dict.

		"""
		if not predation_information['Predation Operator'] == 'Energy':
			print('Error in class Energy_Predation_Operator, in Energy_Predation_Operator.py')
			print('The Predation Operator "Energy_Predation_Operator" has been initialised.')
			print("However, predation_information['Predation_Operator'] is not 'Energy'")
			print("predation_information['Predation_Operator'] = "+str(predation_information['Predation_Operator']))
			print('Check this out.')
			import pdb; pdb.set_trace()
			exit('This program will exit without completing.')
		try:
			self.mode = predation_information['mode']
		except:
			print('Error in class Energy_Predation_Operator, in Energy_Predation_Operator.py')
			print("You need to include a 'mode' in your predation_information dictionary.")
			print("This should be either 'simple' or 'comprehensive'.")
			print('Do this and repeat this algorithm.')
			print('The GA Program will end.')
			exit('This program will exit without completing.')
		############################################################
		if self.mode == 'simple':
			try:
				self.round_energy = int(predation_information['round_energy'])
			except ValueError:
				print('Error in class Energy_Predation_Operator, in Energy_Predation_Operator.py')
				print("predation_information input 'round_energy' but be intergerable.")
				print("predation_information['round_energy'] = "+str(predation_information['round_energy']))
				print('Do this and repeat this algorithm.')
				print('The GA Program will end.')
				exit('This program will exit without completing.')
			except:
				print('Error in class Energy_Predation_Operator, in Energy_Predation_Operator.py')
				print("You need to set a 'round_energy' in to your predation_information variable in your Run.py (or MakeTrial.py) file, as you have set mode = 'simple'.")
				print("E.g. predation_information['round_energy'] = 2")
				print('Do this and repeat this algorithm.')
				print('The GA Program will end.')
				exit('This program will exit without completing.')
			try:
				predation_information['minimum_energy_diff']
				print("Ignoring your 'minimum_energy_diff' input variable for the Energy Predation Operator")
				del predation_information['minimum_energy_diff']
			except:
				pass
		elif self.mode == 'comprehensive':
			try:
				self.type_of_comprehensive_scheme = predation_information['type_of_comprehensive_scheme']
			except:
				print('Error in class Energy_Predation_Operator, in Energy_Predation_Operator.py')
				print("You need to set a 'type_of_comprehensive_scheme' in to your predation_information variable in your Run.py (or MakeTrial.py) file, as you have set mode = 'comprehensive'.")
				print("E.g. predation_information['type_of_comprehensive_scheme'] = 'energy' or predation_information['type_of_comprehensive_scheme'] = 'fitness'")
				print('Do this and repeat this algorithm.')
				print('The GA Program will end.')
				exit('This program will exit without completing.')

			try:
				self.minimum_energy_diff = predation_information['minimum_energy_diff']
			except ValueError:
				print('Error in class Energy_Predation_Operator, in Energy_Predation_Operator.py')
				print("predation_information input 'minimum_energy_diff' but be floatable.")
				print("predation_information['minimum_energy_diff'] = "+str(predation_information['minimum_energy_diff']))
				print('Do this and repeat this algorithm.')
				print('The GA Program will end.')
				exit('This program will exit without completing.')
			except:
				print('Error in class Energy_Predation_Operator, in Energy_Predation_Operator.py')
				print("You need to set a 'minimum_energy_diff' in to your predation_information variable in your Run.py (or MakeTrial.py) file, as you have set mode = 'comprehensive'.")
				print("E.g. predation_information['minimum_energy_diff'] = 0.005 #eV")
				print('Do this and repeat this algorithm.')
				print('The GA Program will end.')
				exit('This program will exit without completing.')
			try:
				predation_information['round_energy']
				print("Ignoring your 'round_energy' input variable for the Energy Predation Operator")
				del predation_information['round_energy']
			except:
				pass
		else:
			print('Error in class Energy_Predation_Operator, in Energy_Predation_Operator.py')
			print("The variable 'mode' in your predation_information dictionary should be either 'simple' or 'comprehensive'.")
			print('Do this and repeat this algorithm.')
			print('The GA Program will end.')
			exit('This program will exit without completing.')
		############################################################

	def get_energy_predation_methods(self):
		"""
		This method is designed to import the methods needed to run this Predation Operator, using with the 'simple' or 'comprehensive' mode.
		"""
		if self.mode == 'simple':
			from Organisms.GA.Predation_Operators.Energy_Predation_Operator_Scripts.Simple_Energy_Predation_Scheme import check_initial_population, assess_for_violations
		elif self.mode == 'comprehensive':
			if self.type_of_comprehensive_scheme == 'energy':
				from Organisms.GA.Predation_Operators.Energy_Predation_Operator_Scripts.Comprehensive_Energy_Predation_Operator_energy  import check_initial_population, assess_for_violations_force_replacement, assess_for_violations_no_force_replacement
			elif self.type_of_comprehensive_scheme == 'fitness':
				from Organisms.GA.Predation_Operators.Energy_Predation_Operator_Scripts.Comprehensive_Energy_Predation_Operator_fitness import check_initial_population, assess_for_violations_force_replacement, assess_for_violations_no_force_replacement
			else:
				print('Error in def get_energy_predation_methods, in class Energy_Predation_Operator, in Energy_Predation_Operator.py')
				print('self.type_of_comprehensive_scheme must be either "energy" or "fitness".')
				print('Currently, self.type_of_comprehensive_scheme = '+str(self.type_of_comprehensive_scheme))
				print('Check this and change as appropriate.')
				exit('This program will exit without completing.')
		self.check_initial_population_imported = check_initial_population
		self.assess_for_violations_force_replacement_imported = assess_for_violations_force_replacement
		self.assess_for_violations_no_force_replacement_imported = assess_for_violations_no_force_replacement
		############################################################
			
	def check_initial_population(self,return_report=False):
		"""
		This definition is responsible for making sure that the initialised population obeys the Predation Operator of interest.

		:param return_report: Will return a dict with all the information about what clusters are similar to what other clusters in the population. 
		:type  return_report: bool.

		returns:
			* **clusters_to_remove** (*list of ints*): a list of the clusters to remove from the population as they violate the Predation Operator. Format is [(index in population, name fo cluster),...]
			* **CNA_report** (*dict.*): a dictionary with information on the clusters being removed and the other clusters in the population which have caused the violation to the SCM Predation Operator. This information is only used to display information so they know why there are violations to the Predation Operator when they occur. For is {removed cluster: [list of clusters that this cluster is similar to in the population.]}

		"""
		return self.check_initial_population_imported(self, return_report)

	def assess_for_violations(self,offspring_pool,force_replace_pop_clusters_with_offspring):
		"""
		This definition is designed to determine which offspring (and the clusters in the population) violate the predation Operator. 
		It will not remove or change any clusters in the offspring or population, but instead will record which offspring violate the 
		predation Operator. 

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
		if force_replace_pop_clusters_with_offspring:
			return self.assess_for_violations_force_replacement_imported(self, offspring_pool)
		else:
			return self.assess_for_violations_no_force_replacement_imported(self, offspring_pool)

	########################################################################################################
	########################################################################################################
	########################################################################################################

	def add_to_database(self, collection):
		'''
		Add clusters similarities to the CNA database to be stored for future generations. 

		:param collection: update the fitnesses of clusters in the collection.
		:type  collection: Organisms.GA.Collection.Collection
		'''
		pass

	def remove_from_database(self, cluster_names_to_remove):
		'''
		Clusters to remove from the CNA database

		:param cluster_names_to_remove: A list of the names of all the clusters to remove from the CNA database
		:type  cluster_names_to_remove: list of ints
		'''
		pass

	def reset(self):
		'''
		Reset the CNA database with no inputs
		'''
		pass