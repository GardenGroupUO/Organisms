from Organisms import MakeTrialsProgram

''' ---------------- '''
# This details the elemental and number of atom composition of cluster that the user would like to investigate
cluster_makeup = {"Ne": 38}

# Surface details
surface_details = None

# These are the main variables of the genetic algorithm that with changes could affect the results of the Genetic Algorithm.
pop_size = 20
generations = 10000
no_offspring_per_generation = 16

# These setting indicate how offspring should be made using the Mating and Mutation Proceedures
creating_offspring_mode = "Either_Mating_and_Mutation"
crossover_type = "CAS_random"
mutation_types = [('move_0.75', 1)]
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

# ------------------------------------------------------------------------------------------------------------ #
# This dictionary includes the information required by the diversity scheme
predation_information_Off = {'Predation Operator':'Off'}
predation_information_Energy_energy = {'Predation Operator': 'Energy', 'mode': 'comprehensive', 'minimum_energy_diff': 0.01, 'type_of_comprehensive_scheme': 'energy'}
predation_information_DCM_PD5 = {'Predation Operator': 'IDCM', 'percentage_diff': 5.0}

eq_dist = 1.0 * (2.0**(1.0/6.0))
first_nn = eq_dist; second_nn = (2.0**0.5)*eq_dist; diff = second_nn - first_nn
rCut_low = first_nn + (1.0/3.0)*diff; rCut_low = round(rCut_low,3)
rCut_high = first_nn + (2.0/3.0)*diff; rCut_high = round(round(rCut_high,3)-0.01,3)
rCut_resolution = 78
predation_information_SCM = {'Predation Operator': 'SCM', 'SCM Scheme': 'T-SCM', 'rCut_high': rCut_high, 'rCut_low': rCut_low, 'rCut_resolution': rCut_resolution}
# ------------------------------------------------------------------------------------------------------------ #

# ------------------------------------------------------------------------------------------------------------ #
# This dictionary includes the information required by the fitness scheme
energy_fitness_function_exp  = {'function': 'exponential', 'alpha': 3.0}
SCM_fitness_function_alpha_1 = {'function': 'exponential', 'alpha': 1.0}

fitness_information_energy_exp =  {'Fitness Operator': 'Energy', 'fitness_function': energy_fitness_function_exp}
# ------------------------------------------------------------------------------------------------------------ #

# This dictionary includes the information required to prevent clusters being placed in the population if they are too similar to clusters in this memory_operator
memory_operator_information = {}

# Variables required for the Recording_Cluster.py class/For recording the history as required of the genetic algorithm.
ga_recording_information = {}

# These are last techinical points that the algorithm is designed in mind
force_replace_pop_clusters_with_offspring = True
user_initialised_population_folder = None 
rounding_criteria = 10
print_details = False
no_of_cpus = 1
finish_algorithm_if_found_cluster_energy = {'cluster energy': -173.93, 'round': 2}
total_length_of_running_time = 70.0

# These are the details that will be used to create all the Trials for this set of genetic algorithm experiments.
general_dir_name = 'Data'
NoOfTrials = 1000
Condense_Single_Mention_Experiments = False
making_files_for = 'slurm_JobArrays_packets'
no_of_packets_to_make = 100


# These are the details that are used to create the Job Array for slurm
JobArraysDetails = {}
JobArraysDetails['mode'] = 'JobArray'
JobArraysDetails['project'] = 'uoo02568'
JobArraysDetails['partition'] = 'large'
JobArraysDetails['time'] = '72:00:00'
JobArraysDetails['nodes'] = 1
JobArraysDetails['ntasks_per_node'] = no_of_cpus
JobArraysDetails['mem'] = '1500MB'
JobArraysDetails['email'] = "geoffreywealslurmnotifications@gmail.com"

''' ---------------------------------------------------------------------------------------------------------------- '''

Runs = []

Runs.append(('D_Off_F_Energy_exp',predation_information_Off,fitness_information_energy_exp))
Runs.append(('D_Energy_energy_F_Energy_exp',predation_information_Energy_energy,fitness_information_energy_exp))
Runs.append(('D_DCM_PD5_F_Energy_exp',predation_information_DCM_PD5,fitness_information_energy_exp))
Runs.append(('D_SCM_F_Energy_exp',predation_information_SCM,fitness_information_energy_exp))

rCut_half = (rCut_low + rCut_high)/2.0

import numpy as np
c_SCMs = np.arange(0.0,1.0+0.1,0.1)
for c_SCM in c_SCMs:
	c_SCM = round(c_SCM,1)
	fitness_information_SCM_rCut_half = {'Fitness Operator': 'Structure + Energy', 'SCM Scheme': 'T-SCM', 'rCut': rCut_half, 'SCM_fitness_contribution': c_SCM, 'normalise_similarities': False, 'Dynamic Mode': False, 'energy_fitness_function': energy_fitness_function_exp, 'SCM_fitness_function': SCM_fitness_function_alpha_1}
	Runs.append(('D_Off_F_SCM_1_rCut'+'/'+'c_SCM_'+str(c_SCM)           ,predation_information_Off,fitness_information_SCM_rCut_half))
	Runs.append(('D_Energy_energy_F_SCM_1_rCut'+'/'+'c_SCM_'+str(c_SCM) ,predation_information_Energy_energy,fitness_information_SCM_rCut_half))
	Runs.append(('D_DCM_PD5_F_SCM_1_rCut'+'/'+'c_SCM_'+str(c_SCM)       ,predation_information_DCM_PD5,fitness_information_SCM_rCut_half))
	Runs.append(('D_SCM_F_SCM_1_rCut'+'/'+'c_SCM_'+str(c_SCM)           ,predation_information_SCM,fitness_information_SCM_rCut_half))

''' ---------------------------------------------------------------------------------------------------------------- '''

for folder_name, predation_information, fitness_information in Runs:
	dir_name = general_dir_name+'/'+folder_name
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
