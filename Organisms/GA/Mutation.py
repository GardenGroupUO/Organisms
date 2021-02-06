import copy
import re
from random import randrange, uniform, randint, random
from ase import Atoms

from Organisms.GA.Types_Of_Mutations import moveMutate, homotopMutate, randomMutate
from Organisms.GA.Population import Population
from Organisms.GA.Cluster import Cluster
from Organisms.GA.ExternalDefinitions import InclusionRadiusOfCluster

population_type_example = Population('example',-1,user_initialised_population_folder=None,write_data=False)
cluster_type_example = Cluster()
atoms_type_example = Atoms()

def isfloat(element):
	"""
	Is the input a float.

	:param element: some input
	:type  element: Any

	:returns True if the element can be considered a float, False if not. 
	:rtype   ebool.
	"""
	if re.match(r'^-?\d+(?:\.\d+)?$', element) is None:
		return False
	else:
		return True

class Mutation:
	"""
	This class contains all the information and proceedures required to perform a Mutation. 

	:param mutation_types: Contains the information about the mutations that the user would like to perform. See Manual for more information about this.
	:type  mutation_types: [(str, float),...]
	:param r_ij: The maximum distance that should be between atoms to be considered bonded. This value should be as large a possible, to reflected the longest bond possible between atoms in the cluster.
	:type  r_ij: float
	:param vacuum_to_add_length: The amount of vacuum to place around the cluster
	:type  vacuum_to_add_length: float
	"""
	def __init__(self,mutation_types,r_ij,vacuum_to_add_length):
		self.mutation_types = mutation_types
		#self.r_ij = r_ij
		#self.vacuum_to_add_length = vacuum_to_add_length
		self.check(r_ij)
		self.change_mutation_chances() # update the values in self.mutation_types into the format used by Mutation class.

	def check(self, r_ij):
		"""
		This method will check that the inputs for the mutation_types has been done correctly, without any violating issues.

		:param r_ij: The maximum distance that should be between atoms to be considered bonded. This value should be as large a possible, to reflected the longest bond possible between atoms in the cluster.
		:type  r_ij: float
		"""
		mutation_types, mutation_chances = [list(i) for i in zip(*self.mutation_types)]
		# check that all mutation types are accepted types.
		# DEAL WITH LATER
		for mutation_type in mutation_types:
			if mutation_type.startswith('move'):
				if mutation_type == 'move':
					self.dist_to_move = float(r_ij)*0.5
				elif mutation_type.startswith("move_") and isfloat(mutation_type.replace("move_",'')):
					self.dist_to_move = float(mutation_type.replace("move_",''))
				else:
					print('Error in class MutationProcedure, in MutationProcedure.py')
					print('You need to enter the move entry in either by:')
					print('    * "move", where the move distance is set to default (r_ij*0.5).')
					print('    * "move_XX", where XX is a float that indicate the maximum move distance.')
					print('You input for the move method: '+str(mutation_type))
					print('Check this out. This program will now exit.')
					exit('This program will finish without completing.')
			elif mutation_type.startswith('homotop'):
				if not len(self.population.cluster_makeup) > 1:
					print('Error in class MutationProcedure, in MutationProcedure.py')
					print('You want to use the mutation method "homotop", but your cluster is monometallic')
					print('Cluster Makeup: '+str(self.population.cluster_makeup))
					print('Check this out.')
					exit('This program will finish without completing.')
			elif mutation_type.startswith('random'):
				pass
				#if self.boxtoplaceinlength == None:
				#	print('Error in def mutation, in Class MutationProceedure, in MutationProceedure.py.')
				#	print('If you want to use the "random" mutation method, you need to specify a value for the boxtoplaceinlength variable.')
				#	print('Check this and see if you need to set a value for the boxtoplaceinlength variable.')
				#	exit('This program will finish without completing.')
			elif mutation_type.startswith("random_"):
				continue
			else:
				print('Error in class MutationProcedure, in MutationProcedure.py')
				print('mutation_type '+str(mutation_type)+' is not one of the types of mutation methods')
				print("The types of mutation_types available are: 'move','homotop','random'")
				print('Check this.')
				exit('This program will finish without completing.')
		# Make sure that there are no repetitions of the mutation methods in mutTypes.
		if not len(mutation_types) == len(set(mutation_types)):
			print('Error in class MutationProcedure, in MutationProcedure.py')
			print('You have entered a repeated mutType into mutTypes')
			print('mutTypes: '+str(self.mutTypes))
			print('Check this.')
			exit('This program will finish without completing.')
		# Check if the total chance of mutTypes is equal to 1.
		total_mutation_type_to_choose = sum(mutation_chances)
		if not total_mutation_type_to_choose == 1.0:
			print('Error: the total chance in mutType must equal 1.')
			print('Check your mutType variable')
			print('mutTypes = ' + str(mutTypes))
			print('Total mutTypes chance = ' + str(total_mutation_type_to_choose))
			import pdb; pdb.set_trace()
			exit('This program will finish without completing.')

	def change_mutation_chances(self):
		"""
		This method will change the format of self.mutation_types into a format that can be used by this Mutation class.

		The format of self.mutation_types changes as follows with this example.
			[] => []
		"""
		end_point = 0.0
		for mutation_type in self.mutation_types:
			end_point += mutation_type[1]
			end_point = round(end_point,12)
			mutation_type[1] = end_point
		if not self.mutation_types[-1][1] == 1.0:
			print('Error: The total chance of picking any mutation_type does not equal 1.')
			print('Check your mutation_type variable')
			print('self.mutation_types = ' + str(self.mutation_types))
			print('total  chance = ' + str(self.mutation_types[-1][1]))
			print('Check this')
			import pdb; pdb.set_trace()
			exit('This program will finish without completing.')

	def run(self,run_input,cell_length=None,vacuum_length=None):
		'''
		This definition will run the Mutation Proceedure. 

		Inputs:
			run_input (GA.Population/GA.Cluster/ase.Atoms): This is the input data about the cluster to mutate, or the population to take a cluster to mutate.
			cell_length (float): This is the cell length of the unit cell.
			vacuum_length (float): The amount of vacuum to add to the unit cell.

		Returns:
			mutant (GA.Cluster) - The mutated cluster
			mutation_method (str.) - The type of mutation that was picked to use for this mutation.
		'''
		if type(run_input) is type(population_type_example):
			cluster_to_mutate = self.pickClusterFromThePopulation(run_input)
		elif type(run_input) is type(cluster_type_example) or type(run_input) is type(atoms_type_example):
			cluster_to_mutate = run_input
		else:
			print('Error in def run of class Mutation.')
			print('run_input must be either a population or a specific cluster (of type ASE.Atoms or Cluster).')
			print('run_inpu: '+str(run_inpu))
			print('Check this')
			import pdb; pdb.set_trace()
			exit('This program will finish without completing.')
		#print('The cluster to be mutated is cluster: '+str(cluster_to_mutate.name))
		# Pick the type of mutation method to use
		mutation_method = self.get_mutation_type()
		# perform the mutation. 
		mutant = self.mutation(mutation_method,cluster_to_mutate,cell_length,vacuum_length)
		# respecify the vacuum around the cluster to that its distance is vacuumAdd
		lengthOfCell = 2.0*InclusionRadiusOfCluster(mutant) + vacuum_length
		cell = [lengthOfCell,lengthOfCell,lengthOfCell]
		mutant.set_cell(cell)
		mutant.center() # centre the cluster within this unit cell
		# return the mutant, as well as the mutation method that was performed. 
		if not len(mutant) == len(cluster_to_mutate):
			print('Error in def run, in Mutation.py')
			print('The offspring contains '+str(len(mutant))+' atoms, but should contain '+str(len(cluster_to_mutate)))
			print('Check this')
			import pdb; pdb.set_trace()
			print('This program will finish without completing')
			exit()
		return mutant, mutation_method

	def pickClusterFromThePopulation(self,population):
		"""
		This definition will pick the cluster from the population to mutate.

		Inputs:
			population (GA.Population): The population to choose the cluster to mutate from.
		
		:returns: cluster_to_mutate - The list of parents for mating.
		:rtypes: Cluster

		"""
		index = randrange(0,len(population))
		cluster_to_mutate = population[index].deepcopy()
		return cluster_to_mutate

	def get_mutation_type(self):
		"""
		This definition will pick the type of mutation.

		:returns: mutation_type
		:rtypes: str.

		"""
		if not len(self.mutation_types) == 1:
			chance_of_type_of_mutation = uniform(0,1)
		else:
			chance_of_type_of_mutation = 0 # dont need to perform uniform(0,1) if you only have one mutation_method
		for mutation_type, mutation_echelon in self.mutation_types:
			if chance_of_type_of_mutation <= mutation_echelon:
				return mutation_type
		print('Error in def get_mutation_type in class Mutation_Procedure, in MutationProcedure.py')
		print('Somehow, I think chance_of_type_of_mutation is greater than 1???')
		print('chance_of_type_of_mutation = '+str(chance_of_type_of_mutation))
		print('self.mutation_types = '+str(self.mutation_types))
		print('Check this')
		import pdb; pdb.set_trace()
		exit('This program will finish without completing.')

	def mutation(self,mutation_method,cluster_to_mutate,cell_length=None,vacuum_length=None):
		"""
		This method will perform the mutation and return the mutant. 

		Inputs:
			mutation_method (str.): The type of mutation to use for the mutation
			cluster_to_mutate (GA>Cluster): This is the cluster that we would like to perform a mutation upon.
			cell_length (float): This is the cell length of the unit cell.
			vacuum_length (float): The amount of vacuum to add to the unit cell.

		:returns: mutant
		:rtypes: Atom

		"""
		if mutation_method == "random":
			mutant = randomMutate(cell_length, vacuum_length,cluster_makeup=cluster_to_mutate.get_elemental_makeup(),cluster_to_mutate=None,percentage_of_cluster_to_randomise=None)
		elif mutation_method.startswith('random_'):
			percentage_of_cluster_to_randomise = mutation_method.replace('random_','')
			try:
				percentage_of_cluster_to_randomise = float(percentage_of_cluster_to_randomise)
			except:
				print('Error in MutationProcedure Class: If you are using chosen_mutation_type in random_X where X is a percentage of atoms to be randomised, X must be in the form of an interger or a decimal number.')
				print('Check this.')
				print('chosen_mutation_type: '+str(mutation_method))
				import pdb; pdb.set_trace()
				exit()
			# this should be check later to see if it is working as intended.
			mutant = randomMutate(cell_length, vacuum_length, cluster_makeup=None,cluster_to_mutate=cluster_to_mutate,percentage_of_cluster_to_randomise=percentage_of_cluster_to_randomise)
		elif mutation_method.startswith("move"):
			mutant = moveMutate(cluster_to_mutate,self.dist_to_move)
		elif mutation_method == "homotop":
			mutant = homotopMutate(cluster_to_mutate)
		else:
			print('Check this')
			import pdb; pdb.set_trace()
			exit('This program will finish without completing.')
		if not len(mutant) == len(cluster_to_mutate):
			print('Error in def mutation, in Mutation.py')
			print('The offspring contains '+str(len(mutant))+' atoms, but should contain '+str(len(cluster_to_mutate)))
			print('Check this')
			import pdb; pdb.set_trace()
			print('This program will finish without completing')
			exit()
		return mutant
