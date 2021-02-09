import os, sys, time

from Organisms import __version__

def get_version_number():
	version = __version__
	return version

def version_no():
	"""
	Will provide the version of the Organisms program
	"""
	path = __file__
	version = get_version_number() 
	return version

def GA_Program_Logo():
	"""
	Provides the opening logo for the Organisms program.
	"""
	print("")
	print(".--------------------------------------------------------------------------.")
	print("|                             ,                                            |")
	print("|              ,_     ,     .'<_                                           |")
	print("|             _> `'-,'(__.-' __<                                           |")
	print("|             >_.--(.. )  =;`                                   _          |")
	print("|                  `V-'`'\\/``                                  ('>         |")
	print("|                                                              /))@@@@@.   |")
	print('|         .----------------------------------.                /@"@@@@@()@  |')
	print("|         | Welcome to the Organisms program |               .@@()@@()@@@@ |")
	print("|         '----------------------------------'               @@@O@@@@()@@@ |")
	print("|                  ^                                         @()@@\\@@@()@@ |")
	print("|  _     (\\_/)     |                                          @()@||@@@@@' |")
	print("| ( \\    (0.o) ----'                 _                         '@@||@@@'   |")
	print("|  ) )   (> <)                     _(_)_            wWWWw   _     ||       |")
	print("| ( (  .-'''''-.  A.-.A      @@@@ (_)@(_)       _   (___) _(_)_   ||       |")
	print("|  \\ \\/         \\/ , , \\    @@()@@  (_)\\      _(_)_   Y  (_)@(_)  ||       |")
	print("|   \\   \\        ;= t =/     @@@@      `|/   (_)@(_) \\|/   (_)\\   ||       |")
	print("|    \\   |'''''-   ,--'       /        \\|     /(_)    |/      |   ||       |")
	print("|     / //     | ||        \\ |          | / \\|/      \\|      \\|/  ||       |")
	print("|    /_,))     |_'))       \\\\|//     \\\\\\|// \\|///   \\\\|//  \\\\\\|// ||       |")
	print("|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^|")
	print("'--------------------------------------------------------------------------'")
	print("")

def Introducing_Remarks(self):
	"""
	Provides information about the settings for your Organisms run.
	"""
	line_length = 60
	print('#'*line_length)
	print('#'*line_length)
	print('#'*line_length)
	print('The Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similarity (Organisms) Program')
	GA_Program_Logo()
	print('Version: '+str(version_no()))
	print('#'*line_length)
	print('#'*line_length)
	time.sleep(1)
	print('')
	print('This algorithm is designed to perform a genetic algorithm to obtain low energetic structures for a given cluster composition.')
	print('')
	print('This genetic algorithm will proceed with the following input parameters')
	print('')
	print('# This details the elemental and number of atom composition of cluster that the user would like to investigate')
	print('cluster_makeup = '+str(self.cluster_makeup))
	print('')
	print('# This details the information used to perform a global optimisation upon a chosen surface')
	print('surface_details = '+str(self.surface_details))
	print('')
	print('# These are the main variables of the genetic algorithm that with changes could affect the results of the Genetic Algorithm.')
	print('pop_size = '+str(self.pop_size))
	print('generations = '+str(self.generations))
	print('no_offspring_per_generation = '+str(self.no_offspring_per_generation))
	print('')
	print('# These setting indicate how offspring should be made using the Mating and Mutation Proceedures')
	print('creating_offspring_mode = '+str(self.creating_offspring_mode))
	print('crossover_type = '+str(self.crossover_type))
	print('mutation_types = '+str(self.mutation_types))
	print('mutation_types = '+str(self.chance_of_mutation))
	print('')
	print('# These are variables used by the algorithm to make and place clusters in.')
	print('r_ij = '+str(self.r_ij)+' Angstroms (This is the maximum possible bond length between two atoms in the cluster)')
	print('cell_length = '+str(self.cell_length)+' Angstroms')
	print('vacuum_to_add_length = '+str(self.vacuum_to_add_length)+' Angstroms')
	print('')
	print('# The RunMinimisation.py algorithm is one set by the user. It contain the def Minimisation_Function')
	print('# That is used for local optimisations. This can be written in whatever way the user wants to perform')
	print('# the local optimisations. This is meant to be as free as possible.')
	print('Minimisation_Function = '+str(self.Minimisation_Function))
	Minimisation_Function_script = self.Minimisation_Function.__module__
	Minimisation_Function_script_location = os.path.dirname(sys.modules[Minimisation_Function_script].__file__)
	print('Path of Minimisation_Function: '+str(Minimisation_Function_script_location+'/'+Minimisation_Function_script+'.py'))
	print('')
	print('# This details the information about the memory operator used in this genetic algorithm.')
	print('memory_operator = '+str(self.memory_operator))
	print('')
	print('# This details the information about the predation operator used in this genetic algorithm.')
	print('predation_operator = '+str(self.predation_operator))
	print('')
	print('# This details the information about the fitness operator used in this genetic algorithm.')
	print('fitness_operator = '+str(self.fitness_operator))
	print('')
	print('# This parameter will tell the Organisms program if an epoch is desired, and how the user would like to proceed.')
	print('epoch_settings: '+str(self.epoch))
	print('')
	print('# Variables required for the GA_Recording_System.py class/For recording the history as required of the genetic algorithm.')
	print('ga_recording_system = '+str(self.ga_recording_system))
	print('')
	print('# These are last techinical points that the algorithm is designed in mind')
	print('force_replace_pop_clusters_with_offspring = '+str(self.force_replace_pop_clusters_with_offspring))
	print('user_initialised_population_folder = '+str(self.user_initialised_population_folder))
	print('rounding_criteria = '+str(self.rounding_criteria))
	print('print_details = '+str(self.print_details))
	print('no_of_cpus = '+str(self.no_of_cpus))
	print('finish_algorithm_if_found_cluster_energy = '+str(self.finish_algorithm_if_found_cluster_energy))
	print('total_length_of_running_time: '+str(self.timer.get_total_length_of_running_time()))
	print('')
	print('#'*line_length)
	print('#'*line_length)
	print('#'*line_length)