import os
import numpy as np
from copy import deepcopy
from Organisms.GA.Predation_Operators.Predation_Operator import Predation_Operator
from Organisms.GA.SCM_Scripts.CNA_Database import CNA_Database
from Organisms.GA.SCM_Scripts.SCM_initialisation import get_SCM_methods, get_rCut_values, get_rCuts

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

class SCM_Predation_Operator(Predation_Operator):
	"""
	This predation operator uses the similarities from the SCM to determine whether to exclude clusters from the population because they are too similar to each other.	

	:param Predation_Information: This contains all the information needed by the Predation Operator you want to use to run.
	:type  Predation_Information: dict.
	:param fitness_information: This is all the settings needed for the SCM predation operator. This is needed if the fitness operator is the structure + energy fitness operator, where the CNA Database maybe the same database for the predation and fitness operator.
	:type  fitness_information: dict.
	:param population: This is the population that this Operator will be controlling to make sure that no two clusters in the population have the same energy.
	:type  population: Organisms.GA.Population
	:param no_of_cpus: This is the number of cpus to use.
	:type  no_of_cpus: int
	:param print_details: Print details of the predation operator, like verbose
	:type  print_details: bool

	"""
	def __init__(self,Predation_Information,fitness_information,population,no_of_cpus,print_details): #,no_generations):
		super().__init__(Predation_Information,population,print_details)
		#self.does_population_need_after_natural_selection_processing = True
		print('######################################################')
		print('SCM Based Predation Algorithm')
		print('')
		############################################################
		# Check the Predation Operator is the correct one for this Predation Operator.
		if not Predation_Information['Predation Operator'] == 'SCM':
			print('Error in class SCM_Predation_Operator, in SCM_Predation_Operator.py')
			print('The Predation Operator "SCM_Predation_Operator" has been initialised.')
			print("However, Predation_Information['Predation Operator'] is not 'SCM'")
			print("Predation_Information['Predation Operator'] = "+str(Predation_Information['Predation Operator']))
			print('Check this out.')
			import pdb; pdb.set_trace()
			exit()
		############################################################
		# Determine which SCM Scheme to use, either the AC-SRA or the TC-SRA.
		self.SCM_Scheme = Predation_Information['SCM Scheme']
		if not self.SCM_Scheme in ['A-SCM','T-SCM']:
			print('Error in class SCM_Predation_Scheme, in SCM_Predation_Scheme.py')
			print('The "SCM_Scheme" option should be either "A-SCM" or "T-SCM"')
			print('You have entered '+str(self.SCM_Scheme))
			print('Check this.')
			exit('This program will finish without running.')
		get_CNA_profile, get_CNA_similarities = get_SCM_methods(self.SCM_Scheme)
		get_cna_profile_method = get_CNA_profile
		get_cna_similarities_method = get_CNA_similarities
		############################################################
		# Get the geometrically similar cut off percentage.
		try:
			self.cut_off_similarity = Predation_Information['Cut_off']
		except:
			self.cut_off_similarity = 100.0
		############################################################
		# Obtain the values for values of rCut to scan across and get the values of rCut the user wishes to investigate
		self.rCuts = get_rCuts(self,Predation_Information)
		############################################################
		# Debugging switch
		if not 'debug' in Predation_Information:
			self.debug = True
		else:
			self.debug = Predation_Information['debug']
		####################################################################################
		# setup the CNA_Database for recording CNA profiles and similarity profiles.
		self.cna_database = CNA_Database(self.rCuts,self.population,self.cut_off_similarity,get_cna_profile_method,get_cna_similarities_method,no_of_cpus,self.debug)
		####################################################################################
		#if not 'Use Same CNA Database' in fitness_information:
		#	fitness_information['Use Same CNA Database'] = False
		if fitness_information['Fitness Operator'] == 'SCM + Energy' and fitness_information['Use Predation Information'] == True:
			self.use_same_CNA_database = True
		else:
			self.use_same_CNA_database = False

	###########################################################################################################
	########################## Methods Required for the def check_initial_population ##########################
	###########################################################################################################

	def check_initial_population(self,return_report=False):
		"""
		This definition is responsible for making sure that the initialised population obeys the CNA Predation Operator. 

		:param return_report: Will return a dict with all the information about what clusters are similar to what other clusters in the population. 
		:type  return_report: bool.

		returns:
			* **clusters_to_remove** (*list of ints*): a list of the clusters to remove from the population as they violate the Predation Operator. Format is [(index in population, name fo cluster),...]
			* **CNA_report** (*dict.*): a dictionary with information on the clusters being removed and the other clusters in the population which have caused the violation to the SCM Predation Operator. This information is only used to display information so they know why there are violations to the Predation Operator when they occur. For is {removed cluster: [list of clusters that this cluster is similar to in the population.]}
		
		"""
		###############################################################################
		# First, the CNA_Database is built from the clusters that are in the newly inialised population.
		# 1.1 - get the 
		if self.use_same_CNA_database == False:
			self.cna_database.add(self.population,initialise=True)
		###############################################################################
		if return_report:
			clusters_to_remove, CNA_report = self.get_similar_clusters_to_remove(return_report)
		else:
			clusters_to_remove = self.get_similar_clusters_to_remove(return_report)
		###############################################################################
		# SECOND: Sort and remove cluster from the population and the cna_database for being geometrically similar.
		clusters_to_remove.sort(key=lambda x:x[0], reverse=False) # sort index from lowest to highest
		to_removes = []
		for pop_index_to_remove, name_to_remove in clusters_to_remove[::-1]: #remove index from highest to lowest
			self.population.remove(pop_index_to_remove)
			to_removes.append(name_to_remove)
		self.cna_database.remove(to_removes) # delete the cluster entrance in the self.cna_database
		###############################################################################
		# Return the information, depending on the value fo return_report
		if return_report:
			return clusters_to_remove, CNA_report
		else:
			return clusters_to_remove
		###############################################################################

	def get_similar_clusters_to_remove(self,return_report):
		"""
		Will update the CNA_Database and return all the names of clusters in the population that violate the SCM predation operator

		:param return_report: Will return a dict with all the information about what clusters are similar to what other clusters in the population. 
		:type  return_report: bool.

		"""
		# Determine which clusters are too similar to other clusters in the population.
		# This will give a dictionary which is written by {cluster_dir: [list of other clusters that are geometrically similar to this cluster_dir]}
		geometrically_similar_clusters = self.cna_database.get_similar_clusters_in_database()
		###############################################################################
		# convert geometrically_similar_clusters to list and order clusters based on their energies
		geometrically_similar_clusters = list(map(list, geometrically_similar_clusters.items())) # given as [[dir, list of sim clusters, dir fitness]]
		for index in range(len(geometrically_similar_clusters)):
			cluster_name = geometrically_similar_clusters[index][0]
			cluster_fitness = self.population.get_cluster_from_name(cluster_name).fitness
			geometrically_similar_clusters[index].append(cluster_fitness)
		###############################################################################
		# sort geometrically_similar_clusters by the fitness of the cluster
		# order fitnesses,From highest to lowest
		geometrically_similar_clusters.sort(key=lambda x:x[2], reverse=True)
		if (not geometrically_similar_clusters == []) and (not geometrically_similar_clusters[0][2] >= geometrically_similar_clusters[-1][2]):
			print('Error in def get_similar_clusters_to_remove in class CNA_Diversity_Scheme, in Energy_Diversity_Scheme.py')
			print('The fitnesses after the sort are the wrong way around')
			print('geometrically_similar_clusters[0][2] (fitness) = '+str(geometrically_similar_clusters[0][2]))
			print('geometrically_similar_clusters[-1][2] (fitness)= '+str(geometrically_similar_clusters[-1][2]))
			print('The fitnesses need to be order from highest to lowest.')
			exit('Check this out. This program will finish without completing.')
		###############################################################################
		if return_report: # make a record of clusters that were kepted, as well as the other clusters that were removed for being geometrically similar.
			CNA_report = {}
		clusters_to_remove = []
		index1 = 0
		while index1 < len(geometrically_similar_clusters):
		#for index1 in range(len(geometrically_similar_clusters)):
			cluster_name, other_cluster_names_similar_too, fitness_NOTUSED = geometrically_similar_clusters[index1]
			if return_report:
				CNA_report[cluster_name] = deepcopy(other_cluster_names_similar_too)
			for name_to_remove in other_cluster_names_similar_too:
				clusters_to_remove.append([self.population.get_index(name_to_remove),name_to_remove]) 
				# remove every instance of name_to_remove in rest of geometrically_similar_clusters.
				for index2 in range(len(geometrically_similar_clusters)-1,index1,-1):
					if name_to_remove == geometrically_similar_clusters[index2][0]:
						del geometrically_similar_clusters[index2]
					elif name_to_remove in geometrically_similar_clusters[index2][1]:
						geometrically_similar_clusters[index2][1].remove(name_to_remove)
			index1 += 1
		###############################################################################
		if return_report:
			return clusters_to_remove, CNA_report
		else:
			return clusters_to_remove

	########################################################################################################
	########################## Methods Required for the def assess_for_violations ##########################
	########################################################################################################

	def assess_for_violations(self,offspring_pool,force_replace_pop_clusters_with_offspring):
		"""
		This definition is designed to determine which offspring (and the clusters in the population) violate the Predation Operator. 
		It will not remove or change any clusters in the offspring or population, but instead will record which offspring violate the 
		Predation Operator. 

		It will return two tuples with nothing in them, as required by this def. 

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
		This definition is designed to determine which offspring (and the clusters in the population) violate the Predation Operator. 
		It will not remove or change any clusters in the offspring or population, but instead will record which offspring violate the 
		Predation Operator. 

		It will return two tuples with nothing in them, as required by this def. 

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
			print('Start assessing for SCM Diversity')
		offspring_to_remove = []
		# Check offspring against themselves
		structures_to_consider = [Cluster_Block(offspring_pool,'Offspring',index) for index in range(len(offspring_pool))]
		structures_to_consider.sort(key=lambda cluster: cluster.fitness, reverse=False)
		index1 = 0
		while index1 < len(structures_to_consider):
			offspring1 = structures_to_consider[index1]
			for index2 in range(len(structures_to_consider)-1,index1,-1):
				offspring2 = structures_to_consider[index2]
				if self.cna_database.get_max_similarity(offspring1.name,offspring2.name) >= self.cut_off_similarity:
					offspring_to_remove.append((offspring2.name,offspring2.index))
					del structures_to_consider[index2]
			index1 += 1
		# check offspring against clusters in the populatino
		for index in range(len(structures_to_consider)):
			offspring = structures_to_consider[index]
			for cluster_in_population in self.population:
				if self.cna_database.get_max_similarity(offspring.name,cluster_in_population.name) >= self.cut_off_similarity:
					offspring_to_remove.append((offspring.name,offspring.index))
					break
		# Sort by index and continue on
		offspring_to_remove.sort(key=lambda x:x[1],reverse=True)
		force_replacement = []
		return offspring_to_remove, force_replacement

	def assess_for_violations_force_replacement(self,offspring_pool):
		"""
		This definition is designed to determine which offspring (and the clusters in the population) violate the Predation Operator. 
		It will not remove or change any clusters in the offspring or population, but instead will record which offspring violate the 
		Predation Operator. 

		It will return two tuples with nothing in them, as required by this def. 

		:param offspring_pool: This is the collection of offspring to assess for violations to the Predation Operator.
		:type  offspring_pool: Organisms.GA.Offspring_Pool.Offspring_Pool

		returns:
			* **offspring_to_remove** (*tuple of ints*): A list of the names of the offspring to be removed
			* **force_replacement** (*tuple of (int, int)*): A list of the clusters in the population that should be replaced, and the offspring they should be replaced by.

		"""
		###############################################################################
		# If you are using a different fitness Operator and different CNA parameters, you will
		# need to add the offspring in the offspring_pool to the self.cna_database
		#if self.use_same_CNA_database == False:
		#	self.cna_database.add(offspring_pool,initialise=False)
		########################################################################################################
		if self.print_details:
			print('Assessing which structures to remove to comply with SCM Predation Operator')
		structures_to_consider = [Cluster_Block(self.population,'Population',index) for index in range(len(self.population))] 
		structures_to_consider += [Cluster_Block(offspring_pool,'Offspring',index) for index in range(len(offspring_pool))]
		# order fitnesses,From highest to lowest
		structures_to_consider.sort(key=lambda cluster: cluster.fitness, reverse=True)
		if (not structures_to_consider == []) and (not structures_to_consider[0].fitness >= structures_to_consider[-1].fitness):
			print('Error in def assess_for_violations in class CNA_Diversity_Scheme, in Energy_Diversity_Scheme.py')
			print('The fitnesses after the sort are the wrong way around')
			print('geometrically_similar_clusters[0].fitness = '+str(structures_to_consider[0].fitness))
			print('geometrically_similar_clusters[-1].fitness= '+str(structures_to_consider[-1].fitness))
			print('The fitnesses need to be order from highest to lowest.')
			exit('Check this out. This program will finish without completing.')
		########################################################################################################
		########################################################################################################
		# Follows same rough algorithm guide as the comprehensive energy Predation Operator
		if self.print_details:
			print('Start assessing')
		index_higher = 0
		removal_O_P = []; removal_O_O = []
		swap_P_O = []; 
		remove_O_similar_to_too_many_P = []
		# scan though all the clusters in offspring and population in order of fitness
		while index_higher < len(structures_to_consider):
			################################################################################################################
			incountered_population_counter = 0
			cluster_higher = structures_to_consider[index_higher]
			one_instance_of_swap_P_O = []
			removal_O_P_temp = []
			remove_O_similar_to_too_many_P_temp = []
			removal_O_O_temp = []
			# scan though all the other clusters which have higher fitnesses
			indices_to_delete = []
			for index_lower in range(index_higher+1, len(structures_to_consider)):
				cluster_lower = structures_to_consider[index_lower]
				############################################################################################################
				#if self.CNA_database.CNA_Analysis(cluster_higher.dir,cluster_lower.dir) == 'geometric':
				if self.cna_database.get_max_similarity(cluster_higher.name,cluster_lower.name) >= self.cut_off_similarity:
					# The two clusters being looked at at the moment are geometrically the same. 
					if cluster_higher.collection_type == 'Population':
						# if two clusters in the population are geometrically similar, we have an issue.
						if cluster_lower.collection_type == 'Population':
							print('Error in def assess_for_violations in class SCM_Predation_Operator, in SCM_Predation_Operator.py')
							print('Two of the clusters in the population are identical by the max  similarity cutt off setting.')
							print('cluster_higher: '+str(cluster_higher))
							print('cluster_lower: '+str(cluster_lower))
							import pdb; pdb.set_trace()
							exit('This program will exit without completing.')
						# If a cluster in the population (and has a higher fitness) is geometrically similar to an offspring,
						# then it is better to keep the offspring and remove the offspring
						elif cluster_lower.collection_type == 'Offspring':
							removal_O_P_temp.append([cluster_lower,cluster_higher])
					elif cluster_higher.collection_type == 'Offspring':
						# If an offspring is geometrically similar (and has a higher fitness) to a cluster in population,
						# then it is better to replace this cluster in the population with this offspring.
						if cluster_lower.collection_type == 'Population':
							# Take the lowest fitness cluster in the population to swap with this offspring.
							if one_instance_of_swap_P_O == []:
								one_instance_of_swap_P_O = [[cluster_lower,cluster_higher]]
							else:
								cluster_lower_old, cluster_higher_old = one_instance_of_swap_P_O[0]
								if not cluster_higher_old.name == cluster_higher.name:
									exit('Somethings up')
								remove_O_similar_to_too_many_P_temp.append([cluster_higher,[cluster_lower_old,cluster_lower]])
								one_instance_of_swap_P_O = []; indices_to_delete = []
								break
						# If an offspring is geometrically similar (and has a higher fitness) to an offspring,
						# remove the higher fitness offspring
						elif cluster_lower.collection_type == 'Offspring':
							removal_O_O_temp.append([cluster_lower,cluster_higher])
					indices_to_delete.append(index_lower)
			# Add the relavent clusters to the various lists. 
			if not remove_O_similar_to_too_many_P_temp == []:
				remove_O_similar_to_too_many_P += remove_O_similar_to_too_many_P_temp
				del structures_to_consider[index_higher]
			else:
				removal_O_P += removal_O_P_temp
				removal_O_O += removal_O_O_temp
				swap_P_O += one_instance_of_swap_P_O
				for index_lower in sorted(indices_to_delete,reverse=True): # remove from highest to lowest index
					del structures_to_consider[index_lower]
				index_higher += 1
		####################################################################################################################
		# write the list offspring_to_remove that contains all the clusters to be removed from the offspring.
		print('Removing offspring that violate the SCM Predation Operator')
		offspring_to_remove = []
		for off_to_remove, pop_to_keep in sorted(removal_O_P+removal_O_O+remove_O_similar_to_too_many_P,key=lambda x:x[0].index,reverse=True): # remove from highest to lowest index
			if offspring_pool[off_to_remove.index].name in [offspring.name for cluster,offspring in swap_P_O]:
				print('Error in def assess_for_violations, in class SCM_Predation_Operator, in SCM_Predation_Operator.py')
				print('Somehow, this algorithm has identified a structure to be in the offspring_pool and the population')
				print('The structure can only be in either the offspring pool or population.')
				print('Offspring: '+str(offspring_pool[off_to_remove.index].name))
				print('Check this out')
				import pdb; pdb.set_trace()
				exit('This program will end without completing.')
			offspring_to_remove.append((offspring_pool[off_to_remove.index].name,off_to_remove.index))
		if not offspring_to_remove == []:
			print(offspring_to_remove)
		####################################################################################################################
		if self.print_details:
			self.assess_for_violations_message(swap_P_O,remove_O_similar_to_too_many_P,removal_O_P,removal_O_O)
		####################################################################################################################
		# Deal with the offspring that you would like to swap with clusters in the population.
		force_replacement = []
		for pop_to_swap_out, off_to_swap_in in swap_P_O:
			if not off_to_swap_in.name in offspring_pool.get_cluster_names():
				print('temp error in CNA_version_3.py')
				import pdb; pdb.set_trace()
				exit()
			force_replacement.append((pop_to_swap_out.name,off_to_swap_in.name))
		force_replacement.sort(key=lambda x:x[1],reverse=True) # force replace from highest to lowest index
		return offspring_to_remove, force_replacement

	def assess_for_violations_message(self,swap_P_O,remove_O_similar_to_too_many_P,removal_O_P,removal_O_O):
		"""
		This method will tell the information that offspring are removed or replaced and why. 

		:param swap_P_O: The clusters in the population to swap out, and the offspring to swap in its place. These will be replaced because the offspring has a higher fitness than the cluster in the population, even though they are similar. 
		:type  swap_P_O: tuple of (Organisms.GA.SCM_Predation_Operator.Cluster_Block, Organisms.GA.SCM_Predation_Operator.Cluster_Block)
		:param remove_O_similar_to_too_many_P: Remove offspring because there are too many similar clusters to it in the population already. 
		:type  remove_O_similar_to_too_many_P: tuple of (Organisms.GA.SCM_Predation_Operator.Cluster_Block, Organisms.GA.SCM_Predation_Operator.Cluster_Block)
		:param removal_O_P: Remove offspring because they are similar to a cluster in the population. These offspring are less fit than their similar counterparts in the population. 
		:type  removal_O_P: tuple of (Organisms.GA.SCM_Predation_Operator.Cluster_Block, Organisms.GA.SCM_Predation_Operator.Cluster_Block)
		:param removal_O_O: Remove offpsring because they are similar to other clusters in the Offspring_Pool. This offspring is less fit than their similar counterparts in the offspring_pool. 
		:type  removal_O_O: tuple of (Organisms.GA.SCM_Predation_Operator.Cluster_Block, Organisms.GA.SCM_Predation_Operator.Cluster_Block)

		"""
		########################################################################################################
		# Mention offspring that have been removed and due to having a similar energy to which cluster in the population
		# Error with this one
		print('1. Clusters in the Population that have been replaced by Offspring, due to the cluster in the offspring being geometrically similar and having a lower fitness than a offspring.')
		if len(swap_P_O) > 0:
			print('1. Clusters in the Population that have been replaced by Offspring, due to the cluster in the offspring being geometrically similar and having a lower fitness than a offspring.')
			for pop_to_swap_out, off_to_swap_in in sorted(swap_P_O,key=lambda x:x[1].name,reverse=False):
				cp_removed_name = pop_to_swap_out.name; cp_removed_fitness = pop_to_swap_out.fitness; cp_removed_energy = pop_to_swap_out.energy
				off_swapped_in_name = off_to_swap_in.name; off_swapped_in_fitness = off_to_swap_in.fitness; off_swapped_in_energy = off_to_swap_in.energy
				print(' --> Population Cluster removed '+str(cp_removed_name)+' (Energy: '+str(round(cp_removed_energy,6))+' eV; fitness: '+str(round(cp_removed_fitness,6))+') {Replaced with Offspring '+str(off_swapped_in_name)+' (Energy: '+str(round(off_swapped_in_energy,6))+' eV; fitness: '+str(round(off_swapped_in_fitness,6))+')}.')
		else:
			print('1. No clusters in the population have been replaced by offspring in the offsprings list')
		print('*****************************')
		########################################################################################################
		# Mention offspring that have been removed and due to having a similar energy to which cluster in the population
		print('2. These offspring have a better fitness and are geometrically similar to two or more clusters in the population.')
		if len(remove_O_similar_to_too_many_P) > 0:
			print('2. These offspring have a better fitness and are geometrically similar to two or more clusters in the population.')
			print('   Therefore it is best to remove the offspring to avoid having geometrically similar clusters in the population.')
			print('   Below are the offspring that will be removed and the clusters in the population they are geometrically similar to.')
			for off_to_swap_out, geo_sim_pops in sorted(remove_O_similar_to_too_many_P,key=lambda x:x[0].name,reverse=False):
				off_removed_name = off_to_swap_out.name; off_removed_fitness = off_to_swap_out.fitness; off_removed_energy = off_to_swap_out.energy
				geo_sim_pop1, geo_sim_pop2 = geo_sim_pops
				geo_sim_pop1_name = geo_sim_pop1.name; geo_sim_pop1_fitness = geo_sim_pop1.fitness; geo_sim_pop1_energy = geo_sim_pop1.energy
				geo_sim_pop2_name = geo_sim_pop2.name; geo_sim_pop2_fitness = geo_sim_pop2.fitness; geo_sim_pop2_energy = geo_sim_pop2.energy
				print(' --> Offspring removed '+str(off_removed_name)+' (Energy: '+str(round(off_removed_energy,6))+' eV; fitness: '+str(round(off_removed_fitness,6))+') {Geometrically similar to (at least) clusters in population: '+str(geo_sim_pop1_name)+' (Energy: '+str(round(geo_sim_pop1_energy,6))+' eV; fitness: '+str(round(geo_sim_pop1_fitness,6))+')} and '+str(geo_sim_pop2_name)+' (Energy: '+str(round(geo_sim_pop2_energy,6))+' eV; fitness: '+str(round(geo_sim_pop2_fitness,6))+')}.')
		else:
			print('2. No offspring need to be removed from the offsprings list')
		print('*****************************')
		########################################################################################################
		# Mention offspring that have been removed and due to having a similar energy to which cluster in the population
		print('3. The following offspring were removed from the offspring pool (and because they are geometrically similar and have a lower fitness to which cluster in the population):')
		if len(removal_O_P) > 0:
			print('3. The following offspring were removed from the offspring pool (and because they are geometrically similar and have a lower fitness to which cluster in the population):')
			for offspring_removed, cp_due_to in removal_O_P:
				offspring_removed_name = offspring_removed.name; offspring_removed_fitness = offspring_removed.fitness; offspring_removed_energy = offspring_removed.energy
				cp_due_to_name = cp_due_to.name; cp_due_to_fitness = cp_due_to.fitness; cp_due_to_energy = cp_due_to.energy
				print(' --> Offspring '+str(offspring_removed_name)+' (Energy: '+str(offspring_removed_energy)+' eV; fitness: '+str(round(offspring_removed_fitness,6))+') {Similar to Population Cluster '+str(cp_due_to_name)+' (Energy: '+str(round(cp_due_to_energy,6))+' eV; fitness: '+str(round(cp_due_to_fitness,6))+')}.')
		else:
			print('3. No offspring need to be removed from the offsprings list')
		print('*****************************')
		########################################################################################################
		# Mention offspring that have been removed and due to having a similar energy to which other offspring in the Offspring_Pool
		print('4. Offspring that have have been removed for being geometrically similar and have a lower fitness to the rest of the other Offspring')
		if len(removal_O_O) > 0:
			print('4. Offspring that have have been removed for being geometrically similar and have a lower fitness to the rest of the other Offspring')
			for offspring_removed, due_to_offspring in removal_O_O:
				offspring_removed_name = offspring_removed.name; offspring_removed_fitness = offspring_removed.fitness; offspring_removed_energy = offspring_removed.energy
				due_to_offspring_name = due_to_offspring.name; due_to_offspring_fitness = due_to_offspring.fitness; due_to_offspring_energy = due_to_offspring.energy
				print(' --> Offspring '+str(offspring_removed_name)+' (Energy: '+str(offspring_removed_energy)+'eV; fitness: '+str(round(offspring_removed_fitness,6))+') {Similar to Offspring '+str(due_to_offspring_name)+' (Energy: '+str(due_to_offspring_energy)+' eV; fitness: '+str(round(due_to_offspring_fitness,6))+')}.')
		else:
			print('4. No offspring have been removed from the rest of the offsprings list for being too similar')
		print('**********************************************************')
		print('**********************************************************')

	def add_to_database(self, collection):
		'''
		Add clusters similarities to the CNA database to be stored for future generations. 

		:param collection: update the fitnesses of clusters in the collection.
		:type  collection: Organisms.GA.Collection.Collection
		'''
		# If you are using a different fitness Operator and different CNA parameters, you will
		# need to add the offspring in the offspring_pool to the self.cna_database
		if self.use_same_CNA_database == False:
			self.cna_database.add(collection,initialise=False)

	def remove_from_database(self, cluster_names_to_remove):
		'''
		Clusters to remove from the CNA database

		:param cluster_names_to_remove: A list of the names of all the clusters to remove from the CNA database
		:type  cluster_names_to_remove: list of ints
		'''
		if self.use_same_CNA_database == False:
			#for cluster_name in cluster_names_to_remove:
			self.cna_database.remove(cluster_names_to_remove) # delete the cluster entrance in the self.cna_database

	def reset(self):
		'''
		Reset the CNA database with no inputs
		'''
		if self.use_same_CNA_database == False:
			self.cna_database.reset()
