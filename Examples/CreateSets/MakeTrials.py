import os, inspect
from Organisms import MakeTrialsProgram

''' ---------------- '''
#Get the input data to run all your Trials
from Run import cluster_makeup, surface_details, pop_size, generations, no_offspring_per_generation, creating_offspring_mode, crossover_type, mutation_types, chance_of_mutation, epoch_settings, r_ij, vacuum_to_add_length, Minimisation_Function, cluster_makeup, cell_length, memory_operator_information, predation_information, fitness_information, ga_recording_information, force_replace_pop_clusters_with_offspring, user_initialised_population_folder, rounding_criteria, print_details, no_of_cpus, finish_algorithm_if_found_cluster_energy

''' ---------------- '''
# These are the details that will be used to create all the Trials for this set of genetic algorithm experiments.
dir_name = 'ThisIsTheFolderThatScriptsWillBeWrittenTo'
NoOfTrials = 100
Condense_Single_Mention_Experiments = True
making_files_for = 'slurm_JobArrays'

''' ---------------- '''
# These are the details that are used to create the Job Array for slurm
JobArraysDetails = {}
JobArraysDetails['mode'] = 'JobArray'
JobArraysDetails['project'] = 'uoo00084'
JobArraysDetails['time'] = '8:00:00'
JobArraysDetails['nodes'] = 1
JobArraysDetails['ntasks_per_node'] = no_of_cpus
JobArraysDetails['mem'] = '1G'
JobArraysDetails['email'] = "geoffreywealslurmnotifications@gmail.com"

''' ---------------- '''
# Write all the trials that the user desires
MakeTrialsProgram(cluster_makeup=cluster_makeup,
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
	dir_name=dir_name,
	NoOfTrials=NoOfTrials,
	Condense_Single_Mention_Experiments=Condense_Single_Mention_Experiments,
	JobArraysDetails=JobArraysDetails,
	making_files_for=making_files_for,
	finish_algorithm_if_found_cluster_energy=finish_algorithm_if_found_cluster_energy)