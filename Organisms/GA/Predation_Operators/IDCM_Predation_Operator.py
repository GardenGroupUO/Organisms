'''
IDCM_Predation_Operator.py, Geoffrey Weal, 25/12/2019

This is one of the Predation Operators that can be used by the genetic algorithm program. This is the IDCM Predation Operator.

This Operator works by preventing the population from having clusters with the same ...

'''

##################################################################################################################################################
#################### Initialising and Preparing the imports and internal defs that are needed for the IDCM Predation Operator #####################
##################################################################################################################################################

import os
import numpy as np
from copy import deepcopy
from io import StringIO

from Organisms.GA.Predation_Operators.Predation_Operator import Predation_Operator

from Organisms.GA.Predation_Operators.IDCM_Predation_Operator_Scripts.IDCM_Methods import get_cluster_distance_list, LoD_compare_two_structures
from Organisms.GA.Predation_Operators.IDCM_Predation_Operator_Scripts.LoD_Comparison_Database import LoD_Comparison_Database

import multiprocessing as mp
import time
from collections import OrderedDict

##################################################################################################################################################

class Collection_and_Similarity_Settings_Iterator:
	def __init__(self, collection, similarity_settings):
		self.index = 0
		self.collection = collection
		self.similarity_settings = similarity_settings

	def __iter__(self):
		return self

	def __next__(self):
		if self.index < len(self.collection):
			index = self.index
			self.index += 1
			cluster = self.collection[index]
			return (cluster, self.similarity_settings)
		else:
			raise StopIteration

class structures_in_LoD_database_Iterator:
	def __init__(self, LoD_database, LoD_comparison_database, similarity_settings):
		self.index1 = 0
		self.index2 = self.index1+1
		self.LoD_database = LoD_database
		self.LoD_comparison_database = LoD_comparison_database
		self.structures_in_LoD_database = list(self.LoD_database.keys())
		self.similarity_settings = similarity_settings

	def __iter__(self):
		return self

	def __next__(self):
		while True:
			if self.index2 == len(self.structures_in_LoD_database):
				self.index1 += 1
				self.index2 = self.index1+1
			if self.index1+1 == len(self.structures_in_LoD_database):
				raise StopIteration
			cluster1_name = self.structures_in_LoD_database[self.index1]
			cluster2_name = self.structures_in_LoD_database[self.index2]
			self.index2 += 1
			if not self.LoD_comparison_database.is_cluster_pair_in_the_database(cluster1_name,cluster2_name):
				task_input = (cluster1_name, cluster2_name, self.LoD_database[cluster1_name], self.LoD_database[cluster2_name], self.similarity_settings)
				break
		return task_input

##################################################################################################################################################

def get_LoD_database(cluster_info):
	cluster, similarity_settings = cluster_info
	percentage_diff = similarity_settings['percentage_diff']
	cluster_LoD = get_cluster_distance_list(cluster, percentage_diff)
	return (cluster.name, cluster_LoD)

def check_if_two_clusters_are_identical_LoD(both_clusters):
	cluster_1_name, cluster_2_name, cluster_1, cluster_2, similarity_settings = both_clusters
	#print((cluster_1_name, cluster_2_name, eps_r))
	#print('Comparing '+str(cluster_1.name)+' with '+str(cluster_2.name))
	percentage_diff = similarity_settings['percentage_diff']
	the_same_cluster = LoD_compare_two_structures(cluster_1, cluster_2, percentage_diff)
	return ((cluster_1_name, cluster_2_name), the_same_cluster)

def remove_duplicates(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 

##################################################################################################################################################

class Cluster_Block:
	"""
	This is used by the Remove_Cluster_Due_To_Predation_Violation definition to store information in an easy way to help the user understand what is going on in this method 

	:param collection: This is the collection to record. This is either the instance of the Population or the Offspring_Pool
	:type  collection: Population or Offspring_Pool
	:param collection_type: This describes if the cluster recorded is in the population (given as 'pop') or the offspring (given as 'off').
	:type  collection_type: str.
	:param index: The position/index of the cluster in the collection.
	:type  index: int

	"""
	def __init__(self,collection,collection_type,index):
		self.collection_type = collection_type
		self.index = index
		self.name = collection[index].name
		self.fitness = collection[index].fitness
		self.energy = collection[index].energy
	def  __repr__(self):
		return str(self.collection_type)+str(self.name)+'('+str(self.index)+','+str(round(self.energy,6))+' eV,'+str(round(self.fitness,3))+')'

##################################################################################################################################################

class IDCM_Predation_Operator(Predation_Operator):
	"""
	This is a Predation Operator for identifying if two clusters are identifcal using a style of a euclidean distance matrix.

	This is based on the method given in MEGA to describe the IDCM Operator.

	MEGA is described in more detail in https://pubs.acs.org/doi/abs/10.1021/acs.jpcc.6b12848

	:param Predation_Information: This contains all the information needed by the Predation Operator you want to use to run.
	:type  Predation_Information: dict.
	:param population: This is the population that this Operator will be controlling to make sure that no two clusters in the population have the same energy.
	:type  population: Organisms.GA.Population
	:param print_details: Print details of the predation operator, like verbose
	:type  print_details: bool

	"""
	def __init__(self,Predation_Information,population,no_of_cpus,print_details):
		super().__init__(Predation_Information,population,print_details)
		self.no_of_cpus = no_of_cpus 
		########################################################################################################################
		if not Predation_Information['Predation Operator'] == 'IDCM':
			print('Error in class IDCM_Predation_Operator, in IDCM_Predation_Operator.py')
			print('The Predation Operator "IDCM_Predation_Operator" has been initialised.')
			print("However, Predation_Information['Predation Operator'] is not 'IDCM'")
			print("Predation_Information['Predation Operator'] = "+str(Predation_Information['Predation Operator']))
			print('Check this out.')
			import pdb; pdb.set_trace()
			exit()
		############################################################
		self.structurally_identical_method = 'IDCM'
		if self.structurally_identical_method == 'IDCM':
			self.get_structural_data_method = get_LoD_database
			self.check_if_two_clusters_are_identical_method = check_if_two_clusters_are_identical_LoD
			percentage_diff = float(Predation_Information['percentage_diff']) # distance_difference
			neighbor_cutoff = float('inf') # Predation_Information['neighbor_cutoff'] # neighbor_cutoff
			self.similarity_settings = {'percentage_diff': percentage_diff}
		else:
			print('Error in IDCM_Predation_Operator, in IDCM_Predation_Operator.py')
			print('The structurally identical method that can be used can be:')
			print('\t- IDCM - A structural identical method that have been taken from the mexican enchanced genetic algorithm. https://doi.org/10.1021/acs.jpcc.6b12848')
			import pdb; pdb.set_trace()
			exit()
		# Create the databases that will hold the EDM information of all the clsuters in the population and offspring, and how they compare.
		self.LoD_database = {}
		self.LoD_comparison_database = LoD_Comparison_Database()
		####################################################################################

	################################################################################################################################################################################################################
	########################## Methods Required for the def Check_Initial_Population, in the class Predation_Operator, in IDCM_Predation_Operator.py ########################################################################
	################################################################################################################################################################################################################

	def check_initial_population(self,return_report=False):
		"""
		This definition is responsible for making sure that the initialised population obeys the Predation Operator of interest.

		:param return_report: Will return a dict with all the information about what clusters are similar to what other clusters in the population. 
		:type  return_report: bool.

		returns:
			* **clusters_to_remove** (*list of ints*): a list of the clusters to remove from the population as they violate the Predation Operator. Format is [(index in population, name fo cluster),...]
			* **CNA_report** (*dict.*): a dictionary with information on the clusters being removed and the other clusters in the population which have caused the violation to the SCM Predation Operator. This information is only used to display information so they know why there are violations to the Predation Operator when they occur. For is {removed cluster: [list of clusters that this cluster is similar to in the population.]}
		
		"""
		if self.print_details:
			print('--------------------------------------')
			print('Checking Population of Same Structure')
			print('--------------------------------------')
			print('Update LoD database')
		self.update_LoD_database(self.population)
		if self.print_details:
			print('Update LoD database comparison')
		self.get_identical_structures_initial_population()
		if self.print_details:
			print('Get which clusters to remove from population due to being identical')
		clusters_to_remove, identical_structures = self.pop_identical_structures()		
		if self.print_details:
			print('Removing similar clusters in the Population.')
		self.remove_similar_clusters_in_population(clusters_to_remove)
		if self.print_details and not clusters_to_remove == []:
			print('Clusters in the Population Removed for being to similar: '+str([cluster_to_remove[1] for cluster_to_remove in clusters_to_remove]))
		self.check_database([self.population])#, clusters_to_remove)
		if return_report:
			return clusters_to_remove, identical_structures
		else:
			return clusters_to_remove

	def update_LoD_database(self, collection):
		"""
		This methos will add the collection to the LoD_database.

		:param collection: This is the collection to add to the LoD_database
		:type  collection: Organisms.GA.Population.Population or Organisms.GA.Offspring_Pool.Offspring_Pool

		"""
		atoms_format_clusters = Collection_and_Similarity_Settings_Iterator(collection, self.similarity_settings)
		start_time = time.time()
		with mp.Pool(processes=self.no_of_cpus) as pool:
			results = pool.map_async(self.get_structural_data_method, atoms_format_clusters)
			results.wait()
		data = results.get()
		end_time = time.time()
		print('Collecting Cluster LoD data took '+str(end_time - start_time)+' seconds.')
		for cluster_name, cluster_EDM in data:
			self.LoD_database[cluster_name] = cluster_EDM

	def get_identical_structures_initial_population(self):
		"""
		This method is designed to identify which clusters in the LoD_database (from the initial population) are identify using this method.

		This will place all the results from this into self.LoD_comparison_database 

		"""
		# Get a list of all the comparisions to make
		structures_to_compare = structures_in_LoD_database_Iterator(self.LoD_database, self.LoD_comparison_database, self.similarity_settings)
		# Perform all the comparisons in parallel
		start_time = time.time()
		with mp.Pool(processes=self.no_of_cpus) as pool:
			results = pool.map_async(self.check_if_two_clusters_are_identical_method, structures_to_compare)
			results.wait()
		data = results.get()
		end_time = time.time()
		print('Processing Cluster LoD comparisons Entries took '+str(end_time - start_time)+' seconds.')
		# Add the comparison information to self.LoD_comparison_database. 
		for compared_cluster_names, is_the_same_cluster in data:
			name1, name2 = compared_cluster_names
			self.LoD_comparison_database.add(name1, name2, is_the_same_cluster)

	def pop_identical_structures(self):
		"""
		This method will identify which clusters need to be removed from self.LoD_comparison_database based on being identical via this method, and will remove the entries of those clusters from self.LoD_database and self.LoD_comparison_database  
		
		returns:
			* **clusters_to_remove** (*list of ints*): a list of the clusters to remove from the population as they violate the Predation Operator. Format is [(index in population, name fo cluster),...]
			* **identical_structures_report** (*dict.*): a dictionary with information on the clusters being removed and the other clusters in the population which have caused the violation to the SCM Predation Operator. This information is only used to display information so they know why there are violations to the Predation Operator when they occur. For is {removed cluster: [list of clusters that this cluster is similar to in the population.]}
		
		"""
		######################################################################
		# Get the pairs of clusters that are indentical using this Predation Operator.
		identical_pairs = self.LoD_comparison_database.which_clusters_in_LoD_comparison_database_are_similar()
		#identical_pairs_copy = deepcopy(identical_pairs)
		list_of_identical_clusters = identical_pairs.keys()
		######################################################################
		# Get a list of all the clusters in the LoD_database and order then by fitness
		list_of_identical_clusters_ordered_by_fitness = []
		for cluster_name in list_of_identical_clusters:
			cluster = self.population.get_cluster_from_name(cluster_name)
			cluster_fitness = cluster.fitness
			list_of_identical_clusters_ordered_by_fitness.append((cluster_name,cluster_fitness))
		# order fitnesses,From highest to lowest
		list_of_identical_clusters_ordered_by_fitness.sort(key = lambda x: x[1], reverse=True) 
		if (not list_of_identical_clusters_ordered_by_fitness == []) and (not list_of_identical_clusters_ordered_by_fitness[0][1] >= list_of_identical_clusters_ordered_by_fitness[-1][1]):
			print('Error in def pop_identical_structures in class CNA_Diversity_Scheme, in Energy_Diversity_Scheme.py')
			print('The fitnesses after the sort are the wrong way around')
			print('list_of_identical_clusters_ordered_by_fitness[0][1] (fitness) = '+str(list_of_identical_clusters_ordered_by_fitness[0][1]))
			print('list_of_identical_clusters_ordered_by_fitness[-1][1] (fitness)= '+str(list_of_identical_clusters_ordered_by_fitness[-1][1]))
			print('The fitnesses need to be order from highest to lowest.')
			exit('Check this out. This program will finish without completing.')
		for index in range(len(list_of_identical_clusters_ordered_by_fitness)):
			cluster_name = list_of_identical_clusters_ordered_by_fitness[index][0]
			list_of_identical_clusters_ordered_by_fitness[index] = cluster_name
		######################################################################
		# This will determine which clusters should be deleted in such a way that the 
		# high fitness clusters are kepted, and the lower fitness clusters are removed.
		# It will also remove those lower fitness identical clusters from self.LoD_database
		clusters_to_remove = []
		identical_structures_report = {}
		index1 = 0
		while index1 < len(list_of_identical_clusters_ordered_by_fitness):
			clusters_to_keep_high_fitness = list_of_identical_clusters_ordered_by_fitness[index1]
			clusters_to_remove_low_fitness = list(identical_pairs[clusters_to_keep_high_fitness])
			for cluster_to_remove in clusters_to_remove_low_fitness:
				identical_structures_report.setdefault(clusters_to_keep_high_fitness,[]).append(cluster_to_remove)
				del self.LoD_database[cluster_to_remove]
				self.LoD_comparison_database.remove(cluster_to_remove)
				# --------------------------------------------- #
				del identical_pairs[cluster_to_remove]
				for key, value in identical_pairs.items():
					if cluster_to_remove in value:
						value.remove(cluster_to_remove)
						#if len(value) == 0:
						#	del identical_pairs[key]
				# --------------------------------------------- #
				clusters_to_remove.append(cluster_to_remove)
				list_of_identical_clusters_ordered_by_fitness.remove(cluster_to_remove)
			index1 += 1
		######################################################################
		return clusters_to_remove, identical_structures_report
		######################################################################

	def remove_similar_clusters_in_population(self,clusters_to_remove):
		"""
		This method will remove the similar clusters from the population.

		:param cluster_names_to_remove: A list of the names of all the clusters to remove from the CNA database
		:type  cluster_names_to_remove: list of ints

		"""
		for index in range(len(clusters_to_remove)):
			cluster_name = clusters_to_remove[index]
			index_pop = self.population.get_index(cluster_name)
			clusters_to_remove[index] = (index_pop,cluster_name)
		clusters_to_remove.sort(key = lambda cluster_to_remove: cluster_to_remove[0], reverse=False) # sort from lowest to highest index
		for cluster_to_remove in clusters_to_remove[::-1]: # remove from highest to lowest index (by doing clusters_to_remove[::-1])
			index_pop = cluster_to_remove[0]
			self.population.remove(index_pop)

	def check_database(self, collections):
		"""
		This method will check to make sure that all the clusters comparisons in the self.LoD_comparison_database are false

		I.e. check that all the clusters in the collections are not idenitcal

		:param collections: This is a list of all the Populations and Offspring_Pool in your genetic algorithm to check.
		:type  collections:  list of Organisms.GA.Collection.Collection

		"""
		total_length = 0
		for collection in collections:
			total_length += len(collection)
		#############################################
		if not total_length == len(self.LoD_database):
			print('Error in def Check_Initial_Population in Class IDCM_Predation_Operator, in IDCM_Predation_Operator.py')
			print('not len(collections) == len(self.EDM_database)')
			print('collections: '+str(collections))
			print('')
			for collection in collections:
				for cluster in collection:
					print(cluster.name)
				print('')
			print('')
			print('total_length = '+str(total_length))
			print('len(self.LoD_database)) = '+str(len(self.LoD_database)))
			print('Check this')
			import pdb; pdb.set_trace()
			exit('This program will exit without completing')
		#############################################
		self.LoD_comparison_database.are_all_entries_false([self.population])

	###########################################################################################################################################################
	########################## Methods Required for the def assess_for_violations, in the class Fitness_Factor, in Fitness_Factor.py ##########################
	###########################################################################################################################################################

	def assess_for_violations(self,offspring_pool,force_replace_pop_clusters_with_offspring):
		"""
		The offspring are assessed against clusters in the population. Offspring are removed from the offspring_pool if:
		1) They are geometrically the same as another offspring
		2) They are geometrically the same as another cluster in the population.

		Must return the clusters that have been removed from population and offspring_pool lists.

		:param offspring_pool: This is the collection of offspring to assess for violations to the Predation Operator.
		:type  offspring_pool: Organisms.GA.Offspring_Pool.Offspring_Pool
		:param force_replace_pop_clusters_with_offspring: This will tell the genetic algorithm whether to swap clusters in the population with offspring if the predation operator indicates they are the same but the predation operator has a better fitness value than the cluster in the population. 
		:type  force_replace_pop_clusters_with_offspring: bool.

		returns:
			* **offspring_to_remove** (*tuple of ints*): A list of the names of the offspring to be removed
			* **force_replacement** (*tuple of (int, int)*): A list of the clusters in the population that should be replaced, and the offspring they should be replaced by.

		"""
		if force_replace_pop_clusters_with_offspring:
			return self.assess_for_violations_force_replacement(offspring_pool)
		else:
			return self.assess_for_violations_no_force_replacement(offspring_pool)

	def assess_for_violations_no_force_replacement(self,offspring_pool):
		"""
		The offspring are assessed against clusters in the population. Offspring are removed from the offspring_pool if:
		1) They are geometrically the same as another offspring
		2) They are geometrically the same as another cluster in the population.

		Must return the clusters that have been removed from population and offspring_pool lists.

		:param offspring_pool: This is the collection of offspring to assess for violations to the Predation Operator.
		:type  offspring_pool: Organisms.GA.Offspring_Pool.Offspring_Pool

		returns:
			* **offspring_to_remove** (*tuple of ints*): A list of the names of the offspring to be removed
			* **force_replacement** (*tuple of (int, int)*): A list of the clusters in the population that should be replaced, and the offspring they should be replaced by.

		"""
		if self.print_details:
			print('**********************************************************')
			print('**********************************************************')
			print('Offspring removed from the Offspring Pool due to violating the Comprehensive Energy Diversity Scheme.')
			print('NOTE: energy difference minimum = '+str(self.minimum_energy_diff)+' eV.')
			print('**********************************************************')
			print('**********************************************************')
		########################################################################################################
		if self.print_details:
			print('Start assessing for IDCM Diversity')
		offspring_to_remove = []
		# Check offspring against themselves
		structures_to_consider = [Cluster_Block(offspring_pool,'Offspring',index) for index in range(len(offspring_pool))]
		structures_to_consider.sort(key=lambda cluster: cluster.fitness, reverse=False)
		index1 = 0
		while index1 < len(structures_to_consider):
			offspring1 = structures_to_consider[index1]
			for index2 in range(len(structures_to_consider)-1,index1,-1):
				offspring2 = structures_to_consider[index2]
				if self.LoD_comparison_database.LoD_Similarity_Analysis(offspring1.name,offspring2.name):
					offspring_to_remove.append((offspring2.name,offspring2.index))
					del structures_to_consider[index2]
			index1 += 1
		# check offspring against clusters in the populatino
		for index in range(len(structures_to_consider)):
			offspring = structures_to_consider[index]
			for cluster_in_population in self.population:
				if self.LoD_comparison_database.LoD_Similarity_Analysis(offspring.name,cluster_in_population.name):
					offspring_to_remove.append((offspring.name,offspring.index))
					break
		# Sort by index and continue on
		offspring_to_remove.sort(key=lambda x:x[1],reverse=True)
		force_replacement = []
		return offspring_to_remove, force_replacement

	def assess_for_violations_force_replacement(self,offspring_pool):
		"""
		The offspring are assessed against clusters in the population. Offspring are removed from the offspring_pool if:
		1) They are geometrically the same as another offspring
		2) They are geometrically the same as another cluster in the population.

		Must return the clusters that have been removed from population and offspring_pool lists.

		:param offspring_pool: This is the collection of offspring to assess for violations to the Predation Operator.
		:type  offspring_pool: Organisms.GA.Offspring_Pool.Offspring_Pool

		returns:
			* **offspring_to_remove** (*tuple of ints*): A list of the names of the offspring to be removed
			* **force_replacement** (*tuple of (int, int)*): A list of the clusters in the population that should be replaced, and the offspring they should be replaced by.

		"""
		if self.print_details:
			print('------------------------------------------------------')
			print('Assessing the clusters in the offspring to decide if:')
			print('\t* offspring are geometrically similar to other offspring.')
			print('\t* offspring are geometrically similar to clusters in the population.')
			print('------------------------------------------------------')
			####################################################################################################
			print('Starting Sorting pop and off by fitness')
		all_clusters_sorted_by_expected_fitness = [Cluster_Block(self.population,'Population',index) for index in range(len(self.population))] + [Cluster_Block(offspring_pool,'Offspring',index) for index in range(len(offspring_pool))]
		# order fitnesses,From highest to lowest
		all_clusters_sorted_by_expected_fitness.sort(key=lambda cluster: cluster.fitness,reverse=True)
		if (not all_clusters_sorted_by_expected_fitness == []) and (not all_clusters_sorted_by_expected_fitness[0].fitness >= all_clusters_sorted_by_expected_fitness[-1].fitness):
			print('Error in def assess_for_violations in class CNA_Diversity_Scheme, in Energy_Diversity_Scheme.py')
			print('The fitnesses after the sort are the wrong way around')
			print('structures_to_consider[0].fitness = '+str(structures_to_consider[0].fitness))
			print('structures_to_consider[-1].fitness = '+str(structures_to_consider[-1].fitness))
			print('The fitnesses need to be order from highest to lowest.')
			exit('Check this out. This program will finish without completing.')
		if self.print_details:
			print('Finishing Sorting pop and off by fitness')
			####################################################################################################
			# Follows same rough algorithm guide as the comprehensive energy Predation Operator
			print('Start assessing for LoD Predation')
		index_higher = 0
		swap_cluster_in_pop_with_offspring = []; offspring_to_remove_due_to_pop = []; offspring_to_remove_due_to_other_offspring = []
		offspring_to_remove_as_too_many_pop_in_similar_common = []
		# scan though all the clusters in offspring and population in order of fitness
		while index_higher < len(all_clusters_sorted_by_expected_fitness):
			################################################################################################################
			incountered_population_counter = 0
			cluster_higher = all_clusters_sorted_by_expected_fitness[index_higher]
			one_instance_of_swap_cluster_in_pop_with_offspring = []
			offspring_to_remove_due_to_pop_temp = []
			offspring_to_remove_as_too_many_pop_in_similar_common_temp = []
			offspring_to_remove_due_to_other_offspring_temp = []
			# scan though all the other clusters which have higher fitnesses
			indices_to_delete = []
			for index_lower in range(index_higher+1, len(all_clusters_sorted_by_expected_fitness)):
				cluster_lower = all_clusters_sorted_by_expected_fitness[index_lower]
				############################################################################################################
				if self.LoD_comparison_database.LoD_Similarity_Analysis(cluster_higher.name,cluster_lower.name):   
					# The two clusters being looked at at the moment are geometrically the same. 
					if cluster_higher.collection_type == 'Population':
						# if two clusters in the population are geometrically similar, we have an issue.
						if cluster_lower.collection_type == 'Population':
							print('Error')
							import pdb; pdb.set_trace()
							exit()
						# If a cluster in the population (and has a higher fitness) is geometrically similar to an offspring,
						# then it is better to keep the offspring and remove the offspring
						elif cluster_lower.collection_type == 'Offspring':
							offspring_to_remove_due_to_pop_temp.append([cluster_lower,cluster_higher])
					elif cluster_higher.collection_type == 'Offspring':
						# If an offspring is geometrically similar (and has a higher fitness) to a cluster in population,
						# then it is better to replace this cluster in the population with this offspring.
						if cluster_lower.collection_type == 'Population':
							# Take the lowest fitness cluster in the population to swap with this offspring.
							if one_instance_of_swap_cluster_in_pop_with_offspring == []:
								one_instance_of_swap_cluster_in_pop_with_offspring = [[cluster_lower,cluster_higher]]
							else:
								cluster_lower_old, cluster_higher_old = one_instance_of_swap_cluster_in_pop_with_offspring[0]
								if not cluster_higher_old.name == cluster_higher.name:
									exit('Somethings up')
								offspring_to_remove_as_too_many_pop_in_similar_common_temp.append([cluster_higher,[cluster_lower_old,cluster_lower]])
								one_instance_of_swap_cluster_in_pop_with_offspring = []; indices_to_delete = []
								break
						# If an offspring is geometrically similar (and has a higher fitness) to an offspring,
						# remove the higher fitness offspring
						elif cluster_lower.collection_type == 'Offspring':
							offspring_to_remove_due_to_other_offspring_temp.append([cluster_lower,cluster_higher])
					indices_to_delete.append(index_lower)
			################################################################################################################
			if not offspring_to_remove_as_too_many_pop_in_similar_common_temp == []:
				offspring_to_remove_as_too_many_pop_in_similar_common += offspring_to_remove_as_too_many_pop_in_similar_common_temp
				del all_clusters_sorted_by_expected_fitness[index_higher]
			else:
				offspring_to_remove_due_to_pop += offspring_to_remove_due_to_pop_temp
				offspring_to_remove_due_to_other_offspring += offspring_to_remove_due_to_other_offspring_temp
				swap_cluster_in_pop_with_offspring += one_instance_of_swap_cluster_in_pop_with_offspring
				for index_lower in sorted(indices_to_delete,reverse=True): # remove from highest to lowest index
					del all_clusters_sorted_by_expected_fitness[index_lower]
				index_higher += 1
			################################################################################################################
		########################################################################################################
		########################################################################################################
		# remove offspring that violate the comprehensive Predation method as it has a higher energy, but within 
		# self.minimum_energy_diff, with other offspring or other clusters in the population.
		if self.print_details:
			print('Finished assessing for LoD Predation')
			print('Start deleting offspring')
		all_clusters_to_be_removed_here = offspring_to_remove_due_to_pop+offspring_to_remove_due_to_other_offspring+offspring_to_remove_as_too_many_pop_in_similar_common
		offspring_to_remove = []
		for off_to_remove, pop_to_keep in sorted(all_clusters_to_be_removed_here,key=lambda x:x[0].index,reverse=True): # remove from highest to lowest index
			if offspring_pool[off_to_remove.index].name in [offspring.name for cluster,offspring in swap_cluster_in_pop_with_offspring]:
				print('Error in def assess_for_violations, in class IDCM_Predation_Operator, in IDCM_Predation_Operator.py')
				print('Somehow, this algorithm has identified a structure to be in the offspring_pool and the population')
				print('The structure can only be in either the offspring pool or population.')
				print('Offspring: '+str(offspring_pool[off_to_remove.index].name))
				print('Check this out')
				import pdb; pdb.set_trace()
				exit('This program will end without completing.')
			off_index = off_to_remove.index
			off_name  = offspring_pool[off_index].name
			offspring_to_remove.append((off_name,off_index))
			###############################################################################
			#name_to_remove = offspring_pool[off_to_remove.index].name
			#del self.LoD_database[name_to_remove]
			#self.LoD_comparison_database.remove(name_to_remove)
			###############################################################################
		###############################################################################
		if self.print_details:
			self.assess_for_violations_message(swap_cluster_in_pop_with_offspring,offspring_to_remove_as_too_many_pop_in_similar_common,offspring_to_remove_due_to_pop,offspring_to_remove_due_to_other_offspring)
		###############################################################################
		# Deal with the offspring that you would like to swap with clusters in the population.
		force_replacement = []
		#print(swap_cluster_in_pop_with_offspring)
		for pop_to_swap_out, off_to_swap_in in swap_cluster_in_pop_with_offspring:
			if not off_to_swap_in.name in offspring_pool.get_cluster_names():
				print('temp error in CNA_version_3.py')
				import pdb; pdb.set_trace()
				exit()
			#off_to_swap_in_index = offspring_pool.get_index(off_to_swap_in.name)
			force_replacement.append((pop_to_swap_out.name,off_to_swap_in.name))
		force_replacement.sort(key=lambda x:x[1],reverse=True) # force replace from highest to lowest index
		#for pop_to_swap_out_name, off_to_swap_in_name in force_replacement:
		#	print(off_to_swap_in_name)
		return offspring_to_remove, force_replacement
		########################################################################################################

	def structures_to_compare_generator(self,offspring_pool):
		for offspring in offspring_pool:
			offspring_name = offspring.name
			for cluster_pop in self.population:
				cluster_pop_name = cluster_pop.name
				yield (offspring_name, cluster_pop_name, self.LoD_database[offspring_name],self.LoD_database[cluster_pop_name],self.similarity_settings)
		for index1 in range(len(offspring_pool)):
			off1_name = offspring_pool[index1].name
			for index2 in range(index1+1,len(offspring_pool)):
				off2_name = offspring_pool[index2].name
				yield (off1_name, off2_name, self.LoD_database[off1_name],self.LoD_database[off2_name],self.similarity_settings)

	def get_identical_structures_generation(self,offspring_pool):
		structures_to_compare = self.structures_to_compare_generator(offspring_pool)
		###############
		start_time = time.time()
		with mp.Pool(processes=self.no_of_cpus) as pool:
			results = pool.map_async(self.check_if_two_clusters_are_identical_method, structures_to_compare)
			results.wait()
		data = results.get()
		end_time = time.time()
		print('Processing Cluster LoD comparisons Entries took '+str(end_time - start_time)+' seconds.')
		for compared_cluster_names, is_the_same_cluster in data:
			name1, name2 = compared_cluster_names
			self.LoD_comparison_database.add(name1, name2, is_the_same_cluster)

	def assess_for_violations_message(self,swap_cluster_in_pop_with_offspring,offspring_to_remove_as_too_many_pop_in_similar_common,offspring_to_remove_due_to_pop,offspring_to_remove_due_to_other_offspring):
		"""
		This method will tell the information that offspring are removed or replaced and why. 

		:param swap_cluster_in_pop_with_offspring: The clusters in the population to swap out, and the offspring to swap in its place. These will be replaced because the offspring has a higher fitness than the cluster in the population, even though they are similar. 
		:type  swap_cluster_in_pop_with_offspring: tuple of (Organisms.GA.SCM_Predation_Operator.Cluster_Block, Organisms.GA.SCM_Predation_Operator.Cluster_Block)
		:param offspring_to_remove_as_too_many_pop_in_similar_common: Remove offspring because there are too many similar clusters to it in the population already. 
		:type  offspring_to_remove_as_too_many_pop_in_similar_common: tuple of (Organisms.GA.SCM_Predation_Operator.Cluster_Block, Organisms.GA.SCM_Predation_Operator.Cluster_Block)
		:param offspring_to_remove_due_to_pop: Remove offspring because they are similar to a cluster in the population. These offspring are less fit than their similar counterparts in the population. 
		:type  offspring_to_remove_due_to_pop: tuple of (Organisms.GA.SCM_Predation_Operator.Cluster_Block, Organisms.GA.SCM_Predation_Operator.Cluster_Block)
		:param offspring_to_remove_due_to_other_offspring: Remove offpsring because they are similar to other clusters in the Offspring_Pool. This offspring is less fit than their similar counterparts in the offspring_pool. 
		:type  offspring_to_remove_due_to_other_offspring: tuple of (Organisms.GA.SCM_Predation_Operator.Cluster_Block, Organisms.GA.SCM_Predation_Operator.Cluster_Block)

		"""
		########################################################################################################
		# Mention offspring that have been removed and due to having a similar energy to which cluster in the population
		# Error with this one
		print('1. Clusters in the Population that have been replaced by Offspring, due to the cluster in the offspring being geometrically similar and having a lower fitness than a offspring.')
		if len(swap_cluster_in_pop_with_offspring) > 0:
			print('1. Clusters in the Population that have been replaced by Offspring, due to the cluster in the offspring being geometrically similar and having a lower fitness than a offspring.')
			for pop_to_swap_out, off_to_swap_in in sorted(swap_cluster_in_pop_with_offspring,key=lambda x:x[1].name,reverse=False):
				cp_removed_name = pop_to_swap_out.name; cp_removed_fitness = pop_to_swap_out.fitness; cp_removed_energy = pop_to_swap_out.energy
				off_swapped_in_name = off_to_swap_in.name; off_swapped_in_fitness = off_to_swap_in.fitness; off_swapped_in_energy = off_to_swap_in.energy
				print(' --> Population Cluster removed '+str(cp_removed_name)+' (Energy: '+str(round(cp_removed_energy,6))+' eV; fitness: '+str(round(cp_removed_fitness,6))+') {Replaced with Offspring '+str(off_swapped_in_name)+' (Energy: '+str(round(off_swapped_in_energy,6))+' eV; fitness: '+str(round(off_swapped_in_fitness,6))+')}.')
		else:
			print('1. No clusters in the population have been replaced by offspring in the offspring_pool list')
		print('*****************************')
		########################################################################################################
		# Mention offspring that have been removed and due to having a similar energy to which cluster in the population
		print('2. These offspring have a better fitness and are geometrically similar to two or more clusters in the population.')
		if len(offspring_to_remove_as_too_many_pop_in_similar_common) > 0:
			print('2. These offspring have a better fitness and are geometrically similar to two or more clusters in the population.')
			print('   Therefore it is best to remove the offspring to avoid having geometrically similar clusters in the population.')
			print('   Below are the offspring that will be removed and the clusters in the population they are geometrically similar to.')
			for off_to_swap_out, geo_sim_pops in sorted(offspring_to_remove_as_too_many_pop_in_similar_common,key=lambda x:x[0].name,reverse=False):
				off_removed_name = off_to_swap_out.name; off_removed_fitness = off_to_swap_out.fitness; off_removed_energy = off_to_swap_out.energy
				geo_sim_pop1, geo_sim_pop2 = geo_sim_pops
				geo_sim_pop1_name = geo_sim_pop1.name; geo_sim_pop1_fitness = geo_sim_pop1.fitness; geo_sim_pop1_energy = geo_sim_pop1.energy
				geo_sim_pop2_name = geo_sim_pop2.name; geo_sim_pop2_fitness = geo_sim_pop2.fitness; geo_sim_pop2_energy = geo_sim_pop2.energy
				print(' --> Offspring removed '+str(off_removed_name)+' (Energy: '+str(round(off_removed_energy,6))+' eV; fitness: '+str(round(off_removed_fitness,6))+') {Geometrically similar to (at least) clusters in population: '+str(geo_sim_pop1_name)+' (Energy: '+str(round(geo_sim_pop1_energy,6))+' eV; fitness: '+str(round(geo_sim_pop1_fitness,6))+')} and '+str(geo_sim_pop2_name)+' (Energy: '+str(round(geo_sim_pop2_energy,6))+' eV; fitness: '+str(round(geo_sim_pop2_fitness,6))+')}.')
		else:
			print('2. No offspring need to be removed from the offspring_pool list')
		print('*****************************')
		########################################################################################################
		# Mention offspring that have been removed and due to having a similar energy to which cluster in the population
		print('3. The following offspring were removed from the offspring pool (and because they are geometrically similar and have a lower fitness to which cluster in the population):')
		if len(offspring_to_remove_due_to_pop) > 0:
			print('3. The following offspring were removed from the offspring pool (and because they are geometrically similar and have a lower fitness to which cluster in the population):')
			for offspring_removed, cp_due_to in offspring_to_remove_due_to_pop:
				offspring_removed_name = offspring_removed.name; offspring_removed_fitness = offspring_removed.fitness; offspring_removed_energy = offspring_removed.energy
				cp_due_to_name = cp_due_to.name; cp_due_to_fitness = cp_due_to.fitness; cp_due_to_energy = cp_due_to.energy
				print(' --> Offspring '+str(offspring_removed_name)+' (Energy: '+str(offspring_removed_energy)+' eV; fitness: '+str(round(offspring_removed_fitness,6))+') {Similar to Population Cluster '+str(cp_due_to_name)+' (Energy: '+str(round(cp_due_to_energy,6))+' eV; fitness: '+str(round(cp_due_to_fitness,6))+')}.')
		else:
			print('3. No offspring need to be removed from the offspring_pool list')
		print('*****************************')
		########################################################################################################
		# Mention offspring that have been removed and due to having a similar energy to which other offspring in the Offspring_Pool
		print('4. Offspring that have have been removed for being geometrically similar and have a lower fitness to the rest of the other Offspring')
		if len(offspring_to_remove_due_to_other_offspring) > 0:
			print('4. Offspring that have have been removed for being geometrically similar and have a lower fitness to the rest of the other Offspring')
			for offspring_removed, due_to_offspring in offspring_to_remove_due_to_other_offspring:
				offspring_removed_name = offspring_removed.name; offspring_removed_fitness = offspring_removed.fitness; offspring_removed_energy = offspring_removed.energy
				due_to_offspring_name = due_to_offspring.name; due_to_offspring_fitness = due_to_offspring.fitness; due_to_offspring_energy = due_to_offspring.energy
				print(' --> Offspring '+str(offspring_removed_name)+' (Energy: '+str(offspring_removed_energy)+'eV; fitness: '+str(round(offspring_removed_fitness,6))+') {Similar to Offspring '+str(due_to_offspring_name)+' (Energy: '+str(due_to_offspring_energy)+' eV; fitness: '+str(round(due_to_offspring_fitness,6))+')}.')
		else:
			print('4. No offspring have been removed from the rest of the offspring_pool list for being too similar')
		print('**********************************************************')
		print('**********************************************************')
		########################################################################################################

	###########################################################################################################################################################
	########################## Methods Required for the def assess_for_violations, in the class Fitness_Factor, in Fitness_Factor.py ##########################
	###########################################################################################################################################################

	def update_database_after_natural_selection(self,offspring_not_accepted):
		for offspring_name in offspring_not_accepted:
			del self.LoD_database[offspring_name]
			self.LoD_comparison_database.remove(offspring_name)
		if not sorted(self.population.get_cluster_names()) == sorted(self.LoD_database.keys()):
			print('Error')
			import pdb; pdb.set_trace()
			exit()
		if not sorted(self.population.get_cluster_names()) == sorted(self.LoD_comparison_database.keys()):
			print('Error')
			import pdb; pdb.set_trace()
			exit()

	def reset(self):
		self.LoD_database = {}
		self.LoD_comparison_database.reset()

	########################################################################################################
	########################################################################################################
	########################################################################################################

	def add_to_database(self, collection):
		self.update_LoD_database(collection)
		self.get_identical_structures_generation(collection)

	def remove_from_database(self, cluster_names_to_remove):
		for cluster_name in cluster_names_to_remove:
			del self.LoD_database[cluster_name]
			self.LoD_comparison_database.remove(cluster_name)
		self.check_for_issues()

	########################################################################################################
	########################################################################################################
	########################################################################################################

	def check_for_issues(self):
		self.LoD_comparison_database.check_for_issues(self.population)




