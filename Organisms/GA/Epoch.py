import os 
from shutil import copyfile

from Organisms.GA.Initialise_Population import Initialise_Population
from Organisms.GA.Get_Predation_and_Fitness_Operators import get_fitness_operator

class Epoch:
	"""
	This class is responsible for the epoch method used during the genetic algorithm run

	:param epoch_settings: This is a dictionary of all the epoch settings.
	:type  epoch_settings: dict.
	:param path: This is the path to store the epoch information in after each generation has completed. This information allows the genetic algorithm run to continue with information of the epoch from the last completed generation. 
	:type  path: str.

	"""
	def __init__(self,epoch_settings,path,fitness_operator,population):
		self.path = path
		self.epoch_data_name = 'epoch_data'
		self.backup_epoch_data_name = self.epoch_data_name+'.backup'
		self.epoch_settings = epoch_settings
		self.set_settings(self.epoch_settings,fitness_operator,population)

	def __repr__(self):
		return str(self.__dict__)

	def set_settings(self,epoch_settings,fitness_operator,population):
		"""
		This sets up the epoch as desired. 

		:param epoch_settings: This is a dictionary of all the epoch settings.
		:type  epoch_settings: dict.

		"""
		if epoch_settings == None:
			epoch_settings = {'epoch mode': None}
		self.epoch_mode = epoch_settings['epoch mode']
		# If there is no epoch
		if self.epoch_mode in ['Off', 'off', 'None', 'none', None, False]:
			self.epoch_function = self.no_epoch
			self.perform_epoch_function = self.perform_epoch_no_epoch
			return
		elif self.epoch_mode in ['mean energy']:
			self.energy_difference = epoch_settings['mean energy difference']
			self.epoch_function = self.should_epoch_using_mean_energy_epoch
			self.perform_epoch_function = self.perform_epoch_mean_energy
		elif self.epoch_mode in ['same population']:
			self.max_number_of_times_non_changing_population = epoch_settings['max repeat']
			self.epoch_function = self.should_epoch_using_same_population_epoch
			self.perform_epoch_function = self.perform_epoch_same_population
		else:
			print('Issue with the Epoch method, def set_settings in Epoch.py')
			print('You must set the epoch method to one of the following:')
			print('  --> Off: No epoch method')
			print('  --> mean energy: epoch method based on the mean energy of the population')
			print('  --> same population: epoch method based on repeated clusters in the population')
			print('See the manual for more details.')
			exit('This program will exit without finishing')
		# if epoching first by changing fitness function to energy fitness function
		first_epoch_to_change_fitness_function_name = 'first epoch changes fitness operator to energy fitness operator'
		if first_epoch_to_change_fitness_function_name in epoch_settings:
			self.first_epoch_to_change_fitness_function = epoch_settings[first_epoch_to_change_fitness_function_name]
			if self.first_epoch_to_change_fitness_function:
				if fitness_operator.fitness_switch == 'Energy':
					print('Error with the Epoch method setting: '+str(first_epoch_to_change_fitness_function_name))
					print('You have chosen that the first time a population epochs that it changes the fitness function to the Energy fitness function')
					print('But you are already using the Energy fitness function.')
					print('This will be ineffective and could cause issues. Therefore we are stopping the program here so you can sort this out')
					print(first_epoch_to_change_fitness_function_name+': '+str(self.first_epoch_to_change_fitness_function))
					print('fitness_operator.fitness_switch: '+str(fitness_operator.fitness_switch))
					exit('This program will finish without completing.')
				elif fitness_operator.fitness_switch == 'SCM + Energy' and float(fitness_operator.SCM_fitness_contribution) == 0.0: 
					print('Error with the Epoch method setting: '+str(first_epoch_to_change_fitness_function_name))
					print('You have chosen that the first time a population epochs that it changes the fitness function to the Energy fitness function')
					print('But you are using the SCM + Energy fitness function with SCM_fitness_contribution = 0.0')
					print('This is equivalent to the Energy fitness function.')
					print('This will be ineffective and could cause issues. Therefore we are stopping the program here so you can sort this out')
					print(first_epoch_to_change_fitness_function_name+': '+str(self.first_epoch_to_change_fitness_function))
					print('fitness_operator.fitness_switch: '+str(fitness_operator.fitness_switch))
					exit('This program will finish without completing.')
				self.perform_reset_population = True
				#if fitness_operator.fitness_switch == 'Energy':
				#	self.fitness_information_temp = {'Fitness Operator': 'Energy', 'fitness_function': fitness_operator.fitness_information['fitness_function']}
				if fitness_operator.fitness_switch == 'SCM + Energy':
					self.fitness_information_temp = {'Fitness Operator': 'Energy', 'fitness_function': epoch_settings['energy_fitness_function']} #'fitness_function': fitness_operator.fitness_information['energy_fitness_function']}
				else:
					exit('fitness_operator switch error')
				predation_information = {'Predation Operator': 'Off'}
				self.fitness_operator_temp = get_fitness_operator(self.fitness_information_temp, None, population, None, 1, False)
		else:
			self.first_epoch_to_change_fitness_function = False

	# --------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------
	# Get data for new genetic algorithm trial

	def setting_up_for_new_GA(self):
		if self.epoch_mode in ['mean energy']:
			self.initialise_mean_energy_epoch_details()
		# import data if same population epoch method was used
		elif self.epoch_mode in ['same population']:
			self.initialise_same_population_epoch_details()
		else:
			print('Error in Epoch')
			print('You have not chosen an available epoch method')
			print('epoch parameter "epoch mode" should be either: "None", "mean energy", or "same population"')
			print("Your Epoch's 'epoch mode': "+str(self.epoch_mode))
			print('Check this')
			exit('This program will exit without completing')
		del self.epoch_settings

	def initialise_mean_energy_epoch_details(self):
		"""
		This contains the information required to set up the mean_energy epoch method. 

		:param epoch_settings: This is a dictionary of all the epoch settings.
		:type  epoch_settings: dict.

		"""
		self.initial_generation = 0
		self.previous_mean_energy = float('inf')

	def initialise_same_population_epoch_details(self):
		"""
		This contains the information required to set up the same_population epoch method. 

		:param epoch_settings: This is a dictionary of all the epoch settings.
		:type  epoch_settings: dict.

		"""
		self.initial_generation = 0
		self.clusters_in_previous_population = None
		self.number_of_times_non_changing_population = 0

	# --------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------
	# Get data for resumed genetic algorithm trial

	def setting_up_epoch_to_resume_GA(self):
		"""
		This method will load the data from the epoch data on disk in order to resume.
		"""
		# check whether to use information from the epoch data on disk or from the backup epoch data.
		# If an epoch method was used, make sure that data is obtained from the backup file before obtaining data from the original file. 
		if self.does_backup_exist()               and self.is_epoch_data_of_disk_complete(self.backup_epoch_data_name,self.epoch_settings):
			get_epoch_data_from = self.backup_epoch_data_name
			self.got_data_from_backup = True
		elif self.does_epoch_data_exist_on_disk() and self.is_epoch_data_of_disk_complete(self.epoch_data_name,self.epoch_settings):
			get_epoch_data_from = self.epoch_data_name
			self.got_data_from_backup = False
		else:
			print('Error with the Epoch data on disk')
			print('The epoch data and the backup file of this are either not there, or is incomplete.')
			print('Make sure that at least one of the epoch data or its backup exist and is complete for the epoch method that you are using')
			print('See the manual for information on the information that is required for the epoch data to be complete.')
			exit('This method will finish without having begun.')
		'''
		# If an epoch method was used, make sure that data is obtained from the backup file before obtaining data from the original file. 
		if self.does_backup_exist():
			get_epoch_data_from = self.backup_epoch_data_name
			self.got_data_from_backup = True
		else:
			get_epoch_data_from = self.epoch_data_name
			self.got_data_from_backup = False
		'''
		# import data if mean energy epoch method was used
		if self.epoch_mode in ['mean energy']:
			self.get_resumed_mean_energy_epoch_details(self.epoch_settings,get_epoch_data_from)
		# import data if same population epoch method was used
		elif self.epoch_mode in ['same population']:
			self.get_resumed_same_population_epoch_details(self.epoch_settings,get_epoch_data_from)
		else:
			print('Error in Epoch')
			print('You have not chosen an available epoch method')
			print('epoch parameter "epoch mode" should be either: "None", "mean energy", or "same population"')
			print("Your Epoch's 'epoch mode': "+str(self.epoch_mode))
			print('Check this')
			exit('This program will exit without completing')
		# make backups
		if self.did_get_data_from_backup():
			self.replace_with_backup()
		del self.epoch_settings

	def get_resumed_mean_energy_epoch_details(self,epoch_settings,get_epoch_data_from):
		"""
		This contains the information required to set up the mean_energy epoch method. 

		:param epoch_settings: This is a dictionary of all the epoch settings.
		:type  epoch_settings: dict.
		:param get_epoch_data_from: The path of the epoch document to get information from if the genetic algorithm is being resumed.
		:type  get_epoch_data_from: str.

		"""
		#self.energy_difference = epoch_settings['mean energy difference']
		#if os.path.exists(get_epoch_data_from):
		with open(get_epoch_data_from,'r') as epoch_data:
			self.initial_generation = eval(epoch_data.readline())
			self.previous_mean_energy = eval(epoch_data.readline())
		#else:
		#	self.initial_generation = 0
		#	self.previous_mean_energy = float('inf')
		#self.epoch_function = self.should_epoch_using_mean_energy_epoch
		#self.perform_epoch_function = self.perform_epoch_mean_energy

	def get_resumed_same_population_epoch_details(self,epoch_settings,get_epoch_data_from):
		"""
		This contains the information required to set up the same_population epoch method. 

		:param epoch_settings: This is a dictionary of all the epoch settings.
		:type  epoch_settings: dict.
		:param get_epoch_data_from: The path of the epoch document to get information from if the genetic algorithm is being resumed.
		:type  get_epoch_data_from: str.

		"""
		#if os.path.exists(get_epoch_data_from):
		with open(get_epoch_data_from,'r') as epoch_data:
			self.initial_generation = eval(epoch_data.readline())
			self.clusters_in_previous_population = eval(epoch_data.readline())
			self.number_of_times_non_changing_population = eval(epoch_data.readline())
		#else:
		#	self.initial_generation = 0
		#	self.clusters_in_previous_population = None
		#	self.number_of_times_non_changing_population = 0
		#self.max_number_of_times_non_changing_population = epoch_settings['max repeat']
		#self.epoch_function = self.should_epoch_using_same_population_epoch
		#self.perform_epoch_function = self.perform_epoch_same_population

	def is_epoch_data_of_disk_complete(self,get_epoch_data_from,epoch_settings):
		# import data if mean energy epoch method was used
		try:
			if self.epoch_mode in ['mean energy']:
				self.get_resumed_mean_energy_epoch_details(epoch_settings,get_epoch_data_from)
			# import data if same population epoch method was used
			elif self.epoch_mode in ['same population']:
				self.get_resumed_same_population_epoch_details(epoch_settings,get_epoch_data_from)
			# If you get to this point, the right epoch method contains the information required, so return True
			return True
		except:
			# Some information is missing from the epoch_data file, so return False
			return False
	# --------------------------------------------------------------------------------------------------------
	# --------------------------------------------------------------------------------------------------------
	# Should en epoch occur methods

	def should_epoch(self,collection,generation_number):
		"""
		Determines if the genetic algorithm should epoch.

		:param collection: This is the collection to use to determine if the genetic algorithm should epoch. This Collection should be the Population.
		:type  collection: Organisms.GA.Collection
		:param generation_number: The number of the last successful generation
		:type  generation_number: int

		returns Should an epoch occur. True if yes, False if no.
		rtype   bool.

		"""
		return self.epoch_function(collection, generation_number)

	def no_epoch(self,collection,generation_number):
		"""
		The proceedure to determine if an epoch should occur.

		Since no epoch is included in this algorithm, return False to mean do not perform an epoch

		:param collection: This is the collection to use to determine if the genetic algorithm should epoch. This Collection should be the Population.
		:type  collection: Organisms.GA.Collection
		:param generation_number: The number of the last successful generation
		:type  generation_number: int

		returns Should an epoch occur. False for no, since this genetic algorithm has not been told to epoch.
		rtype   bool.
		"""
		return False

	def should_epoch_using_mean_energy_epoch(self,collection,generation_number):
		"""
		The proceedure to determine if an epoch should occur, using the mean_energy epoch method.

		:param collection: This is the collection to use to determine if the genetic algorithm should epoch. This Collection should be the Population.
		:type  collection: Organisms.GA.Collection
		:param generation_number: The number of the last successful generation
		:type  generation_number: int

		returns Should an epoch occur. True if yes, False if no.
		rtype   bool.
		"""
		mean_energy = collection.mean_energy()
		with open(self.epoch_data_name,'w') as epoch_data:
			epoch_data.write(str(generation_number)+'\n')
			epoch_data.write(str(mean_energy))
		if (self.previous_mean_energy - mean_energy) > self.energy_difference:
			self.previous_mean_energy = mean_energy
			return False
		else:
			self.previous_mean_energy = float('inf')
			return True

	def should_epoch_using_same_population_epoch(self,collection,generation_number):
		"""
		The proceedure to determine if an epoch should occur, using the same_population epoch method.

		Since no epoch is included in this algorithm, return False to mean do not perform an epoch

		:param collection: This is the collection to use to determine if the genetic algorithm should epoch. This Collection should be the Population.
		:type  collection: Organisms.GA.Collection
		:param generation_number: The number of the last successful generation
		:type  generation_number: int

		returns Should an epoch occur. True if yes, False if no.
		rtype   bool.
		"""
		clusters_in_population = collection.get_cluster_names()
		#print(clusters_in_population)
		if not clusters_in_population == self.clusters_in_previous_population:
			self.clusters_in_previous_population = list(clusters_in_population)
			self.number_of_times_non_changing_population = 0
		else:
			self.number_of_times_non_changing_population += 1
			if self.number_of_times_non_changing_population >= self.max_number_of_times_non_changing_population:
				return True
		with open(self.epoch_data_name,'w') as epoch_data:
			epoch_data.write(str(generation_number)+'\n')
			epoch_data.write(str(self.clusters_in_previous_population)+'\n')
			epoch_data.write(str(self.number_of_times_non_changing_population))
		return False

	# ----------------------------------------------------------------------
	# If to change the fitness function if to energy fitness function if first time the epoch was reached

	def change_fitness_function(self,fitness_operator):
		"""

		"""
		fitness_operator, self.fitness_operator_temp = self.fitness_operator_temp, fitness_operator
		self.perform_reset_population = not self.perform_reset_population
		return self.perform_reset_population, fitness_operator

	# ----------------------------------------------------------------------
	# Perform epoch by resetting the population

	def perform_epoch(self,generation_number,population,energyprofile,population_reset_settings,epoch_due_to_population_energy_convergence):
		"""
		Perform an epoch by resetting all the clusters in the population.

		:param generation_number: The number of the last successful generation
		:type  generation_number: int
		:param population: The number of the last successful generation
		:type  population: Organisms.GA.Population
		:param energyprofile: The energyprofile to write epoch information to.
		:type  energyprofile: Organisms.GA.EnergyProfile
		:param population_reset_settings: This is a dict that contains all the information requied to epoch the population with a set of randomly generated clusters. 
		:type  population_reset_settings: dict.
		:param epoch_due_to_population_energy_convergence: Did the Epoch occur because the population converged? True if yes, False if no. 
		:type  epoch_due_to_population_energy_convergence: bool.

		returns The name of the more recently generated cluster before the epoch method was performed.
		rtype   bool.
		"""
		cluster_makeup, surface, Minimisation_Function, memory_operator, predation_operator, fitness_operator, epoch_method, cell_length, vacuum_to_add_length, r_ij, rounding_criteria, no_of_cpus, previous_cluster_name = population_reset_settings	
		# ---------------------------------------------------------------------------------------- #
		# reset the predation and fitness operators
		fitness_operator.reset()
		predation_operator.reset()
		if epoch_due_to_population_energy_convergence:
			print('------------------------------------------------------------------------------------------')
			print('The clusters in the population all have the same energy, will need to reset the population')
			print('------------------------------------------------------------------------------------------')
			energyprofile.add_epoch_note_due_to_population_energy_convergence()
		else:
			energyprofile.add_epoch_note()
		# ---------------------------------------------------------------------------------------- #
		# reset the population
		for index in range(len(population)-1,-1,-1):
			population.remove(index)
		previous_cluster_name = Initialise_Population(population,cluster_makeup,surface,Minimisation_Function,memory_operator,predation_operator,fitness_operator,epoch_method,cell_length,vacuum_to_add_length,r_ij,rounding_criteria,no_of_cpus,previous_cluster_name=previous_cluster_name,generation=generation_number,get_already_created_clusters=False,is_epoch=True,epoch_due_to_population_energy_convergence=epoch_due_to_population_energy_convergence)
		# ---------------------------------------------------------------------------------------- #
		# reset the epoch_data file
		self.clusters_in_previous_population = population.get_cluster_names()
		self.number_of_times_non_changing_population = 0
		self.perform_epoch_function(generation_number)
		# ---------------------------------------------------------------------------------------- #
		energyprofile.add_collection(population,generation_number)
		return previous_cluster_name

	def perform_epoch_no_epoch(self,generation_number):
		"""
		This method is needed, but does not do anything.

		:param generation_number: The number of the last successful generation
		:type  generation_number: int
		"""
		return

	def perform_epoch_mean_energy(self, generation_number):
		"""
		This method writes the current epoch data to file for the mean_energy epoch method. 

		:param generation_number: The number of the last successful generation
		:type  generation_number: int
		"""
		mean_energy = collection.mean_energy()
		with open(self.epoch_data_name,'w') as epoch_data:
			epoch_data.write(str(generation_number)+'\n')
			epoch_data.write(str(mean_energy))

	def perform_epoch_same_population(self, generation_number):
		"""
		This method writes the current epoch data to file for the same_population epoch method. 

		:param generation_number: The number of the last successful generation
		:type  generation_number: int
		"""
		with open(self.epoch_data_name,'w') as epoch_data:
			epoch_data.write(str(generation_number)+'\n')
			epoch_data.write(str(self.clusters_in_previous_population)+'\n')
			epoch_data.write(str(self.number_of_times_non_changing_population))

	def does_epoch_data_exist_on_disk(self):
		"""
		Determine if a backup of the epoch information stored on disk exists.

		returns If a backup of the epoch information stored on disk exists. True for yes, False for no.
		rtype   bool.
		"""
		if self.epoch_mode == None:
			return
		return os.path.exists(self.path+'/'+self.epoch_data_name)

	# ----------------------------------------------------------------------
	# Epoch backup data

	def information_from_the_same_generation(self, generation_number):
		"""
		Determine if the epoch file contains the relavant information for the generation to resume from.

		:param generation_number: The number of the last successful generation
		:type  generation_number: int

		returns If the epoch information from the epoch file is for the current generation. True if yes, False if no. This value is True if no epoch method is used, as we dont need to deal with any epoch information if no epoch is used. 
		rtype   bool.
		"""
		if self.epoch_mode == None:
			return True
		return self.initial_generation == generation_number

	def did_get_data_from_backup(self):
		"""
		Determine if the data was obtained from backup epoch file or not. True for yes, False for no. If no epoch method was used, return False, since we dont need to deal with previous epoch information if no epoch method was used. 
	
		returns Did the epoch information come from the backup epoch file or not. True for yes, False for no. If no epoch method was used, return False, since we dont need to deal with previous epoch information if no epoch method was used.  
		rtype   bool.
		"""
		if self.epoch_mode == None:
			return False
		return self.got_data_from_backup

	def backup(self):
		"""
		Make a backup of the epoch data stored on disk
		"""
		if self.epoch_mode == None:
			return
		copyfile(self.path+'/'+self.epoch_data_name, self.path+'/'+self.backup_epoch_data_name)

	def remove_backup(self):
		"""
		Remove the backup of the epoch data stored on disk
		"""
		if self.epoch_mode == None:
			return
		os.remove(self.path+'/'+self.backup_epoch_data_name)

	def does_backup_exist(self):
		"""
		Determine if a backup of the epoch information stored on disk exists.

		returns If a backup of the epoch information stored on disk exists. True for yes, False for no.
		rtype   bool.
		"""
		if self.epoch_mode == None:
			return
		return os.path.exists(self.path+'/'+self.backup_epoch_data_name)

	def check_for_backup(self):
		"""
		Checks to see that a backup exists. If not, something has gone wrong and the algorithm needs to stop. 
		"""
		if self.epoch_mode == None:
			return
		if not os.path.exists(self.path+'/'+self.backup_epoch_data_name):
			print('Error in def replace_with_backup, in class Epoch, in Epoch.py')
			print('Could not find the epoch backup file. Called: '+str(self.backup_epoch_data_name))
			print('This should be found in '+str(self.path))
			print('Check this.')
			print('This program will finish without completing')
			exit()

	def replace_with_backup(self):
		"""
		Replace the current epoch data with the backup epoch data.
		"""
		if self.epoch_mode == None:
			return
		self.check_for_backup()
		os.remove(self.path+'/'+self.epoch_data_name)
		copyfile(self.path+'/'+self.backup_epoch_data_name,self.path+'/'+self.epoch_data_name)
		os.remove(self.path+'/'+self.backup_epoch_data_name)







