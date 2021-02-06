from random import uniform 
import os, sys
from io import StringIO
from time import time

from Organisms.GA.ExternalDefinitions import Exploded

def Create_An_Unoptimised_Offspring(cluster_number,chance_of_mutation,cell_length,vacuum_to_add_length,population,creating_offspring_mode,crossover_procedure,mutation_procedure):
	"""
	This definition provides the methodology for how to create an offspring.

	Inputs:
		cluster_number (int): the name of the cluster
		chance_of_mutation (float): the change than a mutation will occur, either as well as or instead of crossover, depending on input for creating_offspring_mode.
		cell_length (float): The size of the unit cell.
		vacuum_to_add_length (float)" The amount of vacuum to add to the unit cell"
		population (Organisms.GA.Population): This is the population that clusters will be taken from for mating and mutation schemes.
		creating_offspring_mode (str.): This tag indicates how the offspring are created. 

			* creating_offspring_mode == 'Mating_and_Mutation_Together' - The mating scheme is run first, followed by a mutation scheme with some probability.. 
			* creating_offspring_mode == 'Either_Mating_and_Mutation' - Either the mating 'or' the mutation scheme will run, depending on a probability value.
		
		crossover_procedure (Organisms.GA.Crossover): 
		mutation_procedure (Organisms.GA.Mutation): 

	:returns: the newly created offspring cluster.
	:rtype: Organisms.GA.Cluster
	"""
	# Choose to perform a Mutation or Mating Proceedure
	choice_mate_or_mutate = uniform(0,1)
	if creating_offspring_mode == 'Mating_and_Mutation_Together':
		#print("Cluster " + str(cluster_number) + " will be put through a Mating Method.")
		offspring = crossover_procedure.run(population)
		#how_created.append('Mating')
		if Will_Mutation_Occur(choice_mate_or_mutate,chance_of_mutation):
			#print("Cluster " + str(cluster_number) + " will be put through a Mutation Method.")
			offspring, mutation_method = mutation_procedure.run(cluster_to_mutate=cluster_to_mutate,cell_length=cell_length,vacuum_length=vacuum_to_add_length)
			#how_created.append('Mutation')
			#print('The mutation method used was ' + mutation_method)
	elif creating_offspring_mode == 'Either_Mating_and_Mutation':
		if Will_Mutation_Occur(choice_mate_or_mutate,chance_of_mutation):
			#print("Cluster " + str(cluster_number) + " obtained using the Mutation Method.")
			offspring, mutation_method = mutation_procedure.run(population,cell_length=cell_length,vacuum_length=vacuum_to_add_length)
			#how_created.append('Mutation')
			#print('The mutation method used was ' + mutation_method)
		else:
			#print("Cluster " + str(cluster_number) + " obtained using the Mating Method.")
			offspring = crossover_procedure.run(population)
			#how_created.append('Mating')
	else:
		print('creating_offspring_mode must be either Mating_and_Mutation_Together or Either_Mating_and_Mutation')
		print('Check this')
		print('creating_offspring_mode = ' + str(creating_offspring_mode))
		exit('This program will finish without completion.')
	if not len(offspring) == len(population[0]):
		print('Error in def Create_An_Unoptimised_Offspring, in Get_Offspring.py')
		print('The offspring contains '+str(len(offspring))+' atoms, but should contain '+str(len(population[0])))
		print('Check this')
		import pdb; pdb.set_trace()
		print('This program will finish without completing')
		exit()
	return offspring

def Will_Mutation_Occur(choice_mate_or_mutate,chance_of_mutation):
	"""
	This method will determine if the algotithm should perform a mutation.

	:param choice_mate_or_mutate: This is a random value between 0 and 1. If this value is less than self.chance_of_mutation, this indicates to perform a mutation
	:type  choice_mate_or_mutate: float
	:param chance_of_mutation: This a decimal value between 0 and 1 that determines the chance of a mutation.
	:type  chance_of_mutation: float

	:returns: If True; mutate. If False; do not mutate (mate).
	:rtype: bool.
	"""
	return choice_mate_or_mutate < chance_of_mutation
	
def Create_An_Offspring(input_data):
	"""
	This method is used to obtain an offspring

	:param input_data: A tuple of all the information needed to make a new offspring
	:type  input_data: tuple of many inputs

	:returns: The offspring and a string containing any information that would be useful for the user to see about how this cluster was made
	:rtype: Organisms.GA.Cluster and str.
	"""
	#total_start_time = time()
	(run_number,generation_number,population,offspring_pool_name,chance_of_mutation,r_ij,cell_length,vacuum_to_add_length,creating_offspring_mode,crossover_procedure,mutation_procedure,no_offspring_per_generation,rounding_criteria,Minimisation_Function,surface,place_cluster_where,print_details) = input_data
	toString = ''
	cluster_name = run_number
	#if print_details:
	#	toString += "----------------------------------------------------------"+'\n'
	no_of_explosions = 0; no_of_not_converged = 0
	while True:
		#cluster_start_time = time()
		#stdout = sys.stdout; output = StringIO(); sys.stdout = output
		UnOpt_offspring = Create_An_Unoptimised_Offspring(cluster_name,chance_of_mutation,cell_length,vacuum_to_add_length,population,creating_offspring_mode,crossover_procedure,mutation_procedure)
		#sys.stdout = stdout
		#cluster_end_time = time()
		#if print_details:
		#	toString += output.getvalue().rstrip()
		#######################################################################################
		# Locally Minimise the cluster. Since the population class looks after the population folder, this process is done from self.population
		#minimisation_start_time = time()
		#stdout = sys.stdout; output = StringIO(); sys.stdout = output
		try_statement_counter = 0
		while True:
			try:
				Opt_offspring, converged, opt_information = Minimisation_Function(UnOpt_offspring.deepcopy(),offspring_pool_name,cluster_name)
				break
			except Exception as exception:
				print('Error during minimisation. Something has gone wrong during the local optimisation process',file=sys.stderr)
				print('Generation: '+str(generation_number)+'; Cluster Name: '+str(run_number),file=sys.stderr)
				print('exception',file=sys.stderr)
				print('Will Try to run the local optimisation process again',file=sys.stderr)
				try_statement_counter += 1
			if try_statement_counter == 10:
				print('The above error has occurred 10 times.',file=sys.stderr)
				print('Will make a new offspring and discard this one',file=sys.stderr)
				break
		#sys.stdout = stdout
		#if print_details:
		#	opt_information['output.txt'] = output.getvalue()
		#######################################################################################
		if not try_statement_counter == 10:
			#minimisation_end_time = time()
			break
			#exploded_start_time = time()
			did_explode = Exploded(Opt_offspring,max_distance_between_atoms=r_ij)
			#exploded_end_time = time()
			if did_explode: # make sure the randomised cluster has not split up when optimised.
				toString += "Cluster exploded. Will disregard this cluster and try mating or mutation method again"+'\n'
				no_of_explosions += 1
			elif not converged:
				toString += "Cluster did not converge. Will disregard this cluster and try mating or mutation method again"+'\n'
				no_of_not_converged += 1
			else:
				break
	# Add the cluster to the list of offspring from this list
	#extra1_start = time()
	Opt_offspring.verify_cluster(cluster_name,generation_number,vacuum_to_add_length,rounding_criteria)
	#extra1_end = time()
	#extra2_start = time()
	Opt_offspring.remove_calculator()
	'''
	extra2_end = time()
	minimisation_end_time = time()
	#print(str(cluster_name)+', ', end = '')
	total_end_time = time()
	print('Total offspring creation time: '+str(total_end_time-total_start_time)+' s.')
	print('Make offspring time: '+str(cluster_end_time-cluster_start_time)+' s. Run Minimisation time: '+str(minimisation_end_time-minimisation_start_time)+' s.')#' Check for exploded: '+str(exploded_end_time-exploded_start_time)+' s.')
	print('Extra time 1: '+str(extra1_end-extra1_start)+' s.')
	print('Extra time 2: '+str(extra2_end-extra2_start)+' s.')
	print('---------------------------------------------------')
	'''
	return Opt_offspring, toString

	