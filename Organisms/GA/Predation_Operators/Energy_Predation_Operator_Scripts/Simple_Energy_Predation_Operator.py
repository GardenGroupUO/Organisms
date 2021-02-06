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

	Here, the clusters in the population are checked to see if they have the same energy. This is needed for after the population has been initally populated with randomly generated clusters and clusters the user has specified.
	
	:param return_report: 
	:type  return_report: bool.

	returns:
		* **clusters_to_remove** (*[[int,str],...]*): Contains a list of [the index of cluster in pop, the dir of the cluster] that have been removed from the population as they violate the Energy Diversity Scheme.
		* **same_energies_report** (*{int: [int,...]}*): Contain a more detailed report of what this method has done by returning a dictorary in the format of {dir of kept cluster: [list of dirs of clusters that have been removed because they have the same energy as the cluster that was kept.]}

	"""
	########################################################################################################
	# get some lists ready to help us.
	cluster_indices_in_population = list(range(len(self.population)))
	clusters_to_remove = []; 
	if return_report:
		same_energies_report = {}
	########################################################################################################
	# Find the energetically repeated clusters in the population as defined by the energy diversity scheme
	#
	# NOTE: Here, we MUST use the list "cluster_indices_in_population". This is because the philosophy of the GA program
	# is to keep the clusters added and removed in-place in the population. For more information abpout what in-place means,
	# see `In-place algorithm <https://en.wikipedia.org/wiki/In-place_algorithm>`_
	#	* Note that no clusters are removed that this point in the algorithm. This is how we can use the list 
	#	  "cluster_indices_in_population" to deals with clusters in the population inplace.
	index1 = 0
	while index1 < len(cluster_indices_in_population):
		index_in_pop1 = cluster_indices_in_population[index1]; cluster1 = self.population[index_in_pop1]
		# scan though the rest of the clusters in the population for any of those clusters with the same energy as cluster1
		for index2 in range(len(cluster_indices_in_population)-1,index1,-1):
			index_in_pop2 = cluster_indices_in_population[index2]; cluster2 = self.population[index_in_pop2]
			# if the energy of cluster2 is the same as cluster1, remove cluster2 from the population.
			if round(cluster2.energy,self.round_energy) == round(cluster1.energy,self.round_energy):
				# If you are giving a report of clusters kept and removed, do the following to place information into "same_energies_report".
				if return_report:
					if not cluster1.dir in same_energies_report:
						same_energies_report[cluster1.dir] = [cluster2.dir]
					else:
						same_energies_report[cluster1.dir].insert(0,cluster2.dir)
				# This cluster will eventually be removed from the population. We will for the moment removed it in place by 
				# removing this clusters index in the "cluster_indices_in_population" list.
				clusters_to_remove.append([index_in_pop2,cluster2.dir])
				del cluster_indices_in_population[index2] # i.e. remove index_in_pop2 from the cluster_indices_in_population list.
		index1 += 1
	########################################################################################################
	# Sort the indices of the clusters_to_remove from lowest to highest index so we can at some point 
	# remove the clusters with these indices from the self.population.
	clusters_to_remove.sort(key=lambda x:x[0],reverse=False)
	########################################################################################################
	# Check to see if there are no two clusters in the clusters_to_remove that are the same cluster (same dir)
	check_for_duplicate_dirs = [cluster_dir_to_remove for _,cluster_dir_to_remove in clusters_to_remove]
	if not len(check_for_duplicate_dirs) == len(set(check_for_duplicate_dirs)):
		print('Error in def check_Population in Class Energy_Diversity_Scheme, in Energy_Diversity_Scheme.py')
		print('Two of the clusters dir in the removed cluster list are the same')
		print('This indicates that this cluster has been deleted twice?')
		print('List of cluster dirs in the population: '+str(check_for_duplicate_dirs))
		print('Check this out.')
		import pdb; pdb.set_trace()
		exit()
	########################################################################################################
	# Return the results, depending on if the user wants to know which clusters were removed as they were energetic similar to which cluster in same_energies_report
	if return_report:
		return clusters_to_remove, same_energies_report
	else:
		return clusters_to_remove
	########################################################################################################

########################################################################################################
########################## Methods Required for the def assess_for_violations ##########################
########################################################################################################

def assess_for_violations(self,offspring_pool):
	"""
	This will assess which offspring to remove before the natural selection process.

	The offspring are assessed against clusters in the population. Offspring are removed from the offsprings if:
	* They have an energy equal to another offspring
	* They have an energy equal to another cluster in the population.

	:param offsprings: This is the offspring that you want to add eventually using the natural selection process to the population.
	:type  offsprings: Offspring_Pool

	"""
	########################################################################################################
	#
	details_of_offsprings_that_will_be_removed = []
	########################################################################################################
	# First, we want to remove any offspring with duplicate energies with other offspring.
	# For example, if 4 offspring have the same energy, the first offspring that was made is kept, and the other three are removed.
	# For this reason, the second while is required to go though the whole of the rest of the offspring_pool to check for more than one duplicate offspring.
	index1 = 0
	while index1 < len(offsprings):
		index2 = index1 + 1
		while index2 < len(offsprings):
			if round(offsprings[index1].energy,self.round_energy) == round(offsprings[index2].energy,self.round_energy):
				offspring_similar_to = ['off_'+str(offsprings[index1].dir),offsprings[index1].energy]
				offspring_to_remove = offsprings.pop(index2)
				details_of_offsprings_that_will_be_removed.append([offspring_to_remove,offspring_similar_to])
			else:
				index2 += 1
		index1 += 1
	########################################################################################################
	# Second, we will now compare the offspring with clusters in the poplation. If a offspring has the same energy as a cluster
	# the population, the offspring will be removed from the offspring pool.
	# The for loop only needs to find one time where offsprings[index1].energy == individual.energy, since there SHOULD be only one cluster
	# in the population with that energy. 
	index1 = 0
	while index1 < len(offsprings):
		for individual in self.population:
			if round(offsprings[index1].energy,self.round_energy) == round(individual.energy,self.round_energy):
				offspring_similar_to = ['pop_'+str(individual.dir),individual.energy]
				offspring_to_remove = offsprings.pop(index1)
				# since we have removed the offspring at index1, we so not want to increment index1, as there will be a new offspring now in index1 due to the pop in the previousl line.
				details_of_offsprings_that_will_be_removed.append([offspring_to_remove,offspring_similar_to])
				break
		else: # This offspring energy was not found in the population, we now increase index1 to move onto the next offspring.
			index1 += 1
	########################################################################################################
	print('*****************************')
	print('*****************************')
	if len(details_of_offsprings_that_will_be_removed) > 0:
		print('Removing the following clusters from the offsprings list')
		for offspring_to_remove, offspring_similar_to in details_of_offsprings_that_will_be_removed:
			print('Cluster '+str(offspring_to_remove.dir)+' ('+str(offspring_to_remove.energy)+' eV) {Similar to '+str(offspring_similar_to[0])+' (Energy = '+str(offspring_similar_to[1])+')}')
	else:
		print('No clusters need to be removed from the offsprings list')
	return [], []

################################################################################################################################################################################################################
############################################################### DEBUGGING METHODS ##############################################################################################################################
################################################################################################################################################################################################################

def Check_for_Issue_with_Scheme_with_collection(self,collection):
	"""
	This method allows us to check that the collection does not violate the simple diversity scheme after it has been perform on the collection.

	The collection is either the Population of Offspring_Pool.

	:param collection: This is the collection to record. This is either the instance of the Population or the Offspring_Pool
	:type  collection: Population or Offspring_Pool
		
	"""
	energies = [cluster.energy for cluster in collection]
	if len(energies) != len(set(energies)):
		print('Error with Energy Diversity Scheme.')
		print('There are duplicates in the energy, which should not be happening in the Energy Diversity Scheme.')
		print('Here is a printout of the clusters in '+str(collection.getname()))
		for cluster in collection:
			print('Cluster '+str(cluster)+'; Energy = '+str(cluster.energy)+' eV.')
		print('This likely means there is an error in the Energy Diversity Scheme code. Check this.')
		import pdb; pdb.set_trace()
		exit()

################################################################################################################################################################################################################
################################################################################################################################################################################################################
################################################################################################################################################################################################################
