def mean(all_cna_averages):
	return (sum(all_cna_averages) / len(all_cna_averages))

def get_CNA_most_similar_average(cluster,cna_database,collection_function):
	cluster_name = cluster.name
	all_cna_averages = cna_database.get_all_averages_for_a_cluster(cluster_name)
	CNA_most_similar_average = float(collection_function(all_cna_averages))
	return CNA_most_similar_average

def get_CNA_fitness_parameter(cluster,cna_database,collection_function):
	"""
	Get the order parameter, based on the CNA, for a cluster. 

	:param cluster: This is the cluster you want to obtain rho_i for.
	:type  cluster: Organisms.GA.Cluster
	:param cna_database: This is an in-memory database (not a ASE disk database) that records the similarities between clusters in the population.
	:type  cna_database: Organisms.GA.SCM_Scripts.CNA_Database
	:param cna_fitness_function: This is the function that converts the rho similarity into a fitness value. 
	:type  cna_fitness_function: __func__

	:returns: CNA_fitness_value: This is the SRM fitness contribution to be used to obtain the fitness valuee 
	:rtypes: float

	"""
	CNA_most_similar_average = get_CNA_most_similar_average(cluster,cna_database,collection_function)
	# Change this to an fitness parameter, where: # Changed 3/12/2018, GRW
	# 	* High similarity -> large fitness parameter -> less favourable for mating and natural selection
	# 	* Low similarity  -> small fitness parameter -> more favourable for mating and natural selection
	CNA_fitness_contribution = (CNA_most_similar_average/100.0) # Note from GRW. This term should be CNA_most_similar_average/100.0
	return CNA_fitness_contribution

def get_CNA_fitness_contribution(cluster,max_similarity,min_minimarity,cna_database,collection_function,cna_fitness_function):
	"""
	Get the fitness, based on the structural diversity as determined by the SCM, for a cluster. 

	:param cluster: This is the cluster you want to obtain rho_i for.
	:type  cluster: Organisms.GA.Cluster
	:param max_similarity: The maximum similarity obtained from the population + offspring_pools. THIS IS NOT USED IN THIS METHOD, IS HERE FOR CONSISTANCY.
	:type  max_similarity: Not needed to be anything
	:param min_minimarity: The minimum similarity obtained from the population + offspring_pools. THIS IS NOT USED IN THIS METHOD, IS HERE FOR CONSISTANCY.
	:type  min_minimarity: Not needed to be anything
	:param cna_database: This is an in-memory database (not a ASE disk database) that records the similarities between clusters in the population.
	:type  cna_database: Organisms.GA.SCM_Scripts.CNA_Database
	:param cna_fitness_function: This is the function that converts the rho similarity into a fitness value. 
	:type  cna_fitness_function: __func__

	"""
	rho_i = get_CNA_fitness_parameter(cluster,cna_database,collection_function)
	fitness = cna_fitness_function.get_fitness(rho_i)
	return fitness, rho_i

# ------------------------------------------------------------------------------------------------------------------------------------------------

def get_CNA_fitness_parameter_normalised(cluster,max_similarity,min_minimarity,cna_database,collection_function):
	"""
	Get the order parameter, based on the CNA, for a cluster. This order parameter is the normalised similarity compared to the similarity of clusters in the population. 

	:param cluster: This is the cluster you want to obtain rho_i for.
	:type  cluster: Organisms.GA.Cluster
	:param max_similarity: The maximum similarity obtained from the population + offspring_pools
	:type  max_similarity: float
	:param min_minimarity: The minimum similarity obtained from the population + offspring_pools
	:type  min_minimarity: float
	:param cna_database: This is an in-memory database (not a ASE disk database) that records the similarities between clusters in the population.
	:type  cna_database: Organisms.GA.SCM_Scripts.CNA_Database
	:param cna_fitness_function: This is the function that converts the rho similarity into a fitness value. 
	:type  cna_fitness_function: __func__

	:returns: CNA_fitness_value: This is the SRM fitness contribution to be used to obtain the fitness valuee 
	:rtypes: float

	"""
	CNA_most_similar_average = get_CNA_most_similar_average(cluster,cna_database,collection_function)
	# Change this to an fitness parameter, where: # Changed 3/12/2018, GRW
	# 	* High similarity -> large fitness parameter -> less favourable for mating and natural selection
	# 	* Low similarity  -> small fitness parameter -> more favourable for mating and natural selection
	CNA_fitness_contribution = (CNA_most_similar_average - min_minimarity)/(max_similarity - min_minimarity) # Note from GRW. This term should be CNA_most_similar_average/100.0
	return CNA_fitness_contribution


def get_CNA_fitness_contribution_normalised(cluster,max_similarity,min_minimarity,cna_database,collection_function,cna_fitness_function):
	"""
	Get the fitness, based on the structural diversity as determined by the SCM, for a cluster. This order parameter is the normalised similarity compared to the similarity of clusters in the population. 

	:param cluster: This is the cluster you want to obtain rho_i for.
	:type  cluster: Organisms.GA.Cluster
	:param max_similarity: The maximum similarity obtained from the population + offspring_pools
	:type  max_similarity: float
	:param min_minimarity: The minimum similarity obtained from the population + offspring_pools
	:type  min_minimarity: float
	:param cna_database: This is an in-memory database (not a ASE disk database) that records the similarities between clusters in the population.
	:type  cna_database: Organisms.GA.SCM_Scripts.CNA_Database
	:param cna_fitness_function: This is the function that converts the rho similarity into a fitness value. 
	:type  cna_fitness_function: __func__

	"""
	rho_i = get_CNA_fitness_parameter_normalised(cluster,max_similarity,min_minimarity,cna_database,collection_function)
	fitness = cna_fitness_function.get_fitness(rho_i)
	return fitness, rho_i

# ------------------------------------------------------------------------------------------------------------------------------------------------

def get_lowest_and_highest_similarities_from_collections(population,collections,cna_database,collection_function):
	"""
	This method will return the value of the highest and lowest similarities from a list of collections that are inputted into this method.
	The collections variable is a list of collections, for example [population,offspring]
	This is a private method.

	:param collections: A list of all the collections that you want to compare..
	:type  collections: list of collection objects

	:returns: the lowest similarity of clusters out of all the inputed collections, the maximum similarity out of all the inputed collections.
	:rtypes: float, float

	"""
	cluster_names = population.get_cluster_names()
	if not collections == None:
		#if not len(collections[0]) == 16:
		#	import pdb; pdb.set_trace()
		for collection in collections:
			cluster_names += collection.get_cluster_names()
	
	lowest_similarity = 101.0
	highest_similarity =  -1.0
	for cluster_name in cluster_names:
		all_cna_averages = cna_database.get_all_averages_for_a_cluster(cluster_name)
		try:
			CNA_most_similar_average = float(collection_function(all_cna_averages))
		except:
			print('Weird CNA fitness contribution issue in CNA_Fitness_Contribution')
			import pdb; pdb.set_trace()
			exit('Exitting')
		if CNA_most_similar_average < lowest_similarity:
			lowest_similarity = CNA_most_similar_average
		if CNA_most_similar_average > highest_similarity:
			highest_similarity = CNA_most_similar_average
	if lowest_similarity == 101.0:
		exit('get_lowest_and_highest_similarities_from_collections, low error')
	if highest_similarity == -1.0:
		exit('get_lowest_and_highest_similarities_from_collections, high error')
	return lowest_similarity, highest_similarity
