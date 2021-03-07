

def get_average(fitnesses):
	sum_of_fitnesses = sum(fitnesses)
	average = float(sum_of_fitnesses)/len(fitnesses)
	return average

def get_population_fitness(cluster_SCM_simiarities,population_fitness_function):
	population_average_similarity = get_average(cluster_SCM_simiarities)
	population_fitness = population_fitness_function.get_fitness(population_average_similarity)
	return population_fitness


