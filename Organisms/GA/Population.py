import os, sys
from shutil import copyfile
from io import StringIO
from copy import deepcopy
import multiprocessing as mp

from Organisms.GA.Collection import Collection

class Population(Collection):
	"""
	This class stores all the clusters that are in the population.

	:param name: Name of the Collection. This can be any name you like, it is just to note what the collection is. All collections should have a unique name if possible to prevent confusion, however this will not break the program.
	:type  name: str.
	:param size: This is the number of clusters that should be in the collection. In this version of the Organisms program, the number of clusters in the population and made during Creation of Offspring should be consistant throughout the genetic algorithm process.
	:type  size: int
	:param user_initialised_population_folder: Indicates the directory to obtain clusters to place in the initial population. If None, there are no user created clusters to obtained. Default: None.
	:type  user_initialised_population_folder: str. 
	:param write_data: Write the clusters to disk in a database. Default: True.
	:type  write_data: bool.

	"""
	def __init__(self,name,size,user_initialised_population_folder=None,write_data=True):
		self.write_data = write_data
		have_database = write_collection_history = self.write_data
		super().__init__(name,size,have_database=have_database,path=None,write_collection_history=write_collection_history)
		self.user_initialised_population_folder = user_initialised_population_folder
		#############################
		# set up current_gen_details
		if self.write_data:
			self.current_population_details = 'current_population_details.txt'
			self.current_population_details_path = self.path+'/'+self.current_population_details

	def get_pool_folder_size(self,folder_to_look_at=False):
		"""
		This definition will count the number of clusters in the population that the user places into the
		GA before it runs. It does this by counting the number of numbered folders (these in this program
		hold information about each cluster created during a GA Run).
		This method is only needed before the GA begins.

		Inputs:
			folder_to_look_at (False/None/str.): Indicate the number of clusters in the population as stored on the disk.
		
		returns: len(clusters_in_population): The size of the population, measured by counting the number of folders named by a number (which this program will interpret as a cluster in the population).
		rtypes: int

		"""
		# obtain the folders that are named by a integer number. A numbered cluster indicates a cluster in the
		# population or if the offspring.
		if folder_to_look_at == False:
			folder_to_look_at = self.name
		clusters_in_population = []
		if folder_to_look_at == None or (not (os.path.exists(folder_to_look_at) and os.path.isdir(folder_to_look_at))):
			return 0
		for cluster in os.listdir(folder_to_look_at):
			if (os.path.isdir(os.path.join(folder_to_look_at, cluster)) and cluster.isdigit()): # If the cluster folder exists and the folder is numbered properl, then it is a cluster to be added into the GA program
				clusters_in_population.append(int(cluster))
		clusters_in_population.sort()
		# We will make sure that the clusters read from the cluster folders in the run folder are sequently
		# numbered, otherwise the user has done something wrong.
		noCluInPool = 1
		for cluster_name in clusters_in_population:
			if not noCluInPool == cluster_name:
				exit("Error: The clusters in the population are not sequently numbered. Please renumber your original clusters so they are in sequential order.")
			noCluInPool += 1
		# if there were no faults (i.e. the folders are sequently numbered), return the number.
		return len(clusters_in_population)

	##########################################################################
	############################# BACKUP METHODS #############################
	##########################################################################

	def backup_files(self):
		"""
		Backup the database and the current state file
		"""
		self.backup_database()
		self.backup_state_file()

	def remove_backup_files(self):
		"""
		Remove the backup the database and the current state file
		"""
		self.remove_backup_database()
		self.remove_backup_state_file()

	##########################################################################
	####################### current_state_file METHODS #######################
	##########################################################################

	def current_state_file(self,generation_number):
		"""
		Write the current state file for the population for this generation.

		:param generation_number: The curent generation.
		:type  generation_number: int

		"""
		if not self.have_database:
			return
		with open(self.path+'/'+self.current_population_details,'w') as Current_Population_details_TXT:
			Current_Population_details_TXT.write("GA Iteration: " + str(generation_number) + "\n")
			Current_Population_details_TXT.write("Clusters in Pool:\t")
			for cluster in self:
				Current_Population_details_TXT.write(str(cluster.name)+"\t")
			Current_Population_details_TXT.write("\n")
			Current_Population_details_TXT.write("Energies of Clusters:\t")
			for cluster in self:
				Current_Population_details_TXT.write(str(cluster.energy) + "\t")
			Current_Population_details_TXT.write("\n")

	def get_data_from_current_state_file(self,current_state_file):
		"""
		Get data about the current population from the state file on disk.

		:param current_state_file: The path to the curent state file.
		:type  current_state_file: str.

		:returns the generation the state file was made, a list of the names of the clusters in the population, and a list of the energies of the clusters in the population.
		:rtype   float, list of int, and list of float
		"""
		with open(current_state_file,'r') as current_state_fileTXT:
			generation_data = current_state_fileTXT.readline()
			generation = int(generation_data.rstrip().split(':')[1])
			cluster_names_data = current_state_fileTXT.readline()
			cluster_names = [int(name) for name in cluster_names_data.rstrip().split(':')[1].split()]
			cluster_energies_data = current_state_fileTXT.readline()
			cluster_energies = [float(energy) for energy in cluster_energies_data.rstrip().split(':')[1].split()]
		return generation, cluster_names, cluster_energies

	def is_data_in_current_state_file(self,current_state_file):
		try:
			self.get_data_from_current_state_file(current_state_file)
			return True
		except Exception as exception:
			print('------------------------------------------------------------------------')
			print('Could not get all the required data from the population state file (from '+str(current_state_file)+').')
			print('The following message is the exception message.')
			print()
			print(exception)
			print()
			print('The GA have some tricks up its sleeve to repair this issue.')
			print('------------------------------------------------------------------------')
			return False

	def backup_state_file(self):
		"""
		This method will make a backup of all the clusters in the Collection as a ASE database
		"""
		if self.have_database:
			copyfile(self.path+'/'+self.current_population_details, self.path+'/'+self.current_population_details+'.backup')
			os.remove(self.path+'/'+self.current_population_details)

	def remove_backup_state_file(self):
		"""
		This method will remove the backup of all the clusters in the Collection, which will be in the format of a ASE database.
		"""
		if self.have_database:
			os.remove(self.path+'/'+self.current_population_details+'.backup')

	def remove_backup_state_file_if_exists(self):
		"""
		This method will remove the backup of all the clusters in the Collection, which will be in the format of a ASE database.
		"""
		if self.have_database:
			if os.path.exists(self.path+'/'+self.current_population_details+'.backup'):
				os.remove(self.path+'/'+self.current_population_details+'.backup')

	def move_backup_to_current_files(self):
		"""
		This method reove the last state file if one exists, and replace it with the backup.
		"""
		if not self.have_database:
			return
		if os.path.exists(self.path+'/'+self.current_population_details):
			os.remove(self.path+'/'+self.current_population_details)
		copyfile(self.path+'/'+self.current_population_details+'.backup', self.path+'/'+self.current_population_details)
		os.remove(self.path+'/'+self.current_population_details+'.backup')

	def repair_current_state_file(self,generation_number,cluster_names,cluster_energies):
		"""
		Write the current state file for the population for this generation. 
		This method is used if the state file or a back up could not be found or were incomplete.
		This method will get the data from the information from the energyprofile.txt file

		:param generation_number: The current generation.
		:type  generation_number: int
		:param cluster_names: The names of the clusters in the population.
		:type  cluster_names: list of ints.
		:param cluster_energies: The energies of the clusters in the population.
		:type  cluster_energies: list of floats

		"""
		if not self.have_database:
			return
		path_to_current_population_details = self.path+'/'+self.current_population_details
		if os.path.exists(path_to_current_population_details):
			copyfile(path_to_current_population_details,path_to_current_population_details+'.original_before_restart.txt')
			os.remove(path_to_current_population_details)
		with open(path_to_current_population_details,'w') as Current_Population_details_TXT:
			Current_Population_details_TXT.write("GA Iteration: " + str(generation_number) + "\n")
			Current_Population_details_TXT.write("Clusters in Pool:\t")
			for cluster_name in cluster_names:
				Current_Population_details_TXT.write(str(cluster_name)+"\t")
			Current_Population_details_TXT.write("\n")
			Current_Population_details_TXT.write("Energies of Clusters:\t")
			for cluster_energy in cluster_energies:
				Current_Population_details_TXT.write(str(cluster_energy) + "\t")
			Current_Population_details_TXT.write("\n")

	def get_current_generation_from_state_file(self):
		"""
		This method is used to get the current generation from the Organisms program if it had already run previously.
		This method is used at the beginnning of the Organisms program to get the current generation if the Organisms program has been
		restarted.

		Returns:
			The current generation of the Organisms program if it has already run previously and is being restarted.
			The names of the clusters in the population at that generation.
		"""
		# looking into the state file for information. 
		if os.path.exists(self.current_population_details_path+'.backup') and self.is_data_in_current_state_file(self.current_population_details_path+'.backup'):
			current_generation, cluster_names, cluster_energies = self.get_data_from_current_state_file(self.current_population_details_path+'.backup')
			return current_generation, cluster_names, cluster_energies, True
		if os.path.exists(self.current_population_details_path)           and self.is_data_in_current_state_file(self.current_population_details_path):
			current_generation, cluster_names, cluster_energies = self.get_data_from_current_state_file(self.current_population_details_path)
			return current_generation, cluster_names, cluster_energies, False
		
		# Could not find the state file or the backup state file. Will attempt to get the relavant data from the history file. 
		if self.write_collection_history:
			self.open('r')
			cluster_energies = []; cluster_names = []; current_generation = None
			# get in PoolProfile.txt the last generation that successfully ran
			for line in reversed(self.history_file.readlines()):
				# get the energies of the clusters of last generation.
				if 'Energies of Clusters:' in line:
					try:
						cluster_energies = line.split()[3:]
						cluster_energies = [float(x) for x in cluster_energies]
					except:
						cluster_energies = None
				# get the dirs of the clusters of last generation.
				elif 'Clusters in Pool:' in line:
					try:
						cluster_names = line.split()[3:]
						cluster_names = [int(x.split('(')[0]) for x in cluster_names]
					except:
						cluster_names = None
				# get the last generation that was successfully completed before the genetic algorithm fail.
				elif 'GA Iteration:' in line:
					try:
						current_generation = line.replace('GA Iteration: ','')
						current_generation = int(current_generation.replace('\n',''))
					except:
						current_generation = None
					if (not cluster_energies == None and not cluster_names == None and not current_generation == None) and (len(cluster_names) == self.size and len(cluster_energies) == self.size):
						break
			self.close()
			#clusters = [(cluster_name, cluster_energy) for cluster_name, cluster_energy in zip(cluster_names,cluster_energies)]
			if current_generation == None:
				self.delete_collection_database()
			self.repair_current_state_file(current_generation, cluster_names, cluster_energies)
			return current_generation, cluster_names, cluster_energies, None
		print('------------------------------------')
		print('ERROR: You do not have any of the following files, or some of the following files are not complete: ')
		print('--> '+self.current_population_details_path+'.backup')
		print('--> '+self.current_population_details_path)
		print('--> '+self.history_path)
		print('Without any of these files, the genetic algorithm can not verify the current generation')
		print()
		print('--> If you have the information, you could consider making a '+str(self.current_population_details_path)+' file yourself in the format')
		print()
		print('GA Iteration: XXX')
		print('Clusters in Pool: XXX XXX XXX ...')
		print('Energies of Clusters: XXX.XX XXX.XX XXX.XX ...')
		print()
		print('Where the "GA Iteration" is the generation that the GA is up to, "Clusters in Pool" are the names of the clusters in the population, and "Energies of Clusters" are the energies of those cluster in the correct units.')
		print()
		print('Check this out')
		exit('This program will exit without completing')

	# ----------------------------------------------------------------------------------------------------------------------------------------------------------
	# Debugging printing information

	def get_details(self):
		"""
		Debugging tool for the Population Class.

		This definition is designed to print all the details about the population.

		"""
		details = [['population_name',self.name],['size',self.size],['Size of Clusters_In_Pop',self.size]]
		print('-----------------------------------------')
		print('Debugging details of the population: '+str(self.name))
		for dd in details:
			print(dd[0]+' = '+str(dd[1]))
		print('-----------------------------------------')

	def print_clusters(self):
		"""
		Debugging tool for the Population Class.

		This definition is designed to print all the details about the clusters in the population.
		
		"""
		print('-----------------------------------------')
		print('Clusters in this population: '+str(self.name))
		highest_energy = -float('inf')
		lowest_energy = float('inf')
		index_highest_energy = -1.1
		index_lowest_energy = -1.1
		print('Sorted by position in the population')
		for index in range(len(self)):
			if 'fitness' in self[index].__dict__.keys():
				print('pop index: ' + str(index) + '; cluster name: ' + str(self[index].name) + '; cluster energy: ' + str(self[index].energy) + ' eV; cluster fitness: ' + str(self[index].fitness) + '')
			else:
				print('pop index: ' + str(index) + '; cluster name: ' + str(self[index].name) + '; cluster energy: ' + str(self[index].energy) + ' eV')
			if self[index].energy > highest_energy:
				highest_energy = self[index].energy
				index_highest_energy = index
			if self[index].energy < lowest_energy:
				lowest_energy = self[index].energy
				index_lowest_energy = index
		print('Sorted by Energy (from lowest to highest energy).')
		indices_of_pop = range(len(self))
		indices_of_pop_sorted = []; sorted_pop_by_energy = [];
		for x,y in sorted(zip(self,indices_of_pop), key = lambda x: x[0].energy, reverse=False):
			sorted_pop_by_energy .append(x)
			indices_of_pop_sorted.append(y)
		for index in range(len(sorted_pop_by_energy)):
			if 'fitness' in sorted_pop_by_energy[index].__dict__.keys():
				print('pop index: ' + str(indices_of_pop_sorted[index]) + '; cluster name: ' + str(sorted_pop_by_energy[index].name) + '; cluster energy: ' + str(sorted_pop_by_energy[index].energy) + ' eV; cluster fitness: ' + str(sorted_pop_by_energy[index].fitness) + '')
			else:
				print('pop index: ' + str(indices_of_pop_sorted[index]) + '; cluster name: ' + str(sorted_pop_by_energy[index].name) + '; cluster energy: ' + str(sorted_pop_by_energy[index].energy) + ' eV')
		print('-----------------------------------------')
