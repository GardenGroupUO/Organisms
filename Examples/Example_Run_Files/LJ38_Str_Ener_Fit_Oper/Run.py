from Organisms import GA_Program

# This details the elemental and number of atom composition of cluster that the user would like to investigate
cluster_makeup = {'Ne': 38}

# Surface details
surface_details = None

# These are the main variables of the genetic algorithm that with changes could affect the results of the Genetic Algorithm.
pop_size = 20
generations = 4000
no_offspring_per_generation = 16

# These setting indicate how offspring should be made using the Mating and Mutation Proceedures
creating_offspring_mode = "Either_Mating_and_Mutation"
crossover_type = "CAS_random"
mutation_types = [['move', 1]]
chance_of_mutation = 0.1

# This parameter will tell the GGA if an epoch is desired, and how the user would like to proceed.
epoch_settings = {'epoch mode': 'same population', 'max repeat': 5}

# These are variables used by the algorithm to make and place clusters in.
r_ij = 1.5
cell_length = 4.1
vacuum_to_add_length = 10.0

# The RunMinimisation.py algorithm is one set by the user. It contain the def Minimisation_Function
# That is used for local optimisations. This can be written in whatever way the user wants to perform
# the local optimisations. This is meant to be as free as possible.
from RunMinimisation_LJ import Minimisation_Function

# This dictionary includes the information required to prevent clusters being placed in the population if they are too similar to clusters in this memory_operator
memory_operator_information = {'Method': 'Off'}

# This dictionary includes the information required by the predation scheme.
predation_information = {'Predation Operator': 'Energy', 'mode': 'comprehensive', 'type_of_comprehensive_scheme': 'energy', 'minimum_energy_diff': 0.01}

# This dictionary includes the information required by the fitness scheme
# fitness_information = {'Fitness Operator': 'Energy', 'fitness_function': {'function': 'exponential', 'alpha': 3.0}}
fitness_information = {'Fitness Operator': 'SCM + Energy', 'SCM Scheme': 'T-SCM', 'rCut': 1.3495, 'SCM_fitness_contribution': 0.8, 'Dynamic Mode': False, 'Use Predation Information': False, 'energy_fitness_function': {'function': 'exponential', 'alpha': 3.0}, 'SCM_fitness_function': {'function': 'exponential', 'alpha': 1.0}}

# Variables required for the Recording_Cluster.py class/For recording the history as required of the genetic algorithm.
ga_recording_information = {'ga_recording_scheme': 'Limit_energy_height', 'limit_number_of_clusters_recorded': 1, 'limit_energy_height_of_clusters_recorded': 1.0, 'exclude_recording_cluster_screened_by_diversity_scheme': False}

# These are last techinical points that the algorithm is designed in mind
force_replace_pop_clusters_with_offspring = True
user_initialised_population_folder = None
rounding_criteria = 10
print_details = True
no_of_cpus = 1
finish_algorithm_if_found_cluster_energy = {'cluster energy': -173.93, 'round': 2}
total_length_of_running_time = None

''' ---------------- '''
# This will execute the genetic algorithm program
GA_Program(cluster_makeup=cluster_makeup,
    pop_size=pop_size,
    generations=generations,
    no_offspring_per_generation=no_offspring_per_generation,
    creating_offspring_mode=creating_offspring_mode,
    crossover_type=crossover_type,
    mutation_types=mutation_types,
    chance_of_mutation=chance_of_mutation,
    r_ij=r_ij,
    vacuum_to_add_length=vacuum_to_add_length,
    Minimisation_Function=Minimisation_Function,
    surface_details=surface_details,
    epoch_settings=epoch_settings,
    cell_length=cell_length,
    memory_operator_information=memory_operator_information,
    predation_information=predation_information,
    fitness_information=fitness_information,
    ga_recording_information=ga_recording_information,
    force_replace_pop_clusters_with_offspring=force_replace_pop_clusters_with_offspring,
    user_initialised_population_folder=user_initialised_population_folder,
    rounding_criteria=rounding_criteria,
    print_details=print_details,
    no_of_cpus=no_of_cpus,
    finish_algorithm_if_found_cluster_energy=finish_algorithm_if_found_cluster_energy,
    total_length_of_running_time=total_length_of_running_time)
''' ---------------- '''
