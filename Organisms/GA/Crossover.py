"""

MatingProcedure.py, 13/04/2017, Geoffrey R. Weal

This program is designed to run the mating proceedure of the Genetic Algorithm.

"""

from ase import Atom, Atoms
import random as rand
import numpy as np
import copy
from Organisms.GA.ExternalDefinitions import get_elemental_makeup, AtomInClusterPosition, InclusionRadiusOfCluster
from Organisms.GA.Cluster import Cluster
from Organisms.GA.Population import Population
from collections import Counter

#population_type_example = Population('example',-1,False,None,False)
#cluster_type_example = Cluster()

class Crossover:
	"""
	This class is designed to perform the mating proceedure of the genetic algorithm. This will produce a cluster that is an outcome of the mating proceedure.

	:param crossover_type: This is the type of mating proceedure the user would like to use. There are currently a few options implimented into this mating proceedure:

		* "CAS_weighted"-: Cut and Splice - Deavon and Ho - weighted by fitness of parents (CAS_weighted)
		* "CAS_random":    Cut and Splice - Deavon and Ho - cut a random percent x% of parent 1 and (100-x)% of parent 2 (CAS_random)
		* "CAS_half":      Cut and Splice - Deavon and Ho - cut both parents by half (CAS_half)
		* "CAS_custom_XX":   Cut and Splice - Deavon and Ho - cut a random percent XX% of parent 1 and (100-XXX)% of parent 2. To use this set crossType = CAS_custom_XX, where XX is a float of your choice between 0 and 100.
	:type  crossover_type: str.
	:param r_ij: the maximum bond distance between atoms in the cluster. This should be the largest value possible for your cluster.
	:type  r_ij: float
	:param vacuumAdd: The vacuum around the cluster
	:type  vacuumAdd: float
	:param size_of_clusters: The number of atoms in the cluster.
	:type  size_of_clusters: int

	"""
	def __init__(self,crossover_type,r_ij,vacuumAdd,size_of_clusters):
		self.crossover_type = crossover_type
		self.r_ij = r_ij
		self.vacuumAdd = vacuumAdd
		self.size_of_clusters = size_of_clusters
		# -------------------------------------------- #
		# Assign a method to use for the mating proceedure.
		if self.crossover_type == "CAS_weighted":
			self.mating_method = self.Cut_and_Splice_Devon_and_Ho
		elif self.crossover_type == "CAS_random":
			self.half_index = self.half_index_random_method()
			self.mating_method = self.Cut_and_Splice_Devon_and_Ho
		elif self.crossover_type == "CAS_half":
			self.half_index = self.half_index_half_method()
			self.mating_method = self.Cut_and_Splice_Devon_and_Ho
		elif "CAS_custom_" in self.crossover_type:
			self.half_index = self.half_index_custom_method()
			self.mating_method = self.Cut_and_Splice_Devon_and_Ho
		else:
			print("Error in def mating in class MatingProcedure, in MatingProcedure.py: No Mating method selected")
			print("Mating Proceedures available:")
			print("\tCut and Splice - Deavon and Ho - weighted by fitness of parents (CAS_weighted)")
			print("\tCut and Splice - Deavon and Ho - cut a random percent x% of parent 1 and (100-x)% of parent 2 (CAS_random)")
			print("\tCut and Splice - Deavon and Ho - cut both parents by half (CAS_half)")
			print("\tCut and Splice - Deavon and Ho - cut a random percent XXX% of parent 1 and (100-XXX)% of parent 2 (CAS_custom_XXX). To use this set crossType = CAS_custom_XXX, where XXX is a float of your choice between 0 and 100.")
			exit('This program will finish without completing')
		# -------------------------------------------- #

	def run(self,run_input):
		"""
		Run this the Mating Proceedure and gives an offspring.

		:param population: This is the population to choose clusters from to mate together. 
		:type  population: Organisms.GA.Population

		:returns: offspring
		:rtypes: Organisms.GA.Cluster

		"""
		parents = self.pickParentsFromThePopulation(run_input)
		#parents = self.centre_parents_about_origin(parents) # put a 
		offspring = self.mating(parents)
		#self.centre_offspring_at_centre_of_cell(offspring)
		return offspring

	def pickParentsFromThePopulation(self,population):
		"""
		This definition will pick the parents for mating.

		:param population: This is the population to choose clusters from to mate together. 
		:type  population: Organisms.GA.Population

		:returns: two clusters from the population that will be mated together to give the offspring.
		:rtypes: (Organisms.GA.Cluster, Organisms.GA.Cluster)

		"""
		pairPos = self.roulette(population)
		parent1 = population[pairPos[0]].deepcopy()
		parent2 = population[pairPos[1]].deepcopy()
		return [parent1, parent2]

	def roulette(self,population):
		"""
		Performed the roulette wheel method to obtain the parents for a Mating proceedure

		Reference: https://pubs.rsc.org/en/content/articlepdf/2003/dt/b305686d

		:param population: This is the population to choose clusters from to mate together. 
		:type  population: Organisms.GA.Population

		:returns: Will return a tuple of two integers that represent the indices of clusters in the population to use as parent to mate together to give a new offspring.
		:rtypes: [int, int]

		"""
		index_pair = []; index_pair_names = []; population_size = len(population)
		# Pick parents
		while len(index_pair) < 2:
			chosen_cluster_index = rand.randrange(0,population_size,1) # Pick a random cluster to assess.
			chosen_cluster = population[chosen_cluster_index]
			if not chosen_cluster.name in index_pair_names:
				randomFit = rand.uniform(0,1) # Choose a random fitness criteria value.
				# If the random cluster's fitness value is higher than the fitness criteria 
				# value (and is not already a parent), accept the cluster as a parent. 
				if chosen_cluster.fitness > randomFit:
					index_pair.append(chosen_cluster_index)
					index_pair_names.append(chosen_cluster.name)
		# This is a method to check that all is well with the roulette method. Turn on if you are ever playing around with it
		if len(index_pair_names) != len(set(index_pair_names)) or len(index_pair) != len(set(index_pair)):
			print("Error in def roulette in class MatingProcedure, in MatingProcedure.py")
			print("A cluster has been selected at least twice by the roulette wheel method.")
			if len(index_pair_names) != len(set(index_pair_names)):
				print('Two of the clusters have the same dir (i.e. this means they are the same cluster).')
			if len(index_pair) != len(set(index_pair)):
				print('Two of the clusters have the same index in the population.')
			print('Clusters that have been selected: '+str(index_pair_names))
			print('The indices of the clusters in the population that have been selected: '+str(index_pair))
			print('Check this.')
			import pdb; pdb.set_trace()
			exit('This program will finish without completing')
		return index_pair

	def tournament(self,population):
		"""
		Performed the tournament method to obtain the parents for a Mating proceedure

		Reference: https://pubs.rsc.org/en/content/articlepdf/2003/dt/b305686d

		:param population: This is the population to choose clusters from to mate together. 
		:type  population: Organisms.GA.Population
		
		:returns: Will return a tuple of two integers that represent the indices of clusters in the population to use as parent to mate together to give a new offspring.
		:rtypes: [int, int]
		"""
		number_of_clusters_in_tournament = X
		clusters_in_tournament = []; population_size = len(population)
		clusters_in_tournament_names = []
		# Pick parents
		while len(clusters_in_tournament) < number_of_clusters_in_tournament:
			chosen_cluster_index = rand.randrange(0,population_size,1) # Pick a random cluster to assess.
			chosen_cluster = population[chosen_cluster_index]
			if not chosen_cluster.name not in clusters_in_tournament_names:
				clusters_in_tournament_names.append(chosen_cluster.name)
				clusters_in_tournament.append((chosen_cluster_index,chosen_cluster.fitness))
		if len(clusters_in_tournament) != len(set(clusters_in_tournament)):
			print("Error in def tournament in class MatingProcedure, in MatingProcedure.py")
			print("A cluster has been selected at least twice by the tournament method.")
			print('Clusters that have been selected (index in pop, cluster name): '+str(clusters_in_tournament))
			print('Check this.')
			import pdb; pdb.set_trace()
			exit('This program will finish without completing')
		clusters_in_tournament.sort(key = lambda x: x[1], reverse=True)
		index_pair = (clusters_in_tournament[0][0], clusters_in_tournament[1][0])
		return index_pair

	def centre_parents_about_origin(self,parents):
		"""
		This method will center the parents about the zero point. This is to make sure that their two halfs will allign correctly when they are cut and spliced to form a new offsping

		:param parents: This is the population to choose clusters from to mate together. 
		:type  parents: [Organisms.GA.Cluster, Organisms.GA.Cluster]
		
		:returns: The parents which have been centered about the (0,0,0) point of the unit cell
		:rtypes: [Organisms.GA.Cluster, Organisms.GA.Cluster]

		"""
		for parent in parents:
			parent.center(vacuum=None, axis=(0, 1, 2), about=0.)
		return parents

	def centre_offspring_at_centre_of_cell(self,offspring):
		"""
		This method will center the offspring as required. 

		:param offspring: The offspring cluster. 
		:type  offspring: Organisms.GA.Cluster

		"""
		offspring.centre_cluster_at_centre_of_cell(self.vacuumAdd)

	def mating(self, parents):
		"""
		This definition is designed as a switch to choose the mating method the user wishes to use for the genetic algorithm.

		:param parents: This is the population to choose clusters from to mate together. 
		:type  parents: [Organisms.GA.Cluster, Organisms.GA.Cluster]

		:returns: Returns an offspring that has been created from mating two parent clusters together. 
		:rtypes:  Organisms.GA.Cluster

		"""
		return self.mating_method(parents) # returns a new offspring

	#################################################################################
	#################################################################################

	def Cut_and_Splice_Devon_and_Ho(self,parents):
		"""
		This definition is designed to perform the Cut and Splice Method as specified by 
		Devon and Ho to mate the parents to give the offspring. The method works as follows:
		
			1. Rotate each parent by some random amount in the theta and phi directions.
			2. Sort the assignment of atoms in the cluster from most positive to most negative z value.
			3. Perform a Cut and Splice proceedure, where the parents are cut in some way and spliced together to give the offspring. 

		:param parents: This is the population to choose clusters from to mate together. 
		:type  parents: [Organisms.GA.Cluster, Organisms.GA.Cluster]
		
		:returns: Returns an offspring that has been created from mating two parent clusters together. 
		:rtypes:  Organisms.GA.Cluster
		"""
		for i in range(len(parents)):
			self.rotate(parents[i]) # Rotate parent parents[1] = self.rotate(parents[1]) 
			parents[i].sortZ() # sort atoms in parent from most positive to most negative value of z
		offspring = self.mate_Cut_and_Splice(parents) # Perform the Cut and Splice Method
		return offspring

	def rotate(self,cluster):
		"""
		Rotate the cluster by some random angle in the theta and phi directions.
		
		:param cluster: The cluster to be randomly rotated
		:type  cluster: Organisms.GA.Cluster

		"""
		#randomly select the value of theta and phi. Change to degrees since change in ase 3.14.0
		# see https://mathworld.wolfram.com/EulerAngles.html for how the angles work.
		phi = rand.uniform(0,360.0)
		theta = rand.uniform(0,180.0) # angle theta in [0,pi]
		psi = rand.uniform(0,360.0)
		# Create the matrix representation to rotate the cluster in the following way:
		#	Look at Euler Angles about this: http://mathworld.wolfram.com/EulerAngles.html
		cluster.euler_rotate(phi=phi, theta=theta, psi=psi, center=(0, 0, 0)) # changed to allign with format from ase >= 3.14.0
		#return cluster

	def mate_Cut_and_Splice(self,parents):
		"""
		This method will perform the mating proceedure as specified by the user.
		This can been designed to be used with multiple parents, however currently it is set up for 2 parents.
		It has also been developed for mating multi-metallic (multi-elemental) clusters together.

		:param parents: This is the population to choose clusters from to mate together. 
		:type  parents: [Organisms.GA.Cluster, Organisms.GA.Cluster]
		
		:returns: Returns an offspring that has been created from mating two parent clusters together. 
		:rtypes:  Organisms.GA.Cluster	

		"""
		#elemental_makeup_of_parents = self.mate_Cut_and_Splice_error_checking_1(parents) # Error Checking. Uncomment this if you are ever editing the crossover method
		# if "weighed" is chosen, use the fitness values of parents to find the cut points in the clusters.
		if self.crossover_type == "CAS_weighted":
			self.half_index = self.half_index_weighted_method(parents)
		if self.crossover_type == "CAS_random":
			self.half_index = self.half_index_random_method()
		# Get half of first parent
		offspring = parents[0][:self.half_index:]
		elementsInParent1 = parents[1].get_elemental_makeup() #elemental_makeup_of_parents[1]
		if len(elementsInParent1.keys()) > 1:
			# Count the difference in elements between the parent and the current cluster. This is so the
			# offspring has the same numbers of elements as its parents
			elements_in_current_offspring = offspring.get_elemental_makeup()
			elements_to_add = elementsInParent1 - elements_in_current_offspring
			for atom_to_add in parents[1][::-1]:
				if elements_to_add[atom_to_add.symbol] > 0 and not AtomInClusterPosition(atom_to_add,offspring):
					offspring.append(atom_to_add)
					elements_to_add[atom_to_add.symbol] -= 1
					if not any(not value == 0 for value in elements_to_add.values()):
						break
		else:
			#for atom_to_add in parents[1][self.half_index::]:
			#	if not AtomInClusterPosition(atom_to_add,offspring):
			#		offspring.append(atom_to_add)
			offspring += parents[1][self.half_index::]
		#self.mate_Cut_and_Splice_error_checking_2(elemental_makeup_of_parents,offspring) # Error Checking. Uncomment this if you are ever editing the crossover method
		return offspring

	def mate_Cut_and_Splice_error_checking_1(self,parents):
		"""
		This is a method for checking if there are any issues with the Cut_and_splice method. 

		This method is only needed when you are developing or modifying a mating proceedure, to help with debugging. Otherwise, you dont need to use this algorithm

		:param parents: This is the population to choose clusters from to mate together. 
		:type  parents: [GA.Cluster, GA.Cluster]

		:returns: A list which indicates the types of elements, and the number of those elements, in the cluster
		:rtype: {str: int, ...} 
		"""
		elemental_makeup_of_parents = []
		for parent in parents:
			elemental_makeup_of_parents.append(parent.get_elemental_makeup())
		# check that the parents have the same elements and amount of every element:
		for index in range(1,len(elemental_makeup_of_parents)):
			if not elemental_makeup_of_parents[index] == elemental_makeup_of_parents[0]:
				print('Error in def mate_Cut_and_Splice: The parents do not have the same element count.')
				print('Element Count of Parents')
				for index in range(len(elemental_makeup_of_parents)):
					print('Parent ' + str(index+1) + ': ' + str(elemental_makeup_of_parents[index]))
				print('Check this')
				import pdb; pdb.set_trace()
				exit('This program will finish without completing')
		return elemental_makeup_of_parents


	def mate_Cut_and_Splice_error_checking_2(self,elemental_makeup_of_parents,offspring):
		"""
		This is a method for checking if there are any issues with the Cut_and_splice method. 

		This method is only needed when you are developing or modifying a mating proceedure, to help with debugging. Otherwise, you dont need to use this algorithm

		:param elemental_makeup_of_parents: A list which indicates the types of elements, and the number of those elements, in the cluster
		:type  elemental_makeup_of_parents: {str: int, ...} 
		:param offspring: The offspring cluster. 
		:type  offspring: Organisms.GA.Cluster

		"""
		elemental_makeup_of_offspring = get_elemental_makeup(offspring)
		if not elemental_makeup_of_offspring == elemental_makeup_of_parents[0]:
			print('Error in def mate_Cut_and_Splice: The parents do not have the same element count.')
			print("ERROR: Parent and offspring elemental makeup are not the same: No of Atoms in;")
			print('-------------------------')
			print('Element Count of Parents')
			for index in range(len(elemental_makeup_of_parents)):
				print('Parent ' + str(index+1) + ': ' + str(elemental_makeup_of_parents[index]))
			print('-------------------------')
			print('Element Count of Offspring')
			print('Offspring: ' + str(offspring.get_elemental_makeup()))
			print('-------------------------')
			import pdb; pdb.set_trace()
			exit('This program will finish without completing')


	def half_index_weighted_method(self,parents):
		"""
		This method will determine how to cut the cluster based on the atom to divide from, where the atoms have been numbered in order of the z axis.

		This version of the method divides the parents based on their relative fitnesses.

		:param parents: This is the population to choose clusters from to mate together. 
		:type  parents: [Organisms.GA.Cluster, Organisms.GA.Cluster]

		:returns: The atom number in the cluster to cut the atom.
		:rtype: int
		"""
		fitPair = []
		for parent in parents:
			fitPair.append(parent.fitness)
		fit1 = fitPair[0]; fit2 = fitPair[1]
		return int(self.size_of_clusters*(fit1/(fit1+fit2))) # This is half_index

	def half_index_random_method(self):
		"""
		This method will determine how to cut the cluster based on the atom to divide from, where the atoms have been numbered in order of the z axis.

		This version of the method divides the parents at some random atom indice

		:returns: The atom number in the cluster to cut the atom.
		:rtype: int
		"""
		half_index = int(self.size_of_clusters*rand.random())
		return half_index

	def half_index_half_method(self):
		"""
		This method will determine how to cut the cluster based on the atom to divide from, where the atoms have been numbered in order of the z axis.

		This version of the method divides the parents in half.

		:returns: The atom number in the cluster to cut the atom.
		:rtype: int
		"""
		half_index = int(self.size_of_clusters*(1.0/2.0))
		return half_index

	def half_index_custom_method(self,cross_type):
		"""
		This method will determine how to cut the cluster based on the atom to divide from, where the atoms have been numbered in order of the z axis.

		This version of the method divides the parents based on a percentage of atoms to take from parent 1

		Here, percentage of parent1 is taken, while 1.0-percentage of parent2 two is taken.

		:param crossover_type: This is the type of mating proceedure the user would like to use. This should be set to "CAS_custom_XX", where XX is the percentage of parent 1 to be cut.
		:type  crossover_type: str.

		:returns: The atom number in the cluster to cut the atom.
		:rtype: int
		"""
		percentage = cross_type.replace('custom_','')
		try:
			percentage = float(percentage)
		except ValueError:
			exit("Error in MatingProcedure.py using Cut and Splice - Deavon and Ho - Custom. " + str(percentage) + " is not a float.") 
		if percentage < 0.0 or percentage > 100:
			print("Error in MatingProcedure.py using Cut and Splice - Deavon and Ho - Custom.")
			print("Custom percentage must be between 0 and 100. Percentage = " + str(percentage))
			exit('This program will finish without completing')
		half_index = int(self.size_of_clusters*(percentage/100.0))
		return half_index


