import sys

from Organisms.GA.Fitness_Operators.Fitness_Operator import Fitness_Operator, dot
from Organisms.GA.Fitness_Operators.SCM_and_Energy_Fitness_Operator_Options import SCM_options

from Organisms.GA.Fitness_Operators.Energetic_Fitness_Contribution import get_lowest_and_highest_energies_from_collections
from Organisms.GA.Fitness_Operators.CNA_Fitness_Contribution       import get_lowest_and_highest_similarities_from_collections

from Organisms.GA.Fitness_Operators.Energetic_Fitness_Contribution import get_energetic_fitness_contribution, get_lowest_and_highest_energies_from_collections
from Organisms.GA.Fitness_Operators.CNA_Fitness_Contribution       import get_lowest_and_highest_similarities_from_collections

from Organisms.GA.Fitness_Operators.CNA_Fitness_Contribution import get_CNA_most_similar_average

def get_average(cluster_SCM_simiarities):
	average = float(sum(cluster_SCM_simiarities)) / float(len(cluster_SCM_simiarities))
	return average

class SCM_and_Energy_Fitness_Operator(Fitness_Operator):
	"""
	This class controls the how the fitness values for the Structural Comparison Method (SRM)-based predation operator are obtained.
	
	:param fitness_information: This is all the information that is needed about the fitness class
	:type  fitness_information: dict.
	:param predation_operator: This is the predation operator that this fitness class will take information from if needed to obtain a fitness.
	:type  predation_operator: Organisms.GA.Predation_Operator
	:param population: The population to assign fitnesses to
	:type  population: Organisms.GA.Population
	:param generations: The number of generations that will be performed in the genetic algorithm.
	:type  generations: int
	:param no_of_cpus: the number of cpus to use when multiprocessing
	:type  no_of_cpus: int
	:param print_details: Print the details of the energy fitness operator. True if yes, False if no
	:type  print_details: bool

	"""
	def __init__(self,fitness_information, predation_operator, population, generations, no_of_cpus, print_details): # Check this out.
		super().__init__(fitness_information, population, print_details)
		SCM_options(self, fitness_information, predation_operator, no_of_cpus)

	def print_initial_message(self):
		"""
		At the start of the GA run, this message will be shown so that the user knows what their energy and fSRM (CNA)-based itness contributions are at the start of the GA.
		"""
		print('****************************************************')
		print('The Fitness Contribution from the Energy and CNA components.')
		print('Energetic Contribution to Fitness: '+str(self.energy_contribution))
		print('CNA Contribution to Fitness: '+str(self.CNA_contribution))
		print('****************************************************')
		
	####################################################################################
	################## Method for assign_initial_population_fitnesses ##################
	####################################################################################

	def assign_initial_population_fitnesses(self): 
		"""
		This method is designed to assign fitness values to the clusters of the population only at the start of the GA, when the population has been initialised

		"""
		self.cna_database.add(self.population,initialise=True)
		self.__assign_population_fitnesses(0)

	####################################################################################
	################## Method for assign_resumed_population_fitnesses ##################
	####################################################################################

	def assign_resumed_population_fitnesses(self,resume_from_generation): 
		"""
		This method is designed to assign fitness values to the clusters of the population only at the beginning of a resumed GA. 

		:param resume_from_generation: The current generation to resume from.
		:type  resume_from_generation: int
		
		"""
		self.cna_database.add(self.population,initialise=True)
		self.__assign_population_fitnesses(resume_from_generation)

	############################################################################################################
	################## Method for assign_all_fitnesses_before_assess_against_predation_operator ##################
	############################################################################################################

	def assign_all_fitnesses_before_assess_against_predation_operator(self,all_offspring_pools,current_generation_no):
		"""
		This method is to be used in the GA program. 
		This will assign all the fitnesses of all clusters in the current generation (population and offspring) before the offspring are assessed to understand if they violate the predation operator (i.e. an offspring is Class 1 similar to a cluster in the population, or another offspring).

		See the description given for the "assign_all_fitnesses" def on what the crux of this method is.

		If you write your own diversiy and fitness classes, you do not need to implement this method in your fitness class.

		:param all_offspring_pools: list of all the offspring pools of offspring to assign fitness values to.
		:type  all_offspring_pools: list of Organisms.GA.Offspring_Pool
		:param current_generation_no: The current generation
		:type  current_generation_no: int
		"""
		if not isinstance(all_offspring_pools,list):
			all_offspring_pools = [all_offspring_pools]
		#for offspring_pool in all_offspring_pools:
		#	self.cna_database.add(offspring_pool,initialise=False)
		return self.__assign_all_fitnesses(all_offspring_pools,current_generation_no)

	###########################################################################################################
	################# Method for assign_all_fitnesses_after_assess_against_predation_operator #################
	###########################################################################################################

	def assign_all_fitnesses_after_assess_against_predation_operator(self,all_offspring_pools,current_generation_no,offspring_to_remove):
		"""
		This method is to be used in the GA program. 
		This will assign all the fitnesses of all clusters in the current generation (population and offspring) after the offspring are assessed to understand if they violate the predation operator (i.e. an offspring is Class 1 similar to a cluster in the population, or another offspring).

		See the description given for the "assign_all_fitnesses" def on what the crux of this method is.

		If you write your own diversiy and fitness classes, you do not need to implement this method in your fitness class.

		:param all_offspring_pools: All of the offspring_pools
		:type  all_offspring_pools: list of Organisms.GA.Offspring_Pool
		:param current_generation_no: The current generation
		:type  current_generation_no: int
		:param offspring_to_remove: a list of all the names of clusters in the offspring that will be removed. Currently not needed, but kept in case. 
		:type  offspring_to_remove: list of int

		"""
		# If self.use_same_CNA_database == False, then the first thing that needs to be done is 
		# to update self.cna_database to remove clusters that would have been removed during 
		# self.predation_operator.remove_offspring_and_replace_with_population_that_violate_predation_operator
		# when the generations are being performed in the GA_Program script.
		#if self.use_same_CNA_database == False:
		#	offspring_to_remove_names = [name for name,index in offspring_to_remove]
		#	self.cna_database.remove(offspring_to_remove_names)
		return self.__assign_all_fitnesses(all_offspring_pools,current_generation_no)

	#############################################################################################
	################## Method for assign_all_fitnesses_after_natural_selection ##################
	#############################################################################################

	def assign_all_fitnesses_after_natural_selection(self,current_generation_no):
		"""
		This method is to be used in the GA program. 
		This will assign all the fitnesses to all the clusters in the population before the offspring are assessed to understand if they violate the predation operator (i.e. an offspring is Class 1 similar to a cluster in the population, or another offspring).

		See the description given for the "assign_population_fitnesses" def on what the crux of this method is.

		If you write your own diversiy and fitness classes, you do not need to implement this method in your fitness class.

		:param current_generation_no: The current generation
		:type  current_generation_no: int

		"""
		# Remove all clusters that were not included in the population due to the natural selection process.
		'''
		clusters_to_remove_from_cna_database = []
		clusters_in_population = self.population.get_cluster_names()
		for cluster_name in self.cna_database.keys():
			if not cluster_name in clusters_in_population:
				clusters_to_remove_from_cna_database.append(cluster_name)
		'''
		#self.cna_database.remove(clusters_to_remove_from_cna_database)
		# Just doing a check to make sure that the number of entries in the self.cna_database is being reduced after every generation, preventing memory leaking
		#self.cna_database.check_database(self.population)
		# Assign fitnesses
		cluster_SCM_simiarities = self.__assign_population_fitnesses(current_generation_no)
		self.__update_weights(cluster_SCM_simiarities)

	def __update_weights(self,cluster_SCM_simiarities):
		"""
		Updates the energy and SCM coefficients if the dynamic version of the structure + energy fitness operator is used.

		:param cluster_SCM_simiarities: The similarities of clusters of the population as obtained by the SCM. These are the sigma 1/2 similarities. 
		:type  cluster_SCM_simiarities: list of floats
		"""
		if self.dynamic_mode:
			# Obtain the population 'similarity value' from all the similarity values from all clusters in the population. 
			population_fitness = self.get_population_fitness(cluster_SCM_simiarities,self.population_fitness_function)
			# The population 'fitness value' is used to update the coefficients (weights) for the energy and SCM coefficients.
			self.SCM_fitness_contribution = self.convert_population_fitness_to_SCM_fitness_contribution(population_fitness)
			# obtain the new coefficients for energy, and place them into self.fitness_weights. The format of self.fitness_weights must be [energy_fitness_coefficient, SCM_fitness_coefficient]
			self.energy_fitness_contribution = 1.0 - self.SCM_fitness_contribution
			self.fitness_weights = []
			if not self.energy_fitness_contribution == 0.0:
				self.fitness_weights.append(self.energy_fitness_contribution)
			if not self.SCM_fitness_contribution == 0.0:
				self.fitness_weights.append(self.SCM_fitness_contribution)

	def get_population_fitness(self,cluster_SCM_simiarities,population_fitness_function):
		"""
		Obtain the 'fitness' of the population. This population fitness is based on the similarity values from all clusters in the population. 
		This python definition will take the similarity values from all clusters in the population and get a 'similarity value' of the population. 
		This definition will then take this population similarity value and convert it into a population fitness value. 
		The population fitness value must be a read value between (and including) 0.0 and 1.0.

		:param cluster_SCM_simiarities: The similarities of clusters of the population as obtained by the SCM. These are the sigma 1/2 similarities. 
		:type  cluster_SCM_simiarities: list of floats
		:param population_fitness_function: The python def that turns the population similarity value into a population fitness value.
		:type  population_fitness_function: def

		"""
		# THis is just an example which geoff is having a mess around with
		# from https://pdf.sciencedirectassets.com/280203/1-s2.0-S1877050918X00076/1-s2.0-S1877050918306100/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJGMEQCIGj3e8QchiulQhGRvnjboT7FpZqiI27yQRKXZruql7etAiA8cKouDjyTz0Z4dE%2BuPF09Jh7j3TyRtcEI3pjGm%2BEvayq0AwhyEAMaDDA1OTAwMzU0Njg2NSIMKfbjirK0jaEfegOBKpEDFTS0BzXwH84wlrINvGrWjj%2B7iae1aUvWuZHY0HK0DBqyNUC8Ws9mX3zMw9pD96tiIH4ER921DG5eCY8i%2Byv1aqEiO5ELgt4Ny0%2B9nLJXIvINi3ajOvXqhkygomRmQPwRH9fHm9tH6x5c2RG0JQerIMG0yalE1%2BlYO%2FwdizaeCUruvug32x0n%2B2pfqc32zjIComIh%2B0WhomLSgijxAQhy4Q7n6flosjb9i5k6TaZQ5Z6jHReNsNZBXL06SiA5wGtGirgW%2F5dGoRIceP6paAP6cAi03eoBzpFefp556hcAQO8VAlFVybITXJr72i%2BqAQJhQnZGKu4uu1dz%2FRiCRq63qWhJlhLrWgHBgYJglwK0Km7s2zB58be7FWARekdjlXWucPug4den3hp%2FLgh4fB%2Bn%2FmJUWNl2z2WUWh%2FgBhrbw%2FZ7Wmv9N9SCXW2LXAjuCdaD6FMFQuM96FpxhmamMFggzd41H3jYINrJ%2F4D5lyI6WC9lMiVnG%2B6BC1ywdc6tlD%2BjSWLaB0p8%2F%2FHUZqKKTZd%2FRFMw%2F4Pe%2FQU67AE4oTrypN69ZmxuFP%2FDJ5QjDIL4ZdNGuFxoBP46SoDn44Z%2Fsp%2Bofib8SFZCkIo3Peb0rRKE01atFcddH9j3TN8Ft8muloLoPlV4RJu14VPZtwpTt%2BzRth5I1LjtJSw2FVVeEuAb%2BAO3YmlMUc7bRzLDe3dLghSIDLXArz3VhQrAB0vMmWQUbmSoF34B89AjNcv3mYh53jJAzYpx7n8d%2B2mt2xl%2FH1J4DHvmoyn6syHA4MdTiCugNCnLBmGqN1bVn9S6bCe349dftzdRwCoBjDanZ2l0CMhMiK5ZV1bni0vK1WCPR9FQpQRxyPDo3A%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20201120T094441Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYRCMUJEVX%2F20201120%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=b6d1076269a5e78baa96eb7767b830747ebd951f54c72663b69a906be8d1100a&hash=4deb11b77677cd260b84379bebb2c3fcb2bcab1036d6a3c1d95df37b83c2d45b&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S1877050918306100&tid=spdf-fdbaed26-450e-41d4-9f78-2f601327c053&sid=98c7a6d02333b5488f4aa07-ffcec9794cf8gxrqa&type=client
		average_similarity_value = get_average(cluster_SCM_simiarities)
		min_similarity_value = min(cluster_SCM_simiarities)
		max_similarity_value = max(cluster_SCM_simiarities)
		diff_similarity_value = max_similarity_value - min_similarity_value
		k_value = 1.0
		population_similarity_value = (1.0 - ((average_similarity_value - min_similarity_value)/diff_similarity_value)) ** k_value
		#population_fitness_value = population_fitness_function(population_similarity_value)
		population_fitness_value = population_similarity_value
		return population_fitness_value

	def convert_population_fitness_to_SCM_fitness_contribution(population_fitness):
		'''
		This method will take the population fitness and use this to determine what the new coefficients (weights) for the energy and SCM coefficients are.

		:param population_fitness: The population 'fitness value'. This value is some value between 0.0 and 1.0.
		:type  population_fitness: float

		'''
		return population_fitness

	#####################################################################################
	################## Subsidiary Methods for the Energy Fitness Class ##################
	#####################################################################################

	def __assign_population_fitnesses(self,current_generation): 
		"""
		This method is designed to assign fitness values to the clusters of the population only. 

		This methos also returns the cluster_SCM_simiarities which the algorithm then uses to update the c_e and c_SCM values. 

		:param current_generation_no: The current generation.
		:type  current_generation_no: int

		:returns: The similarities of the clusters. These are he sigma 1/2 similarities. 
		:rtype:   list of floats
		
		"""
		# Update the maximum and minimum energy of the population.
		lowest_energy, highest_energy = get_lowest_and_highest_energies_from_collections(self.population, None)
		# Update the maximum and minimum similarities of the population.
		if self.normalise_similarities:
			lowest_similarity, highest_similarity = get_lowest_and_highest_similarities_from_collections(self.population, None, self.cna_database, self.collection_function)
		else:
			lowest_similarity, highest_similarity = None, None
		# Update the fitness of all clusters in the population
		cluster_SCM_simiarities = self.__update_collection_fitnesses(self.population, highest_energy, lowest_energy, highest_similarity, lowest_similarity)
		return cluster_SCM_simiarities

	def __assign_all_fitnesses(self,all_offspring_pools,current_generation): 
		"""
		Update the fitnesses of all clusters in population and all offsprings

		:param all_offspring_pools: All of the offspring_pools
		:type  all_offspring_pools: list of Organisms.GA.Offspring_Pool
		:param current_generation_no: The current generation
		:type  current_generation_no: int

		"""
		if not isinstance(all_offspring_pools,list):
			all_offspring_pools = [all_offspring_pools]
		# Update the maximum and minimum energy of the population and offsprings as a whole.
		lowest_energy, highest_energy = get_lowest_and_highest_energies_from_collections(self.population, all_offspring_pools)
		# Update the maximum and minimum similarities of the population and offsprings as a whole.
		if self.normalise_similarities:
			lowest_similarity, highest_similarity = get_lowest_and_highest_similarities_from_collections(self.population, all_offspring_pools, self.cna_database, self.collection_function)
		else:
			lowest_similarity, highest_similarity = None, None	
		# Update the fitness of all clusters in the population
		cluster_SCM_simiarities = self.__update_collection_fitnesses(self.population, highest_energy, lowest_energy, highest_similarity, lowest_similarity)
		# Update the fitness of all clusters in all the offsprings
		for offspring_pool in all_offspring_pools:
			self.__update_collection_fitnesses(offspring_pool, highest_energy, lowest_energy, highest_similarity, lowest_similarity)

	def __update_collection_fitnesses(self,collection,highest_energy,lowest_energy,highest_similarity,lowest_similarity):
		"""
		The fitness of all the clusters in the collection are updated. The collection could be the population or the offspring_pool

		:param collection: update the fitnesses of clusters in the collection.
		:type  collection: Organisms.GA.Collection.Collection
		:param highest_energy: The highest energy of the clusters in the collection. 
		:type  highest_energy: float
		:param lowest_energy: The lowest energy of the clusters in the collection. 
		:type  lowest_energy: float

		:returns: The similarities of the clusters. These are he sigma 1/2 similarities. 
		:rtype:   list of floats

		"""
		cluster_SCM_simiarities = []
		for cluster in collection:
			fitness, cluster_SCM_simiarity = self.__get_fitness(cluster, highest_energy, lowest_energy, highest_similarity, lowest_similarity)
			cluster.fitness = fitness
			cluster_SCM_simiarities.append(cluster_SCM_simiarity)
		#import pdb; pdb.set_trace()
		return cluster_SCM_simiarities

	def __get_fitness(self,cluster,highest_energy,lowest_energy,highest_similarity,lowest_similarity):
		"""
		Get the fitness of a cluster.

		:param cluster: The cluster to get the fitness of
		:type  cluster: Organisms.GA.Cluster.Cluster
		:param highest_energy: The highest energy of the clusters in the collection. 
		:type  highest_energy: float
		:param lowest_energy: The lowest energy of the clusters in the collection. 
		:type  lowest_energy: float

		:returns: The similarities of the clusters. These are he sigma 1/2 similarities. 
		:rtype:   list of floats

		"""
		fitness_contributions = []
		# get fitness in terms of energy
		if (not self.energy_fitness_contribution == 0.0):
			energy_fitness_contribution = get_energetic_fitness_contribution(cluster,highest_energy,lowest_energy,self.energy_fitness_function)
			fitness_contributions.append(energy_fitness_contribution)
		# get fitness in terms of CNA predation
		if (not self.SCM_fitness_contribution == 0.0) or self.dynamic_mode:
			CNA_fitness_contribution, cluster_SCM_simiarity = self.get_CNA_fitness_contribution(cluster,highest_similarity,lowest_similarity,self.cna_database,self.collection_function,self.cna_fitness_function)
			fitness_contributions.append(CNA_fitness_contribution)
		else:
			cluster_SCM_simiarity = None # Dont need this if self.SCM_fitness_contribution == 0.0 or self.dynamic_mode == False
		# Get the overall fitness
		overall_fitness = dot(self.fitness_weights,fitness_contributions)
		return overall_fitness, cluster_SCM_simiarity

	def add_to_database(self, collection):
		'''
		Add clusters similarities to the CNA database to be stored for future generations. 

		:param collection: update the fitnesses of clusters in the collection.
		:type  collection: Organisms.GA.Collection.Collection
		'''
		self.cna_database.add(collection,initialise=False)

	def remove_from_database(self, cluster_names_to_remove):
		'''
		Clusters to remove from the CNA database

		:param cluster_names_to_remove: A list of the names of all the clusters to remove from the CNA database
		:type  cluster_names_to_remove: list of ints
		'''
		self.cna_database.remove(cluster_names_to_remove) # delete the cluster entrance in the self.cna_database

	def reset(self):
		'''
		Reset the CNA database with no inputs
		'''
		self.cna_database.reset()

	def is_there_an_similarity_range(self,similarity_rounding):
		"""
		Determines if there is a range of similarities in the collection

		:param rounding: The rounding of the similarity of the cluster
		:type  rounding: float

		returns Is there a range of similarities in the collection
		rtype   bool 
		"""
		cluster_similarities = [get_CNA_most_similar_average(cluster,self.cna_database,self.collection_function) for cluster in self.population]
		if round(max(cluster_similarities),similarity_rounding) == round(min(cluster_similarities),similarity_rounding):
			return False
		else:
			return True

	# ------------------------------------------------------------------------------------------------------------------------------------------------------

