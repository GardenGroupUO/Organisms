from Organisms.GA.SCM_Scripts.SCM_initialisation import get_rCuts, get_SCM_methods
from Organisms.GA.SCM_Scripts.CNA_Database import CNA_Database

from Organisms.GA.Fitness_Operators.CNA_Database_Check import CNA_Database_Check
from Organisms.GA.Fitness_Operators.Fitness_Function import Fitness_Function

from Organisms.GA.Fitness_Operators.CNA_Fitness_Contribution import get_CNA_fitness_contribution, get_CNA_fitness_contribution_normalised, mean

def SCM_options(self,fitness_information, predation_operator, no_of_cpus):
	"""
	This method records the information from the predation_operator that is relavant to the fitness class rather than the needed to obtain the predation operator class, and make a link to the similarity profile database, containing the similarity plots of every cluster against every other cluster for the current generation,

	:param fitness_information: This is all the information that is needed about the fitness class
	:type  fitness_information: dict.
	:param predation_operator: This is the predation operator that this fitness class will take information from if needed to obtain a fitness.
	:type  predation_operator: Organisms.GA.Predation_Operator
	:param no_of_cpus: the number of cpus to use when multiprocessing
	:type  no_of_cpus: int

	"""
	self.predation_switch = predation_operator.Predation_Switch
	if not ('SCM Scheme' in fitness_information) and not (fitness_information['SCM Scheme'] in ['T-SCM','A-SCM']):
		print('ERROR in def SCM_options, in Class SCM_and_Energy_Fitness_Operator, in SCM_and_Energy_Fitness_Operator.py/SCM_and_Energy_Fitness_Operator_Options.py')
		print('You either need to include the "SCM Scheme" setting, or you have entered an invalid entry for "SCM Scheme" setting in the fitness_information dictionary.')
		print('The "SCM Scheme" setting can be either the T-SCM or the A-SCM.')
		print('Your fitness_information dictionary is: '+str(fitness_information))
		print('Check this.')
		exit('This program will finish without completing.')
	# --------------------------------------------------- #
	# Settings for the 'Use Predation Information' setting
	# The end result of this is to set up the cna_database.
	will_make_new_cna_database = CNA_Database_Check(self,fitness_information, predation_operator)
	if will_make_new_cna_database:
		self.cna_database = make_new_cna_database(self, fitness_information, no_of_cpus)
	# --------------------------------------------------- #
	# Get the other variable for the SCM + energy fitness operator from the fitness_information dictionary.
	self.fitness_switch = fitness_information['Fitness Operator']
	self.SCM_fitness_contribution = fitness_information['SCM_fitness_contribution']
	self.dynamic_mode = fitness_information['Dynamic Mode']
	# --------------------------------------------------- #
	# Get the fitness contributions
	self.energy_fitness_contribution = 1.0 - self.SCM_fitness_contribution
	self.fitness_weights = []
	if not self.energy_fitness_contribution == 0.0:
		self.fitness_weights.append(self.energy_fitness_contribution)
	if not self.SCM_fitness_contribution == 0.0:
		self.fitness_weights.append(self.SCM_fitness_contribution)
	# Double check the fitness_contributions add up to 1
	if not sum(self.fitness_weights) == 1.0:
		print('Error in def get_fitness of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
		print('The sum of the coefficients of the linear superposition (sorry cant remember the right word right now) does not equal 1.')
		print('Coefficients: '+str(self.fitness_weights))
		print('sum(fitness_weights) = '+str(sum(self.fitness_weights)))
		print('Check this.')
		import pdb; pdb.set_trace()
		exit('This program will finish without completing')
	# --------------------------------------------------- #
	# Determine how the collection of sigma values between cluster x and every other cluster in the population (including offspring.)
	if 'Take from the collection of a clusters similarities' in fitness_information:
		self.take_for_clusters_similarities = fitness_information['Take from the collection of a clusters similarities']
	else:
		self.take_for_clusters_similarities = 'Maximum'
	if self.take_for_clusters_similarities == 'Maximum':
		self.collection_function = max
	elif self.take_for_clusters_similarities == 'Average':
		self.collection_function = mean
	else:
		print('Error in def get_fitness of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
		print('You have not supplied a valid input for "Take from the collection of a clusters similarities"')
		print('"Take from the collection of a clusters similarities" can only be either "Maximum" or "Average"')
		print('You input for "Take from the collection of a clusters similarities": '+str(self.take_for_clusters_similarities))
		print('Check this.')
		exit('This program will finish without completing')
	# --------------------------------------------------- #
	# Determine if the similarities used to obtain the structure + energy fitness operator are normalised or not
	if 'normalise_similarities' in fitness_information:
		self.normalise_similarities = fitness_information['normalise_similarities']
	else:
		self.normalise_similarities = False
	if self.normalise_similarities:
		self.get_CNA_fitness_contribution = get_CNA_fitness_contribution_normalised
	else:
		self.get_CNA_fitness_contribution = get_CNA_fitness_contribution
	# --------------------------------------------------- #
	# fitness functions
	self.energy_fitness_function = Fitness_Function(**fitness_information['energy_fitness_function'])
	self.cna_fitness_function    = Fitness_Function(**fitness_information['SCM_fitness_function'])
	if self.dynamic_mode:
		self.population_fitness_function = Fitness_Function(**fitness_information['fitness_function'])
	# --------------------------------------------------- #

def make_new_cna_database(self, fitness_information, no_of_cpus):
	"""
	Reset the CNA database

	:param fitness_information: This is all the information that is needed about the fitness class
	:type  fitness_information: dict.
	:param no_of_cpus: the number of cpus to use when multiprocessing
	:type  no_of_cpus: int

	:returns: return a CNA_Database object
	:rtype:   Organisms.GA.SCM_Scripts.CNA_Database
	"""
	SCM_Scheme = fitness_information['SCM Scheme']
	rCuts = get_rCuts(self,fitness_information)
	get_cna_profile_method, get_cna_similarities_method = get_SCM_methods(SCM_Scheme)
	try:
		cut_off_similarity = predation_Information['Cut_off']
	except:
		cut_off_similarity = 100.0
	debug = False
	return CNA_Database(rCuts,self.population,cut_off_similarity,get_cna_profile_method,get_cna_similarities_method,no_of_cpus,debug)
