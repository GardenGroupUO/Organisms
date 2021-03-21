import sys

from Organisms.GA.check_version_of_asap3 import check_version_of_asap3

def get_predation_operator(predation_information, fitness_information, population, no_of_cpus, print_details):
	"""
	This def will set up the predation operator to be by the genetic algorithm. This is dependent on the entry for the 'Predation_Switch' 
	given in the predation_information. 

	:param predation_information: All the informatino about the predation operator.
	:type  predation_information: dict.
	:param fitness_information: All the information about the fitness operator
	:type  fitness_information: dict.
	:param population: The population
	:type  population: Organisms.GA.Population
	:param no_of_cpus: The number of cpus that are to be used by your genetic algorithm run.
	:type  no_of_cpus: int
	:param print_details: Print information to the terminal
	:type  print_details: bool.

	:returns: The predation operator object
	:rtype:    Organisms.GA.Predation_Operators.Predation_Operator

	"""
	predation_switch = predation_information['Predation Operator']
	if predation_switch == 'Off':
		from Organisms.GA.Predation_Operators.No_Predation_Operator import No_Predation_Operator
		return No_Predation_Operator(predation_information, population, print_details)
	elif predation_switch == 'Energy':
		from Organisms.GA.Predation_Operators.Energy_Predation_Operator import Energy_Predation_Operator
		return Energy_Predation_Operator(predation_information, population, print_details)
	if predation_switch == 'IDCM':
		from Organisms.GA.Predation_Operators.IDCM_Predation_Operator import IDCM_Predation_Operator
		return IDCM_Predation_Operator(predation_information, population, no_of_cpus, print_details)
	elif predation_switch == 'SCM':
		from Organisms.GA.Predation_Operators.SCM_Predation_Operator import SCM_Predation_Operator
		return SCM_Predation_Operator(predation_information, fitness_information, population, no_of_cpus, print_details)#,no_of_generations)
	else:
		error_string =  'Error in choosing Predation Operators.\n'
		error_string += 'Predation_Operator must be either:'
		error_string += '\t"Off" - No Predation Operator is used.\n'
		error_string += '\t"Energy" - Based on no two clusters can have the same energy in the population.\n'
		error_string += '\t"IDCM" - Based on no two clusters can be structurally identical in the population based on the comparison of those two structuress EDM\'. See Manual for more information.\n'
		error_string += '\t"SCM" - No two structures can be Geometrically Similar based on the Structral Comarison Method. See Manual for more information.\n'
		error_string += 'Check this.\n'
		error_string += 'Predation_Operator = ' + str(predation_switch)+'\n'
		#import pdb, traceback, sys
		#extype, value, tb = sys.exc_info()
		#traceback.print_exc()
		#pdb.post_mortem(tb)
		print(error_string,file=sys.stderr)
		import pdb; pdb.set_trace()
		exit()

def get_fitness_operator(fitness_information, predation_operator, population, generations, no_of_cpus, print_details):
	"""
	This def will set up the fitness operator to be by the genetic algorithm. This is dependent on the entry for the 'Predation_Switch' 
	given in the fitness_information. 

	:param fitness_information: All the information about the fitness operator
	:type  fitness_information: dict.
	:param predation_information: All the informatino about the predation operator.
	:type  predation_information: dict.
	:param population: The population
	:type  population: Organisms.GA.Population
	:param generations: The number of generations being run
	:param generations: int
	:param no_of_cpus: The number of cpus that are to be used by your genetic algorithm run.
	:type  no_of_cpus: int
	:param print_details: Print information to the terminal
	:type  print_details: bool.

	:returns: The fitness operator object
	:rtype:   Organisms.GA.Fitness_Operators.Fitness_Operator

	"""
	fitness_switch = fitness_information['Fitness Operator']
	if fitness_switch == 'Energy':
		from Organisms.GA.Fitness_Operators.Energy_Fitness_Operator import Energy_Fitness_Operator
		return Energy_Fitness_Operator(fitness_information, predation_operator, population, print_details)
	elif fitness_switch == 'Structure + Energy':
		from Organisms.GA.Fitness_Operators.SCM_and_Energy_Fitness_Operator import SCM_and_Energy_Fitness_Operator
		return SCM_and_Energy_Fitness_Operator(fitness_information, predation_operator, population, generations, no_of_cpus, print_details)
	else:
		error_string =  'Error in choosing Fitness Operators.\n'
		error_string += 'Predation_Operator must be either:\n'
		error_string += '\t"Energy" - The fitness of a cluster is based on its energy only.\n'
		error_string += '\t"Structure + Energy" - The fitness of a cluster is based on its energy and structural diversity as determined by the SCM.\n'
		error_string += 'Check this.\n'
		error_string += 'Fitness Operator = ' + str(fitness_switch)+'\n'
		#import pdb, traceback, sys
		#extype, value, tb = sys.exc_info()
		#traceback.print_exc()
		#pdb.post_mortem(tb)
		print(error_string,file=sys.stderr)
		import pdb; pdb.set_trace()
		exit()

def check_asap3_version(self,predation_information,fitness_information):
	"""
	This method is required because their seems to be subtle issues with asap3 3.12.2. Require that asap3 3.11.10 be used.

	:param predation_information: All the informatino about the predation operator.
	:type  predation_information: dict.
	:param fitness_information: All the information about the fitness operator
	:type  fitness_information: dict.	
	"""
	predation_switch = predation_information['Predation Operator']
	fitness_switch = fitness_information['Fitness Operator']
	if (predation_switch == 'SCM') or (fitness_switch == 'SCM + Energy'):
		check_version_of_asap3()
		'''
		import asap3
		version = asap3.__version__
		if not version == '3.11.10':
			print('----------------------------------------------------------------------')
			print('Error when loading asap3 into either the predation or fitness operator.')
			print()
			print('You are wanting to use one or more of the following:')
			print('   * SCM-based predation operator')
			print('   * structure + energy fitness operator')
			print()
			print('If you are using one or more of the above, you need to use asap3.')
			print('Specifically, you want to use asap3 version 3.11.10')
			print()
			print("This is because we have noticed a (core dump) issue that seems to occur during the genetic algorithm. Unfortunately, this error appears at seemingly random times so we don't know what the problem is, but it seems to be resolved if you use this version of asap3")
			print()
			print('Refer to:')
			print('https://organisms.readthedocs.io/en/latest/Installation.html#as-soon-as-possible-asap')
			print('to read about how to install this version of asap3 with pip3.')
			print()
			print('This program with finish without completing.')
			print('----------------------------------------------------------------------')
			exit()
		'''

def get_predation_and_fitness_operators(predation_information, fitness_information, population, generations, no_of_cpus, print_details):
	"""
	This def will set up the predation and fitness operators to be by the genetic algorithm. 

	:param predation_information: All the informatino about the predation operator.
	:type  predation_information: dict.
	:param fitness_information: All the information about the fitness operator
	:type  fitness_information: dict.
	:param population: The population
	:type  population: Organisms.GA.Population
	:param generations: The number of generations being run
	:param generations: int
	:param no_of_cpus: The number of cpus that are to be used by your genetic algorithm run.
	:type  no_of_cpus: int
	:param print_details: Print information to the terminal
	:type  print_details: bool.

	:returns: The predation operator object and the fitness operator object
	:rtype:    A Organisms.GA.Predation_Operators.Predation_Operator object and a Organisms.GA.Fitness_Operators.Fitness_Operator object

	"""
	if not 'Use Predation Information' in fitness_information:
		fitness_information['Use Predation Information'] = False

	predation_operator = get_predation_operator(predation_information, fitness_information, population, no_of_cpus, print_details)
	fitness_operator = get_fitness_operator(fitness_information, predation_operator, population, generations, no_of_cpus, print_details)
	return predation_operator, fitness_operator

