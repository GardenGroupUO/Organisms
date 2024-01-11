from Organisms import MakeTrialsProgram

from RunMinimisation_Cu import Minimisation_Function as Minimisation_Function_Cu
from RunMinimisation_Au import Minimisation_Function as Minimisation_Function_Au
from RunMinimisation_AuPd import Minimisation_Function as Minimisation_Function_AuPd

cluster_makeups = [({"Cu": 37}, Minimisation_Function_Cu), ({"Au": 55}, Minimisation_Function_Au), ({"Au": 21, "Pd": 17}, Minimisation_Function_AuPd)]
genetic_algorithm_systems = [(20,16), (100,80), (50,1)]

for cluster_makeup, Minimisation_Function in cluster_makeups:
	for pop_size, no_offspring_per_generation in genetic_algorithm_systems:
		# Surface details
		surface_details = {}

		# These are the main variables of the genetic algorithm that with changes could affect the results of the Genetic Algorithm.
		generations = 2000

		# These setting indicate how offspring should be made using the Mating and Mutation Proceedures
		creating_offspring_mode = "Either_Mating_and_Mutation" 
		crossover_type = "CAS_weighted"
		mutation_types = [['random', 1.0]]
		chance_of_mutation = 0.1

		# This parameter will tell the Organisms program if an epoch is desired, and how the user would like to proceed.
		epoch_settings = {'epoch mode': 'same population', 'max repeat': 5}

		# These are variables used by the algorithm to make and place clusters in.
		r_ij = 3.4
		cell_length = r_ij * (sum([float(noAtoms) for noAtoms in list(cluster_makeup.values())]) ** (1.0/3.0))
		vacuum_to_add_length = 10.0

		# The RunMinimisation.py algorithm is one set by the user. It contain the def Minimisation_Function
		# That is used for local optimisations. This can be written in whatever way the user wants to perform
		# the local optimisations. This is meant to be as free as possible.

		# This dictionary includes the information required to prevent clusters being placed in the population if they are too similar to clusters in this memory_operator
		memory_operator_information = {'Method': 'Off'}

		# This dictionary includes the information required by the predation scheme
		predation_information = {'Predation Operator':'Energy', 'mode': 'comprehensive', 'minimum_energy_diff': 0.025}

		# This dictionary includes the information required by the fitness scheme
		energy_fitness_function = {'function': 'exponential', 'alpha': 3.0}
		SCM_fitness_function = {'function': 'exponential', 'alpha': 1.0}
		fitness_information = {'Fitness Operator': 'Structure + Energy', 'Use Predation Information': False, 'SCM_fitness_contribution': 0.5, 'Dynamic Mode': False, 'energy_fitness_function': energy_fitness_function, 'SCM_fitness_function': SCM_fitness_function}

		# Variables required for the Recording_Cluster.py class/For recording the history as required of the genetic algorithm.
		ga_recording_information = {}
		ga_recording_information['ga_recording_scheme'] = 'Limit_energy_height' # float('inf')
		ga_recording_information['limit_number_of_clusters_recorded'] = 5 # float('inf')
		ga_recording_information['limit_energy_height_of_clusters_recorded'] = 1.5 #eV
		ga_recording_information['exclude_recording_cluster_screened_by_diversity_scheme'] = True
		ga_recording_information['record_initial_population'] = True
		ga_recording_information['saving_points_of_GA'] = [3,5]

		# These are last techinical points that the algorithm is designed in mind
		force_replace_pop_clusters_with_offspring = True
		user_initialised_population_folder = None 
		rounding_criteria = 10
		print_details = False
		no_of_cpus = 2
		finish_algorithm_if_found_cluster_energy = None
		total_length_of_running_time = None

		''' ---------------- '''
		# These are the details that will be used to create all the Trials for this set of genetic algorithm experiments.
		dir_name = 'ThisIsTheFolderThatScriptsWillBeWrittenTo'
		NoOfTrials = 100
		Condense_Single_Mention_Experiments = True
		making_files_for = 'slurm_JobArrays_full'
		no_of_packets_to_make = None # This does not need a setting in this example as we have set 'making_files_for = 'slurm_JobArrays_full'. This only need to be set to an int if making_files_for = 'slurm_JobArrays_packet'

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
		JobArraysDetails['python version'] = 'Python/3.6.3-gimkl-2017a'

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
			finish_algorithm_if_found_cluster_energy=finish_algorithm_if_found_cluster_energy,
			total_length_of_running_time=total_length_of_running_time,
			no_of_packets_to_make=no_of_packets_to_make)
		''' ---------------- '''
