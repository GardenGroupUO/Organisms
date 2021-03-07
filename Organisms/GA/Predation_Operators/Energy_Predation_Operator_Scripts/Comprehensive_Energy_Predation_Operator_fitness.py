'''
Energy_Diversity_Scheme.py, Geoffrey Weal, 28/10/2018

This is one of the Diversity schemes that can be used by the genetic algorithm program. This is the Energy Diversity Scheme.

This scheme works by preventing the population from having clusters with the same energy existing in the population at any one time.

'''

############################################################################################################################################################
###### These Methods are used by other Diversity Scheme. For this reason, these methods have been written to be accessible to those Diversity Schemes ######
############################################################################################################################################################

import os, sys, inspect

###########################################################################################################
########################## Methods Required for the def check_initial_population ##########################
###########################################################################################################

def check_initial_population(self,return_report=False):
	"""
	This definition is responsible for making sure that the initialised population obeys the Energy Diversity Scheme. 

	Here, the clusters in the population are checked to see if they have the same energy. This is needed for after the 
	population has been initally populated with randomly generated clusters and clusters the user has specified.
	
	:param return_report: This indicates if the user want to return a report on which clusters were removed and why (i.e. what clusters it was similar to energetically.) 
	:type  return_report: bool.

	returns:
		* **clusters_to_remove** (*[[int,str],...]*): Contains a list of [the index of cluster in pop, the name of the cluster] that have been removed from the population as they violate the Energy Diversity Scheme.
		* **Energy_Diversity_report** (*{int: [int,...]}*): Contain a more detailed report of what this method has done by returning a dictorary in the format of {name of kept cluster: [list of names of clusters that have been removed because they have the same energy as the cluster that was kept.]}

	"""
	########################################################################################################
	# Sort the indices of clusters in the population by fitness, from highest to lowest.
	cluster_in_pop_index_fitness = sorted(zip(range(len(self.population)),[cluster.fitness for cluster in self.population]), key=lambda x:x[1], reverse=True)
	if (not cluster_in_pop_index_fitness == []) and (not cluster_in_pop_index_fitness[0][1] >= cluster_in_pop_index_fitness[-1][1]):
		print('Error in def check_initial_population in class CNA_Diversity_Scheme, in Energy_Diversity_Scheme.py')
		print('The fitnesses after the sort are the wrong way around')
		print('cluster_in_pop_index_fitness[0][1] (fitness) = '+str(cluster_in_pop_index_fitness[0][1]))
		print('cluster_in_pop_index_fitness[-1][1] (fitness)= '+str(cluster_in_pop_index_fitness[-1][1]))
		print('The fitnesses need to be order from highest to lowest.')
		exit('Check this out. This program will finish without completing.')
	indices_of_pop_sorted_by_fitness = [index for index, fitness in cluster_in_pop_index_fitness]
	########################################################################################################
	# Energy_Diversity_report will give a report of what clusters were removed and why.
	if return_report:
		Energy_Diversity_report = {}
	########################################################################################################
	clusters_to_remove = []
	i1 = 0
	while i1 < len(indices_of_pop_sorted_by_fitness):
		index1 = indices_of_pop_sorted_by_fitness[i1]; cluster1 = self.population[index1]
		i2 = i1 + 1
		while i2 < len(indices_of_pop_sorted_by_fitness):
			index2 = indices_of_pop_sorted_by_fitness[i2]; cluster2 = self.population[index2]
			if abs(round(cluster2.energy - cluster1.energy,12)) < self.minimum_energy_diff:
				name_to_remove  = cluster2.name
				index_to_remove = index2
				# Record information about cluster that were kept and as a result which clusters were removed
				if return_report:
					name_to_keep = cluster1.name; 
					Energy_Diversity_report.setdefault(name_to_keep,[]).append(name_to_remove)
				# add cluster2 to clusters_to_remove and remove it from indices_of_pop_sorted_by_fitness
				clusters_to_remove.append((index_to_remove, name_to_remove))
				del indices_of_pop_sorted_by_fitness[i2]
			else:
				i2 += 1
		i1 += 1
	if return_report:
		Energy_Diversity_report = Energy_Diversity_report.items()
	########################################################################################################
	# Check to see if there are no two clusters in the clusters_to_remove that are the same cluster (same name)
	check_for_duplicate_names = [cluster_name_to_remove for _,cluster_name_to_remove in clusters_to_remove]
	if not len(check_for_duplicate_names) == len(set(check_for_duplicate_names)):
		print('Error in def check_Population in Class Energy_Diversity_Scheme, in Energy_Diversity_Scheme.py')
		print('Two of the clusters name in the removed cluster list are the same')
		print('This indicates that this cluster has been deleted twice?')
		print('List of cluster names in the population: '+str(check_for_duplicate_names))
		print('Check this out.')
		import pdb; pdb.set_trace()
		exit()
	########################################################################################################
	# Sort the indices of the clusters_to_remove from lowest to highest index so we can at some point 
	# remove the clusters with these indices from the self.population.
	clusters_to_remove.sort(key=lambda x:x[0],reverse=False) # Order index from lowest to highest
	########################################################################################################
	# Remove duplicates from the population
	for index_to_remove, name_to_remove in clusters_to_remove[::-1]: # remove index from highest to lowest
		self.population.remove(index_to_remove)
	########################################################################################################
	# Return the results, depending on if the user wants to know which clusters were removed as they were energetic similar to which cluster in same_energies_report
	if return_report:
		return clusters_to_remove, Energy_Diversity_report
	else:
		return clusters_to_remove
	########################################################################################################

########################################################################################################
########################## Methods Required for the def assess_for_violations ##########################
########################################################################################################

class Cluster_Block:
	"""
	This is used by the Remove_Cluster_Due_To_Diversity_Violation definition to store information in an easy way to help the user understand what is going on in this method 

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
		self.energy = collection[index].energy
		self.fitness = collection[index].fitness
	def  __repr__(self):
		return str(self.collection_type)+str(self.name)+'('+str(self.index)+', energy = '+str(self.energy)+' eV, fitness = '+str(self.fitness)+')'

def assess_for_violations_message(swap_P_O,remove_O_similar_to_too_many_P,removal_O_P,removal_O_O):
	########################################################################################################
	# Mention offspring that have been removed and due to having a similar energy to which cluster in the population
	# Error with this one
	print('1. Clusters in the Population that have been replaced by Offspring, due to the cluster in the offspring being energetically similar and having a lower energy than a offspring.')
	if len(swap_P_O) > 0:
		print('1. Clusters in the Population that have been replaced by Offspring, due to the cluster in the offspring being energetically similar and having a lower energy than a offspring.')
		for pop_to_swap_out, off_to_swap_in in sorted(swap_P_O,key=lambda x:x[1].name,reverse=False):
			cp_removed_name = pop_to_swap_out.name; cp_removed_energy = pop_to_swap_out.energy; cp_removed_fitness = pop_to_swap_out.fitness
			off_swapped_in_name = off_to_swap_in.name; off_swapped_in_energy = off_to_swap_in.energy; off_swapped_in_fitness = off_to_swap_in.fitness
			print(' --> Population Cluster removed '+str(cp_removed_name)+' (Energy: '+str(round(cp_removed_energy,6))+' eV, fitness = '+str(round(cp_removed_fitness,6))+') {Replaced with Offspring '+str(off_swapped_in_name)+' (Energy: '+str(round(off_swapped_in_energy,6))+' eV, fitness = '+str(round(off_swapped_in_fitness,6))+')}.')
	else:
		print('1. No clusters in the population have been replaced by offspring in the offsprings list')
	print('*****************************')
	########################################################################################################
	# Mention offspring that have been removed and due to having a similar energy to which cluster in the population
	print('2. These offspring have a better energy and are energetically similar to two or more clusters in the population.')
	if len(remove_O_similar_to_too_many_P) > 0:
		print('2. These offspring have a better energy and are energetically similar to two or more clusters in the population.')
		print('   Therefore it is best to remove the offspring to avoid having energetically similar clusters in the population.')
		print('   Below are the offspring that will be removed and the clusters in the population they are energetically similar to.')
		for off_to_swap_out, geo_sim_pops in sorted(remove_O_similar_to_too_many_P,key=lambda x:x[0].name,reverse=False):
			off_removed_name = off_to_swap_out.name; off_removed_energy = off_to_swap_out.energy; off_removed_fitness = off_to_swap_out.fitness
			geo_sim_pop1, geo_sim_pop2 = geo_sim_pops
			geo_sim_pop1_name = geo_sim_pop1.name; geo_sim_pop1_energy = geo_sim_pop1.energy; geo_sim_pop1_fitness = geo_sim_pop1.fitness
			geo_sim_pop2_name = geo_sim_pop2.name; geo_sim_pop2_energy = geo_sim_pop2.energy; geo_sim_pop2_fitness = geo_sim_pop2.fitness
			print(' --> Offspring removed '+str(off_removed_name)+' (Energy: '+str(round(off_removed_energy,6))+' eV; fitness = '+str(round(off_removed_fitness,6))+') {Energetically similar to (at least) clusters in population: '+str(geo_sim_pop1_name)+' (Energy: '+str(round(geo_sim_pop1_energy,6))+' eV, fitness = '+str(round(geo_sim_pop1_fitness,6))+')} and '+str(geo_sim_pop2_name)+' (Energy: '+str(round(geo_sim_pop2_energy,6))+' eV, fitness = '+str(round(geo_sim_pop2_fitness,6))+')}.')
	else:
		print('2. No offspring need to be removed from the offsprings list')
	print('*****************************')
	########################################################################################################
	# Mention offspring that have been removed and due to having a similar energy to which cluster in the population
	print('3. The following offspring were removed from the offspring pool (and because they are energetically similar and have a lower energy to which cluster in the population):')
	if len(removal_O_P) > 0:
		print('3. The following offspring were removed from the offspring pool (and because they are energetically similar and have a lower energy to which cluster in the population):')
		for offspring_removed, cp_due_to in removal_O_P:
			offspring_removed_name = offspring_removed.name; offspring_removed_energy = offspring_removed.energy; offspring_removed_fitness = offspring_removed.fitness
			cp_due_to_name = cp_due_to.name; cp_due_to_energy = cp_due_to.energy; cp_due_to_fitness = cp_due_to.fitness
			print(' --> Offspring '+str(offspring_removed_name)+' (Energy: '+str(offspring_removed_energy)+' eV, fitness = '+str(round(offspring_removed_fitness,6))+') {Similar to Population Cluster '+str(cp_due_to_name)+' (Energy: '+str(round(cp_due_to_energy,6))+' eV, fitness = '+str(round(cp_due_to_fitness,6))+')}.')
	else:
		print('3. No offspring need to be removed from the offsprings list')
	print('*****************************')
	########################################################################################################
	# Mention offspring that have been removed and due to having a similar energy to which other offspring in the Offspring_Pool
	print('4. Offspring that have have been removed for being energetically similar and have a lower energy to the rest of the other Offspring')
	if len(removal_O_O) > 0:
		print('4. Offspring that have have been removed for being energetically similar and have a lower energy to the rest of the other Offspring')
		for offspring_removed, due_to_offspring in removal_O_O:
			offspring_removed_name = offspring_removed.name; offspring_removed_energy = offspring_removed.energy; offspring_removed_fitness = offspring_removed.fitness
			due_to_offspring_name = due_to_offspring.name; due_to_offspring_energy = due_to_offspring.energy; due_to_offspring_fitness = due_to_offspring.fitness
			print(' --> Offspring '+str(offspring_removed_name)+' (Energy: '+str(offspring_removed_energy)+'eV, fitness = '+str(round(offspring_removed_fitness,6))+') {Similar to Offspring '+str(due_to_offspring_name)+' (Energy: '+str(due_to_offspring_energy)+' eV, fitness = '+str(round(due_to_offspring_fitness,6))+')}.')
	else:
		print('4. No offspring have been removed from the rest of the offsprings list for being too similar')
	print('**********************************************************')
	print('**********************************************************')
	########################################################################################################

def assess_for_violations_no_force_replacement(self,offspring_pool):
	"""
	This will assess which offspring to remove before the natural selection process.

	The offspring are assessed against clusters in the population. Offspring are removed from the offspring_pool if:
	* They have an energy equal to another offspring
	* They have an energy equal to another cluster in the population.

	:param offspring_pool: This is the offspring that you want to add eventually using the natural selection process to the population.
	:type  offspring_pool: Offspring_Pool

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
		print('Start assessing for Energy Diversity')
	offspring_to_remove = []
	# Check offspring against themselves
	structures_to_consider = [Cluster_Block(offspring_pool,'Offspring',index) for index in range(len(offspring_pool))]
	structures_to_consider.sort(key=lambda cluster: cluster.fitness, reverse=False)
	index1 = 0
	while index1 < len(structures_to_consider):
		offspring1 = structures_to_consider[index1]
		for index2 in range(len(structures_to_consider)-1,index1,-1):
			offspring2 = structures_to_consider[index2]
			energy_diff = abs(round(offspring1.energy - offspring2.energy,12))
			if energy_diff < self.minimum_energy_diff:
				offspring_to_remove.append((offspring2.name,offspring2.index))
				del structures_to_consider[index2]
		index1 += 1
	# check offspring against clusters in the populatino
	for index in range(len(structures_to_consider)):
		offspring = structures_to_consider[index]
		for cluster_in_population in self.population:
			energy_diff = abs(round(offspring.energy - cluster_in_population.energy,12))
			if energy_diff < self.minimum_energy_diff:
				offspring_to_remove.append((offspring.name,offspring.index))
				break
	# Sort by index and continue on
	offspring_to_remove.sort(key=lambda x:x[1],reverse=True)
	force_replacement = []
	return offspring_to_remove, force_replacement

def assess_for_violations_force_replacement(self,offspring_pool):
	"""
	This will assess which offspring to remove before the natural selection process.

	The offspring are assessed against clusters in the population. Offspring are removed from the offspring_pool if:
	* They have an energy equal to another offspring
	* They have an energy equal to another cluster in the population.

	:param offspring_pool: This is the offspring that you want to add eventually using the natural selection process to the population.
	:type  offspring_pool: Offspring_Pool

	"""
	print('**********************************************************')
	print('**********************************************************')
	print('Offspring removed from the Offspring Pool due to violating the Comprehensive Energy Diversity Scheme.')
	print('NOTE: energy difference minimum = '+str(self.minimum_energy_diff)+' eV.')
	print('**********************************************************')
	print('**********************************************************')
	########################################################################################################
	# sort all clusters in population and offspring by fitness
	print('Assessing which structures to remove to comply with the Energy Diversity Scheme')
	structures_to_consider = [Cluster_Block(self.population,'Population',index) for index in range(len(self.population))] 
	structures_to_consider += [Cluster_Block(offspring_pool,'Offspring',index) for index in range(len(offspring_pool))]
	# order fitnesses,From highest to lowest
	structures_to_consider.sort(key=lambda cluster: cluster.fitness, reverse=True)
	if (not structures_to_consider == []) and (not structures_to_consider[0].fitness >= structures_to_consider[-1].fitness):
		print('Error in def assess_for_violations in class CNA_Diversity_Scheme, in Energy_Diversity_Scheme.py')
		print('The fitnesses after the sort are the wrong way around')
		print('structures_to_consider[0].fitness = '+str(structures_to_consider[0].fitness))
		print('structures_to_consider[-1].fitness = '+str(structures_to_consider[-1].fitness))
		print('The fitnesses need to be order from highest to lowest.')
		exit('Check this out. This program will finish without completing.')
	########################################################################################################
	print('Start assessing for Energy Diversity')
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
		# scan though all the other clusters which have higher energies
		indices_to_delete = []
		for index_lower in range(index_higher+1, len(structures_to_consider)):
			cluster_lower = structures_to_consider[index_lower]
			############################################################################################################
			energy_diff = abs(round(cluster_higher.energy - cluster_lower.energy,12))
			if energy_diff < self.minimum_energy_diff:
				# The two clusters being looked at at the moment are geometrically the same. 
				if cluster_higher.collection_type == 'Population':
					# if two clusters in the population are geometrically similar, we have an issue.
					if cluster_lower.collection_type == 'Population':
						print('Error in def assess_for_violations in class CNA_Diversity_Scheme, in Energy_Diversity_Scheme.py')
						print('Two of the clusters in the population are identical by the max  similarity cutt off setting.')
						print('cluster_higher: '+str(cluster_higher))
						print('cluster_lower: '+str(cluster_lower))
						import pdb; pdb.set_trace()
						exit('This program will exit without completing.')
					# If a cluster in the population (and has a higher energy) is geometrically similar to an offspring,
					# then it is better to keep the offspring and remove the offspring
					elif cluster_lower.collection_type == 'Offspring':
						removal_O_P_temp.append([cluster_lower,cluster_higher])
				elif cluster_higher.collection_type == 'Offspring':
					# If an offspring is geometrically similar (and has a higher energy) to a cluster in population,
					# then it is better to replace this cluster in the population with this offspring.
					if cluster_lower.collection_type == 'Population':
						# Take the lowest energy cluster in the population to swap with this offspring.
						if one_instance_of_swap_P_O == []:
							one_instance_of_swap_P_O = [[cluster_lower,cluster_higher]]
						else:
							cluster_lower_old, cluster_higher_old = one_instance_of_swap_P_O[0]
							if not cluster_higher_old.name == cluster_higher.name:
								exit('Somethings up')
							remove_O_similar_to_too_many_P_temp.append([cluster_higher,[cluster_lower_old,cluster_lower]])
							one_instance_of_swap_P_O = []; indices_to_delete = []
							print('Energy Scheme Debugger Marker 1')
							break
					# If an offspring is geometrically similar (and has a higher energy) to an offspring,
					# remove the higher energy offspring
					elif cluster_lower.collection_type == 'Offspring':
						removal_O_O_temp.append([cluster_lower,cluster_higher])
				indices_to_delete.append(index_lower)
		################################################################################################################
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
			################################################################################################################
	####################################################################################################################
	print('Removing offspring that violate the Energy Diversity Scheme')
	offspring_to_remove = []
	for off_to_remove, pop_to_keep in sorted(removal_O_P+removal_O_O+remove_O_similar_to_too_many_P,key=lambda x:x[0].index,reverse=True): # remove from highest to lowest index
		if offspring_pool[off_to_remove.index].name in [offspring.name for cluster,offspring in swap_P_O]:
			print('Error in def assess_for_violations, in class CNA_Diversity_Scheme, in CNA_Diversity_Scheme.py')
			print('Somehow, this algorithm has identified a structure to be in the offspring_pool and the population')
			print('The structure can only be in either the offspring pool or population.')
			print('Offspring: '+str(offspring_pool[off_to_remove.index].name))
			print('Check this out')
			import pdb; pdb.set_trace()
			exit('This program will end without completing.')
		offspring_to_remove.append((offspring_pool[off_to_remove.index].name,off_to_remove.index))
	####################################################################################################################
	assess_for_violations_message(swap_P_O,remove_O_similar_to_too_many_P,removal_O_P,removal_O_O)
	####################################################################################################################
	# Deal with the offspring that you would like to swap with clusters in the population.
	force_replacement = []
	for pop_to_swap_out, off_to_swap_in in swap_P_O:
		if not off_to_swap_in.name in offspring_pool.get_cluster_names():
			print('Error in assess_for_violations.py in Comprehensive_Energy_Diversity_Scheme_energy.py')
			print('One of the offspring that will be swapped into the population for force_replacement does not exist in the offspring_pool')
			print('Offspring to swap into the population: '+str(swap_P_O))
			print('Offspring in the offspring_pool: '+str(offspring_pool.get_cluster_names()))
			print('Problematic offspring that was incountered: '+str(off_to_swap_in.name))
			print('Check this.')
			import pdb; pdb.set_trace()
			exit('This program will finish without completing.')
		force_replacement.append((pop_to_swap_out.name,off_to_swap_in.name))
	force_replacement.sort(key=lambda x:x[1],reverse=True) # force replace from highest to lowest index
	return offspring_to_remove, force_replacement

################################################################################################################################################################################################################
############################################################### DEBUGGING METHODS ##############################################################################################################################
################################################################################################################################################################################################################

def Check_for_Issue_with_Scheme_with_collection(self,collection):
	"""
	This method allows us to check that the collection does not violate the comprehensive diversity scheme after it has been perform on the collection.

	The collection is either the Population of Offspring_Pool.

	:param collection: This is the collection to record. This is either the instance of the Population or the Offspring_Pool
	:type  collection: Population or Offspring_Pool
		
	"""
	energies = [cluster.energy for cluster in collection]
	similar_energy_clusters = []
	for index1 in range(len(self.population)):
		for index2 in range(index1+1,len(self.population)):
			energy_diff = round(self.population[index1].energy - self.population[index2].energy,12)
			if abs(energy_diff) < self.minimum_energy_diff:
				similar_energy_clusters.append([index1,index2,abs(energy_diff)])
	if len(similar_energy_clusters) > 0:
		print('*******************************************')
		print('Error with Energy Diversity Scheme.')
		print('There are duplicates in the energy, which should not be happening in the Energy Diversity Scheme.')
		print('*******************************************')
		print('Here is a printout of the clusters in '+str(collection.getname()))
		for cluster in collection:
			print('Cluster '+str(cluster)+'; Energy = '+str(cluster.energy)+' eV.')
		print('*******************************************')
		print('The clusters that have an energy less than the minimum energy diff ('+str(self.minimum_energy_diff)+' eV) are:')
		for index1, index2, abs_energy_diff in similar_energy_clusters:
			cluster1 = self.population[index1]; cluster2 = self.population[index2]
			print('Cluster '+str(cluster1.name)+' (Energy = '+str(cluster1.energy)+' eV); Cluster '+str(cluster2.name)+' (Energy = '+str(cluster2.energy)+' eV); Energy Difference: '+str(abs_energy_diff))
		print('*******************************************')
		print('This likely means there is an error in the Energy Diversity Scheme code. Check this.')
		import pdb; pdb.set_trace()
		exit()

################################################################################################################################################################################################################
################################################################################################################################################################################################################
################################################################################################################################################################################################################



