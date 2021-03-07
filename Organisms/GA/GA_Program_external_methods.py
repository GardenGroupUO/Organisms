import os
import math
from Organisms.GA.Lock import Lock_Remove

def if_to_finish_because_found_cluster_energy(self, all_energies_of_offpsring):
	if not self.finish_algorithm_if_found_cluster_energy == None:
		for cluster in self.population:
			if round(cluster.energy,self.finish_algorithm_if_found_cluster_rounding) == self.finish_algorithm_if_found_cluster_energy:
				self.energyprofile.add_found_LES_note()
				return True
		for offspring_energy in all_energies_of_offpsring:
			if round(offspring_energy,self.finish_algorithm_if_found_cluster_rounding) == self.finish_algorithm_if_found_cluster_energy:
				self.energyprofile.add_found_LES_note()
				return True
	return False

def check_for_duplicates(collection_cluster_names):
	if len(collection_cluster_names) == len(set(collection_cluster_names)):
		return False
	else:
		return True

def check_names_1(population):	
	pop_cluster_names = population.get_cluster_names()
	if check_for_duplicates(pop_cluster_names):
		print('Error in def check_names, in GA_Program.py')
		print('We have found duplicates in both the population')
		print('pop_cluster_names: '+str(pop_cluster_names.sort()))
		print('Check this out')
		Lock_Remove()
		raise Exception('Program finishing without completing')

def check_names_2(population,offspring_pool):
	pop_cluster_names = population.get_cluster_names()
	off_cluster_names = offspring_pool.get_cluster_names()
	if check_for_duplicates(off_cluster_names):
		print('Error in def check_names, in GA_Program.py')
		print('We have found duplicates in both the population')
		print('off_cluster_names: '+str(off_cluster_names.sort()))
		print('Check this out')
		Lock_Remove()
		raise Exception('Program finishing without completing')
	check = any(cluster_name in off_cluster_names for cluster_name in pop_cluster_names)
	if check:
		print('Error in def check_names, in GA_Program.py')
		print('We have found the cluster with the same name in both the offspring and population')
		print('pop_cluster_names: '+str(pop_cluster_names))
		print('off_cluster_names: '+str(off_cluster_names))
		duplicate_clusters = []
		for cluster_name in pop_cluster_names:
			if cluster_name in off_cluster_names:
				duplicate_clusters.append(cluster_name)
		print('The cluster names in the population and offspring: '+str(duplicate_clusters))
		print('Check this out')
		Lock_Remove()
		raise Exception('Program finishing without completing')

def remove_cluster_files(self):
	"""
	Will remove the xyz or database files when the Organisms program is finished. However, it is recommended that you keep the population database or xyz files when the Organisms program finishes, just in case you would like to extend the Organisms program to perform more generations.
	"""
	if self.remove_cluster_files_at_end:
		self.population.delete_collection()

def add_metadata(self):
	"""
	This is included as this seems to not be added to the collections database when it is first created. Fixing an issue with ASE.
	"""
	self.ga_recording_system.add_metadata()
	self.population.add_metadata()
	#self.offspring_pool.add_metadata()

def floor_float(number,decimal_place):
	number_up = 10.0 ** float(decimal_place)
	return math.floor(float(number) * number_up)/number_up

def reset_population(self,generation_number):
	population_reset_settings = (self.cluster_makeup, self.surface, self.Minimisation_Function, self.memory_operator, self.predation_operator, self.fitness_operator, self.epoch, self.cell_length, self.vacuum_to_add_length, self.r_ij, self.rounding_criteria, self.no_of_cpus, self.previous_cluster_name)
	epoch_due_to_population_energy_convergence = not self.population.is_there_an_energy_range(self.rounding_criteria)
	self.previous_cluster_name = self.epoch.perform_epoch(generation_number,self.population,self.energyprofile,population_reset_settings,epoch_due_to_population_energy_convergence=epoch_due_to_population_energy_convergence)
	self.ga_recording_system.add_collection(self.population, []) # save this new reset population

import time, sys
# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 50 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), round(progress*100.0,1), status)
    sys.stderr.write(text)
    sys.stderr.flush()

def convert_seconds_to_normal_time(seconds):
    mins, secs = divmod(seconds, 60)
    return str(mins)+' mins and '+str(secs)+' secs'

def check_files_for_readable_and_writable():
	not_readable_and_writable_files = []
	not_readable_and_writable_folders = []
	root_path = os.path.dirname(__file__)
	files_to_check = ['epoch_data','GA_Run_Details.txt']
	folders_to_check = ['Population','Recorded_Data']
	# check root GA files
	for name in files_to_check:
		path_to_file = name #os.path.relpath(os.path.join('.', name))
		if not os.access(path_to_file,0o777):
			not_readable_and_writable_files.append(path_to_file)
	# check root GA folders
	for folder_to_check in folders_to_check:
		for root, dirs, files in os.walk(folder_to_check, topdown=False):
			for name in files:
				path_to_file = os.path.relpath(os.path.join(root, name))
				if not os.access(path_to_file,0o777):
					not_readable_and_writable_files.append(path_to_file)
			for name in dirs:
				path_to_folder = os.path.relpath(os.path.join(root, name))
				if not os.access(path_to_folder,0o777):
					not_readable_and_writable_folders.append(path_to_folder)
	# turning folders to chmod 777
	if not len(not_readable_and_writable_files) == 0 or len(not_readable_and_writable_folders) == 0:
		try:
			for path_to_file in not_readable_and_writable_files:
				os.access(path_to_file,0o777)
			for path_to_folder in not_readable_and_writable_folders:
				os.access(path_to_folder,0o777)
		except:
			print('--------------------------------------------------------------------------------------')
			print('Error in your genetic algorithm program')
			print('Some of your files and folders are not both readable and writable.')
			print('All of your files in your genetic algorithm need to be readable and writable by anyone')
			print('files and folders that you need to check')
			print('-----------------')
			print('Files')
			for path_to_file in not_readable_and_writable_files:
				print('\t'+str(path_to_file))
			print('-----------------')
			print('Folders')
			for path_to_folder in not_readable_and_writable_folders:
				print('\t'+str(path_to_folder))
			print('-----------------')
			print("You can attempt to change the permissions of these files by performing the following in this genetic algorithm run's folder in the terminal:")
			print('\tchmod -R 777 *')
			print('If this does not work, this likely means that this genetic algorithm was run last by someone else.')
			print('Check this out and talk to the person who last ran this genetic algorithm run.')
			exit('This program will finish without completing.')


