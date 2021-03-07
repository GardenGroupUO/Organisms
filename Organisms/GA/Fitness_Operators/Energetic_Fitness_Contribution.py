from Organisms.GA.Collections_Iterator import Collections_Iterator

def get_lowest_and_highest_energies_from_collections(population,collections):
	"""
	This method will return the value of the highest and lowest energy from a list of collections that are inputted into this method.
	The collections variable is a list of collections, for example [population,offspring]
	This is a private method.

	:param collections: A list of all the collections that you want to compare..
	:type  collections: list of collection objects

	:returns: the lowest energy of clusters out of all the inputed collections, the maximum energy out of all the inputed collections.
	:rtypes: float, float

	"""
	lowest_energy  =  population[0].energy
	highest_energy =  population[0].energy
	collections_iterator = Collections_Iterator(population,collections,pass_first_cluster=True)
	for cluster in collections_iterator:
		if cluster.energy < lowest_energy:
			lowest_energy = cluster.energy
		if cluster.energy > highest_energy:
			highest_energy = cluster.energy
	return lowest_energy, highest_energy

##########################################################################################################################################################

def check_rho_i(rho_i,cluster,max_energy,min_energy):
	"""
	This method will check that the rho value for the cluster is within the expected limits. If there are any errors, the program will mention what is wrong and terminate.

	:param rho_i: This is the rho value to check.
	:type  rho_i: float
	:param collection: This is the cluster that contains the associated rho value to check.
	:type  collection: Organisms.GA.Cluster
	:param min_energy: This is the lowest energy of the current lowest energetic structure across all the collections in the GA (e.g. [population, offspring]).
	:type  min_energy: float
	:param max_energy: This is the highest energy of the current highest energetic structure across all the collections in the GA (e.g. [population, offspring]).
	:type  max_energy: float
		
	"""
	if not (0.0 <= rho_i and rho_i <= 1.0):
		print('Error with def check_row_i in Energy_Diversity_Operator.py')
		print('There is no error with this method in Energy_Diversity_Operator.py, there is an error with the Diversity Operator you are using.')
		print('The value of rho must be between 0.0 and 1.0. This is not the case here.')
		print('The value of this rho_i = '+str(rho_i))
		print('Given Cluster: '+str(cluster))
		print('Given Cluster energy: '+str(cluster.energy)+' eV')
		print('Given max_energy: '+str(max_energy)+' eV')
		print('Given min_energy: '+str(min_energy)+' eV')
		print('NOTE:')
		print('Checking if min_energy < cluster.energy < max_energy:')
		print('min_energy <= cluster.energy = '+str(min_energy <= cluster.energy))
		print('cluster.energy <= max_energy = '+str(cluster.energy <= max_energy))
		print('Check this.')
		import pdb; pdb.set_trace()
		exit('This program will now end.')
		
def get_rho_i(cluster,highest_energy,lowest_energy):
	"""
	Get the rho of a cluster. Note that the max and min energy are based on that of the current population. 

	See `Theoretical study of Cu-Au nanoalloy clusters using a genetic algorithm, Darby et al., 116, 1536 (2002); doi: 10.1063/1.1429658 <http://dx.doi.org/10.1063/1.1429658>`_, page 1538 about this fitness equation, including the definition of max_energy and min_energy.

	:param cluster: This is the cluster you want to obtain rho_i for.
	:type  cluster: Cluster
	:param highest_energy: This is the highest energy of the current highest energetic structure across all the collections in the GA (e.g. [population, offspring]).
	:type  highest_energy: float
	:param lowest_energy: This is the lowest energy of the current lowest energetic structure across all the collections in the GA (e.g. [population, offspring]).
	:type  lowest_energy: float

	:returns: The value for rho for the cluster
	:rtypes: float
	"""
	energy_i = float(cluster.energy)
	rho_i = (energy_i - lowest_energy)/(highest_energy - lowest_energy)
	check_rho_i(rho_i,cluster,highest_energy,lowest_energy)
	return rho_i

def get_energetic_fitness_contribution(cluster,highest_energy,lowest_energy,energy_fitness_function):
	"""
	Get the fitness, based on the energy, for a cluster. 

	See `Theoretical study of Cu-Au nanoalloy clusters using a genetic algorithm, Darby et al., 116, 1536 (2002); doi: 10.1063/1.1429658 <http://dx.doi.org/10.1063/1.1429658>`_, page 1538 about this fitness equation, including the definition of max_energy and min_energy.

	:param cluster: This is the cluster you want to obtain rho_i for.
	:type  cluster: Cluster
	:param population: This is the population which will be used to get the max_energy and min_energy to obtain rho_i.
	:type  population: Population

	:returns: The value for energetic fitness value for the cluster
	:rtypes: float
	"""
	rho_i = get_rho_i(cluster,highest_energy,lowest_energy)
	fitness = energy_fitness_function.get_fitness(rho_i)
	return fitness

##########################################################################################################################################################

