'''
Geoffrey Weal, MakeTrialsProgram.py, 10/02/2021

This program is designed to create all the Run.py files and submit.sl/mass_submit.sl that you desire.

This files are ordered into not subdirectories.
'''

import os, sys, inspect
from math import ceil, sqrt
from shutil import copyfile
from Organisms.Subsidiary_Programs.Create_submitSL_slurm_Main import make_submitSL, make_mass_submitSL_full, make_mass_submitSL_packets
 
def makeDirAndMove(folder):
    if not os.path.exists(str(folder)):
        os.makedirs(str(folder))
    os.chdir(str(folder))

def makeDir(folder):
    if not os.path.exists(str(folder)):
        os.makedirs(str(folder))

class MakeTrialsProgram:
    def __init__(self,cluster_makeup,pop_size,generations,no_offspring_per_generation,creating_offspring_mode,crossover_type,mutation_types,chance_of_mutation,r_ij,vacuum_to_add_length,Minimisation_Function,surface_details,epoch_settings,cell_length,memory_operator_information,predation_information,fitness_information,ga_recording_information,force_replace_pop_clusters_with_offspring,user_initialised_population_folder,rounding_criteria,print_details,no_of_cpus,dir_name,NoOfTrials,Condense_Single_Mention_Experiments,JobArraysDetails,making_files_for,finish_algorithm_if_found_cluster_energy=None,total_length_of_running_time=None,no_of_packets_to_make=None): 
        self.cluster_makeup=cluster_makeup
        self.pop_size=pop_size
        self.generations=generations
        self.no_offspring_per_generation=no_offspring_per_generation
        self.creating_offspring_mode=creating_offspring_mode
        self.crossover_type=crossover_type
        self.mutation_types=mutation_types
        self.chance_of_mutation=chance_of_mutation
        self.r_ij=r_ij
        self.vacuum_to_add_length=vacuum_to_add_length

        self.RunMinimisation_filename=os.path.relpath(inspect.getfile(Minimisation_Function)).replace('.py','').replace('/','.')
        self.Minimisation_Function_name=Minimisation_Function.__name__
        
        self.surface_details=surface_details
        self.epoch_settings=epoch_settings
        self.cell_length=cell_length
        self.memory_operator_information=memory_operator_information
        self.predation_information=predation_information
        self.fitness_information=fitness_information
        self.make_ga_recording_information_dict(ga_recording_information)
        self.force_replace_pop_clusters_with_offspring = force_replace_pop_clusters_with_offspring
        if user_initialised_population_folder in [None, 'None', 'none']:
            self.user_initialised_population_folder = None
        else:
            self.user_initialised_population_folder=os.path.abspath(user_initialised_population_folder)
        self.rounding_criteria=rounding_criteria
        self.print_details=print_details
        self.no_of_cpus=no_of_cpus
        self.finish_algorithm_if_found_cluster_energy=finish_algorithm_if_found_cluster_energy
        self.total_length_of_running_time=total_length_of_running_time

        self.dir_name=dir_name
        self.NoOfTrials=NoOfTrials
        self.making_files_for=making_files_for
        if self.making_files_for == 'slurm_JobArrays_packets':
            self.no_of_packets_to_make = no_of_packets_to_make
        self.Condense_Single_Mention_Experiments=Condense_Single_Mention_Experiments
        self.JobArraysDetails=JobArraysDetails
        if 'partition' not in self.JobArraysDetails:
            self.JobArraysDetails['partition'] = 'large'
        if 'python version' not in self.JobArraysDetails:
            self.JobArraysDetails['python version'] = 'Python/3.6.3-gimkl-2017a'
        self.check_inputs()
        self.MakeTrials()
        print('Created Multiple Trials files for Slurm')

    def make_ga_recording_information_dict(self,ga_recording_information):
        self.ga_recording_information = ga_recording_information
        if 'limit_number_of_clusters_recorded' in self.ga_recording_information and self.ga_recording_information['limit_number_of_clusters_recorded'] in ['inf', float('inf')]:
            self.ga_recording_information['limit_number_of_clusters_recorded'] = "inf"
        if 'limit_energy_height_of_clusters_recorded' in self.ga_recording_information and self.ga_recording_information['limit_number_of_clusters_recorded'] in ['inf', float('inf')]:
            self.ga_recording_information['limit_energy_height_of_clusters_recorded'] = "inf" #eV
        #import pdb; pdb.set_trace()

    def check_inputs(self):
        # Double check to make sure all things are in order.
        pass

    def MakeTrials(self):
        if self.making_files_for == 'individual':
            self.make_individual_trials()
        if self.making_files_for.startswith('slurm_JobArrays'):
            self.make_slurm_jobarray_files()

    def make_individual_trials(self):
        subdirname = self.get_folder_details_name()
        for trial_no in range(1,self.NoOfTrials+1):
            path_to = self.dir_name+'/'+subdirname+'/Trial'+str(trial_no)
            makeDir(path_to)
            #Write the Run.py file
            self.makeRunPY(path_to,self.cluster_makeup,self.pop_size,self.generations,self.no_offspring_per_generation,
                self.creating_offspring_mode,self.crossover_type,self.mutation_types,self.chance_of_mutation,self.r_ij,self.vacuum_to_add_length,
                self.RunMinimisation_filename,self.Minimisation_Function_name,self.surface_details,self.epoch_settings,self.cell_length,
                self.memory_operator_information,self.predation_information,self.fitness_information,self.ga_recording_information,
                self.force_replace_pop_clusters_with_offspring,self.user_initialised_population_folder,self.rounding_criteria,self.print_details,
                self.no_of_cpus,self.finish_algorithm_if_found_cluster_energy,self.total_length_of_running_time)
            # Copy the RunMinimisation.py file
            RunMinimisationPY_path = self.copyRunMinimisationPY(os.getcwd(), self.RunMinimisation_filename) # self.Minimisation_Function.__name__)
            self.PasteRunMinimisationPY(RunMinimisationPY_path, path_to, self.RunMinimisation_filename)
            # Make the submit.sl file for slurm
            make_submitSL(path_to,self.JobArraysDetails['project'],self.JobArraysDetails['time'],self.JobArraysDetails['nodes'],self.JobArraysDetails['ntasks_per_node'],self.JobArraysDetails['mem'],self.JobArraysDetails['partition'],self.JobArraysDetails['email'],self.JobArraysDetails['python version'])

    def make_slurm_jobarray_files(self):
        subdirname = self.get_folder_details_name()
        path_to = self.dir_name+'/'+subdirname
        makeDir(path_to)
        print('Making Run.py file in '+str(path_to))
        self.makeRunPY(path_to,self.cluster_makeup,self.pop_size,self.generations,self.no_offspring_per_generation,
            self.creating_offspring_mode,self.crossover_type,self.mutation_types,self.chance_of_mutation,self.r_ij,self.vacuum_to_add_length,
            self.RunMinimisation_filename,self.Minimisation_Function_name,self.surface_details,self.epoch_settings,self.cell_length,
            self.memory_operator_information,self.predation_information,self.fitness_information,self.ga_recording_information,
            self.force_replace_pop_clusters_with_offspring,self.user_initialised_population_folder,self.rounding_criteria,self.print_details,
            self.no_of_cpus,self.finish_algorithm_if_found_cluster_energy,self.total_length_of_running_time)
        # Copy the RunMinimisation.py file
        RunMinimisationPY_path = self.copyRunMinimisationPY(os.getcwd(), self.RunMinimisation_filename) # self.Minimisation_Function.__name__)
        self.PasteRunMinimisationPY(RunMinimisationPY_path, path_to, self.RunMinimisation_filename)
        # Make the submit.sl file for slurm
        if self.making_files_for == 'slurm_JobArrays_full':
            make_mass_submitSL_full(path_to,self.JobArraysDetails['project'],self.NoOfTrials,self.JobArraysDetails['time'],self.JobArraysDetails['nodes'],self.JobArraysDetails['ntasks_per_node'],self.JobArraysDetails['mem'],self.JobArraysDetails['partition'],self.JobArraysDetails['email'],self.RunMinimisation_filename,self.JobArraysDetails['python version'])
        elif self.making_files_for == 'slurm_JobArrays_packets':
            print('======================================================================')
            print('======================================================================')
            print()
            print('NOTE: YOU ARE USING slurm_JobArrays_packets')
            print()
            print('This will make slurm run a set of genetic algorithm trials within a single array')
            print('Only use this if your genetic algorithm will take less than 10 minutes to run')
            print('We have had issues if you run genetic algorithm trials where each GA takes over an hour to run with slurm_JobArrays_packets')
            print('Avoid this')
            print()
            print("You should only use this if you know your packet of GA trials will finish within the time you have given for JobArraysDetails['time'].")
            print()
            print('If each of your GA trials will take over an hour to complete, rerun this program but set making_files_for = "slurm_JobArrays_full"')
            print()
            print("Also Note, make sure you have set JobArraysDetails['time'] is set to as long as possible to avoid further issues.")
            print('======================================================================')
            print('======================================================================')
            make_mass_submitSL_packets(path_to,self.JobArraysDetails['project'],self.NoOfTrials,self.no_of_packets_to_make,self.JobArraysDetails['time'],self.JobArraysDetails['nodes'],self.JobArraysDetails['ntasks_per_node'],self.JobArraysDetails['mem'],self.JobArraysDetails['partition'],self.JobArraysDetails['email'],self.RunMinimisation_filename,self.JobArraysDetails['python version'])
        else:
            exit('Error, "making_files_for" must be either "slurm_JobArrays_full" or "slurm_JobArrays_packets". making_files_for = '+str(self.making_files_for))

    def get_folder_details_name(self):
        cluster_symbol_name = '_'.join(str(symbol) for symbol, number in self.cluster_makeup.items())
        cluster_makeup_name = ''.join((str(symbol)+str(number)) for symbol, number in self.cluster_makeup.items())
        if self.Condense_Single_Mention_Experiments:
            dirname = str(cluster_makeup_name)+'_P'+str(self.pop_size)+'_O'+str(self.no_offspring_per_generation)
        else:
            dirname = str(cluster_symbol_name)+'/'+str(cluster_makeup_name)+'/PopSize'+str(self.pop_size)+'/OffPerGenEquals'+str(self.no_offspring_per_generation)
        return dirname

    def makeRunPY(self,path_to,cluster_makeup,pop_size,generations,no_offspring_per_generation,creating_offspring_mode,crossover_type,mutation_types,chance_of_mutation,r_ij,vacuum_to_add_length,RunMinimisation_filename,Minimisation_Function_name,surface_details,epoch_settings,cell_length,memory_operator_information,predation_information,fitness_information,ga_recording_information,force_replace_pop_clusters_with_offspring,user_initialised_population_folder,rounding_criteria,print_details,no_of_cpus,finish_algorithm_if_found_cluster_energy,total_length_of_running_time):
        with open(path_to+'/Run.py','w+') as RunPY:
            print('from Organisms import GA_Program',file=RunPY)
            print('',file=RunPY)
            print('# This details the elemental and number of atom composition of cluster that the user would like to investigate',file=RunPY)
            print('',file=RunPY)
            print('cluster_makeup = '+str(cluster_makeup),file=RunPY)
            print('',file=RunPY)
            print('# Surface details',file=RunPY)
            print('surface_details = '+str(surface_details),file=RunPY)
            print('',file=RunPY)
            print('# These are the main variables of the genetic algorithm that with changes could affect the results of the Genetic Algorithm.',file=RunPY)
            print('pop_size = '+str(pop_size),file=RunPY)
            print('generations = '+str(generations),file=RunPY)
            print('no_offspring_per_generation = '+str(no_offspring_per_generation),file=RunPY)
            print('',file=RunPY)
            print('# These setting indicate how offspring should be made using the Mating and Mutation Proceedures',file=RunPY)
            print('creating_offspring_mode = "'+str(creating_offspring_mode)+'"',file=RunPY)
            print('crossover_type = "'+str(crossover_type)+'"',file=RunPY)
            print('mutation_types = '+str(mutation_types),file=RunPY)
            print('chance_of_mutation = '+str(chance_of_mutation),file=RunPY)
            print('',file=RunPY)
            print('# This parameter will tell the Organisms program if an epoch is desired, and how the user would like to proceed.',file=RunPY)
            print("epoch_settings = "+str(epoch_settings),file=RunPY)
            print('',file=RunPY)
            print('# These are variables used by the algorithm to make and place clusters in.',file=RunPY)
            print('r_ij = '+str(r_ij),file=RunPY)
            print('cell_length = '+str(cell_length),file=RunPY)
            print('vacuum_to_add_length = '+str(vacuum_to_add_length),file=RunPY)
            print('',file=RunPY)
            print('# The RunMinimisation.py algorithm is one set by the user. It contain the def Minimisation_Function',file=RunPY)
            print('# That is used for local optimisations. This can be written in whatever way the user wants to perform',file=RunPY)
            print('# the local optimisations. This is meant to be as free as possible.',file=RunPY)
            print('from '+str(RunMinimisation_filename)+' import '+str(Minimisation_Function_name),file=RunPY)
            print('',file=RunPY)
            print('# This dictionary includes the information required to prevent clusters being placed in the population if they are too similar to clusters in this memory_operator',file=RunPY)
            print('memory_operator_information = '+str(memory_operator_information),file=RunPY)
            print('',file=RunPY)
            print('# This dictionary includes the information required by the predation scheme.',file=RunPY)
            print('predation_information = '+str(predation_information),file=RunPY)
            print('',file=RunPY)
            print('# This dictionary includes the information required by the fitness scheme',file=RunPY)
            print('fitness_information = '+str(fitness_information),file=RunPY)
            print('',file=RunPY)
            print('# Variables required for the Recording_Cluster.py class/For recording the history as required of the genetic algorithm.',file=RunPY)
            print('ga_recording_information = '+str(ga_recording_information),file=RunPY)
            print('',file=RunPY)
            print('# These are last techinical points that the algorithm is designed in mind',file=RunPY)
            print('force_replace_pop_clusters_with_offspring = '+str(force_replace_pop_clusters_with_offspring),file=RunPY)
            if user_initialised_population_folder in [None, 'None', 'none']:
                print('user_initialised_population_folder = None',file=RunPY)
            else:
                print('user_initialised_population_folder = "'+str(user_initialised_population_folder)+'"',file=RunPY)
            print('rounding_criteria = '+str(rounding_criteria),file=RunPY)
            print('print_details = '+str(print_details),file=RunPY)
            print('no_of_cpus = '+str(no_of_cpus),file=RunPY)
            if finish_algorithm_if_found_cluster_energy:
                print('finish_algorithm_if_found_cluster_energy = '+str(finish_algorithm_if_found_cluster_energy),file=RunPY)
            else:
                print('finish_algorithm_if_found_cluster_energy = None',file=RunPY)
            if total_length_of_running_time:
                print('total_length_of_running_time = '+str(total_length_of_running_time),file=RunPY)
            else:
                print('total_length_of_running_time = None',file=RunPY)
            print('',file=RunPY)
            print("''' ---------------- '''",file=RunPY)
            print('GA_Program(cluster_makeup=cluster_makeup,',file=RunPY)
            print('    pop_size=pop_size,',file=RunPY)
            print('    generations=generations,',file=RunPY)
            print('    no_offspring_per_generation=no_offspring_per_generation,',file=RunPY)
            print('    creating_offspring_mode=creating_offspring_mode,',file=RunPY)
            print('    crossover_type=crossover_type,',file=RunPY)
            print('    mutation_types=mutation_types,',file=RunPY)
            print('    chance_of_mutation=chance_of_mutation,',file=RunPY)
            print('    r_ij=r_ij,',file=RunPY)
            print('    vacuum_to_add_length=vacuum_to_add_length,',file=RunPY)
            print('    Minimisation_Function=Minimisation_Function,',file=RunPY)
            print('    surface_details=surface_details,',file=RunPY)
            print('    epoch_settings=epoch_settings,',file=RunPY)
            print('    cell_length=cell_length,',file=RunPY)
            print('    memory_operator_information=memory_operator_information,',file=RunPY)
            print('    predation_information=predation_information,',file=RunPY)
            print('    fitness_information=fitness_information,',file=RunPY)
            print('    ga_recording_information=ga_recording_information,',file=RunPY)
            print('    force_replace_pop_clusters_with_offspring=force_replace_pop_clusters_with_offspring,',file=RunPY)
            print('    user_initialised_population_folder=user_initialised_population_folder,',file=RunPY)
            print('    rounding_criteria=rounding_criteria,',file=RunPY)
            print('    print_details=print_details,',file=RunPY)
            if not finish_algorithm_if_found_cluster_energy:
                print('    no_of_cpus=no_of_cpus,',file=RunPY)
                print('    total_length_of_running_time=total_length_of_running_time)',file=RunPY)
            else:
                print('    no_of_cpus=no_of_cpus,',file=RunPY)
                print('    finish_algorithm_if_found_cluster_energy=finish_algorithm_if_found_cluster_energy,',file=RunPY)
                print('    total_length_of_running_time=total_length_of_running_time)',file=RunPY)
            print("''' ---------------- '''",file=RunPY)

    ##########################################################################################################

    def copyRunMinimisationPY(self, path_to, RunMinimisation_Name):
        RunMinimisationPY_path = path_to+'/'+RunMinimisation_Name+'.py'
        return RunMinimisationPY_path

    def PasteRunMinimisationPY(self,RunMinimisationPY_path,path_to,RunMinimisation_Name=None):
        if RunMinimisation_Name == None:
            RunMinimisation_Path = os.path.basename(os.path.normpath(RunMinimisationPY_path))
        else:
            RunMinimisation_Path = path_to+'/'+RunMinimisation_Name+'.py'
        copyfile(RunMinimisationPY_path,os.getcwd()+'/'+RunMinimisation_Path)

    ##########################################################################################################

    def writeDetails(self,cluster_makeup,nPool,generations,noOffspringPerGeneration,Creating_Offspring_Mode,crossType,ChanceOfMutation,mutTypes,r_ij,boxtoplaceinlength,vacuumAdd,RunMinimisation_Name,Predation_Information,recording_cluster_scheme_information,write_folders,write_Initial_Population_folder,user_initialised_population_folder,rounding_criteria):
        with open('Genetic_Algorithm_Run_Information.txt','w') as InfoTXT:
            InfoTXT.write('===========================================================================================\n')
            InfoTXT.write('===========================================================================================\n')
            InfoTXT.write('Here provides all the information about this set of repeated Genetic Algorithm experiments.\n')
            InfoTXT.write('===========================================================================================\n')
            InfoTXT.write('===========================================================================================\n')
            InfoTXT.write('\n')
            InfoTXT.write('-----------------\n')
            InfoTXT.write('Makeup of Cluster\n')
            InfoTXT.write('-----------------\n')
            InfoTXT.write('This details the elemental and number of atom composition of cluster that the user would like to investigate\n')
            InfoTXT.write('\n')
            InfoTXT.write('Atomic Makeup of the Cluster: '+str(cluster_makeup)+'\n')
            InfoTXT.write('\n')
            InfoTXT.write('-------------------------------------------\n')
            InfoTXT.write('General Details about the Genetic Algorithm\n')
            InfoTXT.write('-------------------------------------------\n')
            InfoTXT.write('These are the main variables of the genetic algorithm that with changes could affect the results of the Genetic Algorithm.\n')
            InfoTXT.write('\n')
            InfoTXT.write('Population Size: '+str(nPool)+'\n')
            InfoTXT.write('Number of Generations: '+str(generations)+'\n')
            InfoTXT.write('Number of Offspring Generated per Generation: '+str(noOffspringPerGeneration)+'\n')
            InfoTXT.write('\n')
            InfoTXT.write('-------------------------------------------------\n')
            InfoTXT.write('Details about the Mating and Mutation Procedures\n')
            InfoTXT.write('-------------------------------------------------\n')
            InfoTXT.write('These setting indicate how offspring should be made using the Mating and Mutation Procedures\n')
            InfoTXT.write('\n')
            InfoTXT.write('Mate and/or Mutate? (both/either): '+str(Creating_Offspring_Mode)+'\n')
            InfoTXT.write('Mating Procedure: '+str(crossType)+'\n')
            InfoTXT.write('Mutation Procedure (and chance they will occur out of 1): '+str(mutTypes)+'\n')
            InfoTXT.write('Chance of a Mutation Occurring: '+str(ChanceOfMutation)+' ('+str(float(ChanceOfMutation)*100.0)+' %)'+'\n')
            InfoTXT.write('\n')
            InfoTXT.write('-------------------------------------------------\n')
            InfoTXT.write('Other General Details about the Genetic Algorithm\n')
            InfoTXT.write('-------------------------------------------------\n')
            InfoTXT.write('These are variables used by the algorithm to make and place clusters in.\n')
            InfoTXT.write('\n')
            InfoTXT.write('r_ij: '+str(r_ij)+'\n')
            InfoTXT.write('boxtoplaceinlength: '+str(boxtoplaceinlength)+'\n')
            InfoTXT.write('vacuumAdd (vacuum to add around cluster): '+str(vacuumAdd)+'\n')
            InfoTXT.write('\n')
            InfoTXT.write('-------------------------\n')
            InfoTXT.write('Local Minimisation Script\n')
            InfoTXT.write('-------------------------\n')
            InfoTXT.write('The RunMinimisation.py algorithm is one set by the user. It contain the def Minimisation_Function\n')
            InfoTXT.write('That is used for local optimisations. This can be written in whatever way the user wants to perform\n')
            InfoTXT.write('the local optimisations. This is meant to be as free as possible.\n')
            InfoTXT.write('\n')
            InfoTXT.write('Local Minimisation Script Name: '+str(RunMinimisation_Name)+'\n')
            InfoTXT.write('\n')
            InfoTXT.write('----------------------------\n')
            InfoTXT.write('Predation Scheme Information\n')
            InfoTXT.write('----------------------------\n')
            InfoTXT.write('This switch tells the genetic algorithm the type of predation scheme they want to place on the genetic algoithm.\n')
            InfoTXT.write('\n')
            for Predation_entry in Predation_Information:
                InfoTXT.write(str(Predation_entry)+': '+str(Predation_Information[Predation_entry])+'\n')
            InfoTXT.write('\n')
            InfoTXT.write('------------------------------\n')
            InfoTXT.write('Recording Clusters Information\n')
            InfoTXT.write('------------------------------\n')
            InfoTXT.write('Place all the recording_cluster_scheme_information variables together into a list as below\n')
            InfoTXT.write('\n')
            for recording_cluster_entry in recording_cluster_scheme_information:
                InfoTXT.write(str(recording_cluster_entry)+': '+str(recording_cluster_scheme_information[recording_cluster_entry])+'\n')
            InfoTXT.write('\n')
            InfoTXT.write('--------------\n')
            InfoTXT.write('Other Settings\n')
            InfoTXT.write('--------------\n')
            InfoTXT.write('These are last techinical points that the algorithm is designed in mind\n')
            InfoTXT.write('\n')
            InfoTXT.write('write_folders: '+str(write_folders)+'\n')
            InfoTXT.write('write_Initial_Population_folder: '+str(write_Initial_Population_folder)+'\n')
            InfoTXT.write('user_initialised_population_folder: '+str(user_initialised_population_folder)+'\n')
            InfoTXT.write('rounding_criteria: '+str(rounding_criteria)+'\n')
