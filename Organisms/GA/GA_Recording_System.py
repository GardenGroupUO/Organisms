'''
Recording_Clusters.py, 02/10/2018, Geoffrey R Weal

'''
import sys
from math import pi
import numpy as np

from Organisms.GA.Collection import Collection
from Organisms.GA.GA_Program_external_methods import update_progress

class GA_Recording_Database(Collection):
	"""
	This is a Collection that has been designed to record clusters that have been created during the genetic algorithm.

	This has been designed to give the user many ways to limit the number of clusters that are recorded. This is to prevent the size of the database from getting to big in disk size.
	
	:param path_of_database: The path to this database
	:type  path_of_database: str.
	:param max_no_of_recorded_structures: This is the maximum number of clusters that will be recorded. If this limit is reached, the higher energy clusters will be replaced in new, lower energy clusters.
	:type  max_no_of_recorded_structures: int
	:param limit_datasize_of_database: This is the maximum size the database can get. Give as a string with size + memory type (e.g. 150MB, 2.0GB)
	:type  limit_datasize_of_database: str.
	:param ga_recording_scheme: The user can indicate a specific type of recording scheme to use to limit the clusters that are recorded. See manual for more details. Default: 'None'
	:type  ga_recording_scheme: str.
	:param limit_energy_height_of_clusters_recorded: If ga_recording_scheme == 'Limit_energy_height': is selected, this is the maximum energy above the LES energy. Any clusters that are lower in energy than Energy(LES) + limit_energy_height_of_clusters_recorded will be recorded. Any that have an energy higher than this will not be recorded. Default: float('inf')
	:type  limit_energy_height_of_clusters_recorded: float
	:param lower_energy_limit: If ga_recording_scheme == Set_energy_limits is selected, this is the low energy limit. Any cluster with an energy lower than lower_energy_limit will not be recorded. Default: -float('inf')
	:type  lower_energy_limit: float
	:param upper_energy_limit: If ga_recording_scheme == Set_energy_limits or ga_recording_scheme == 'Set_higher_limit', this is the upper energy limit. Any clusters with an energy higher than this energy limit will not be recorded. Default: float('inf')
	:type  upper_energy_limit: float

	"""
	def __init__(self,path_of_database,max_no_of_recorded_structures=None,limit_datasize_of_database=None,ga_recording_scheme='None',limit_energy_height_of_clusters_recorded=float('inf'),lower_energy_limit=-float('inf'),upper_energy_limit=float('inf'),show_GA_Recording_Database_check_percentage=False): 
		self.limit_datasize_of_database = limit_datasize_of_database
		self.ga_recording_scheme = ga_recording_scheme
		# Get the setting for any of the ga_recording_scheme
		if self.ga_recording_scheme == 'All':
			self.write_initial_cluster_in_RAM = False
			self.write_cluster_in_RAM = False
		elif self.ga_recording_scheme == 'Limit_energy_height':
			self.limit_energy_height_of_clusters_recorded = limit_energy_height_of_clusters_recorded
			self.write_initial_cluster_in_RAM = True
			self.write_cluster_in_RAM = True
		elif self.ga_recording_scheme == 'Set_higher_limit':
			self.upper_energy_limit = upper_energy_limit
			self.write_initial_cluster_in_RAM = False
			self.write_cluster_in_RAM = True
		elif self.ga_recording_scheme == 'Set_energy_limits':
			self.lower_energy_limit = lower_energy_limit
			self.upper_energy_limit = upper_energy_limit
			self.write_initial_cluster_in_RAM = False
			self.write_cluster_in_RAM = True
		elif self.ga_recording_scheme == 'None':
			exit('Error, should not create a GA_Recording_Database if self.ga_recording_scheme == None')
		# Get the settings for if self.size or self.limit_datasize_of_database is not equal to none
		if (max_no_of_recorded_structures == None) or (self.limit_datasize_of_database == None):
			self.write_initial_cluster_in_RAM = True
			self.write_cluster_in_RAM = True
		# Show the GA recording database check percentage
		self.show_GA_Recording_Database_check_percentage = show_GA_Recording_Database_check_percentage
		# Write the rest of the collection
		name = 'GA_Recording_Database'
		Collection.__init__(self,name,max_no_of_recorded_structures,have_database=True,path=path_of_database,write_collection_history=False,write_cluster_in_RAM=self.write_cluster_in_RAM)

	# ----------------------------------------------------------------------------------------------------------------------

	def get_cluster_names(self,order=False):
		"""
		Will provide a list of all the names of all the clusters in the Collection

		Inputs:
			order (bool.): This tag will tell this method whether the user would like the list of names given in order. 

		Returns:
			List of the names of all the clusters in the Population
		"""
		if self.write_cluster_in_RAM:
			cluster_names = [cluster[0] for cluster in self.clusters]
		else:
			import pdb; pdb.set_trace()
			exit('Cant do this')
		if order == True:
			cluster_names.sort()
		return cluster_names

	def sort_by_name(self):
		"""
		This method will sort the clusters in the list by their name.
		"""
		if self.write_cluster_in_RAM:
			self.clusters.sort(key=lambda cluster: cluster[0])
		else:
			import pdb; pdb.set_trace()
			exit('Cant do this')

	def sort_by_energy(self):
		"""
		This method will sort the clusters in the list by their energy (from lowest energy to highest energy).  
		"""
		if self.write_cluster_in_RAM:
			self.clusters.sort(key=lambda cluster: cluster[1])
		else:
			import pdb; pdb.set_trace()
			exit('Cant do this')

	def get_index(self,name_to_find):
		"""
		This method will provide the index of the cluster that has the name "name_to_find" in the Collection

		Inputs:
			name_to_find (int): the name of the cluster in the Collection to obtain the index for

		Returns:
			the index of the cluster in the Collection with the name "name_to_find"

		Exceptions:
			Will break if the cluster with the name "name_to_find" can not be found in this method.
		"""
		if self.write_cluster_in_RAM:
			for index in range(len(self.clusters)):
				if self.clusters[index][0] == name_to_find:
					return index
		else:
			print('Error in def get_index in class GA_Recording_System, in GA_Recording_System.py')
			print('You can use this method as the collection is not recording clusters in the RAM')
			print('Check your setting for write_cluster_in_RAM for '+str(self))
			exit('This program will exit without completing')
		print('Error in def get_index, in Class GA_Recording_Database, in GA_Recording_System.py')
		print('Error in def get_index in GA_Recording_System.py: Could not find the cluster that has the name = '+str(name_to_find))
		print('Check this.')
		exit('This program will exit without completing.')

	def add(self, index, cluster):
		"""
		Adds a cluster to the Collection.

		Index:
			index (int/str.): the index of the ith cluster in the Collection. If "End" is inputed, the cluster will be append to the end of the Collection list.
			cluster (Organisms.GA.Cluster): The cluster to add at the ith position in the Collection. 
		"""
		# Add the cluster to the Collection
		if self.write_cluster_in_RAM:	
			if index == 'End':
				self.clusters.append((cluster.name,cluster.energy))
			else:
				self.clusters.insert(index,(cluster.name,cluster.energy))
		else:
			self.no_of_clusters_counter += 1
		# adds the cluster in the collection to disk
		if self.have_database:
			self.add_to_database(cluster,center=True)

	def remove_to_database(self,cluster):
		"""
		Allows the user to remove a cluster in the collection from the  ASE database

		Inputs:
			cluster (Organisms.GA.Cluster): The cluster to remove from the database.
		"""
		with connect(self.database_path) as database:
			cluster_id_to_remove = database.get(name=cluster[0]).id
			del database[cluster_id_to_remove]

	def add_clusters_into_RAM(self, cluster_dict, cluster_names):
		"""
		This method adds clusters into the RAM

		:param cluster_dict: This is a dicionary of all the clusters from the database, given as {cluster_name: Cluster}
		:type  cluster_dict: {int: ASE.Cluster}
		:param cluster_names: list of the names of the clusters that are needed for the collection
		:type  cluster_names: list of int
		"""
		if self.write_cluster_in_RAM:	
			for cluster_name in cluster_names:
				cluster = cluster_dict[cluster_name]
				self.clusters.append((cluster.name,cluster.energy))

	# ----------------------------------------------------------------------------------------------------------------------
		
	def add_collection_to_database(self, collection, clusters_not_to_include):
		"""
		Will record the clusters in the collection to the GA_Recording_Database. 

		:param collection: The collection to be recorded
		:type  collection: Organisms.GA.Collection
		:param clusters_not_to_include: A list of names of clusters in the collection not to record in GA_Recording_Database.
		:type  clusters_not_to_include: list of int
		"""
		if self.ga_recording_scheme == 'None':
			return 
		# Add all clusters that you have in the collection to the GA recording database
		elif self.ga_recording_scheme == 'All':
			for cluster in collection:
				if not cluster.name in clusters_not_to_include:
					self.add(-1,cluster)
			#self.sort_by_energy()
		# Add all clusters that you have in the collection to the GA recording database
		elif self.ga_recording_scheme == 'Limit_energy_height': 
			for cluster in collection:
				if not cluster.name in clusters_not_to_include:
					self.add(-1,cluster)
			self.sort_by_energy()
			for index in range(len(self)-1,-1,-1): 
				if self[index][1] > (self[0][1] + self.limit_energy_height_of_clusters_recorded):
					del self[index]
				else:
					break
		# Add all clusters that you have in the collection to the GA recording database
		elif self.ga_recording_scheme == 'Set_higher_limit': 
			for cluster in collection:
				if (cluster.energy < self.upper_energy_limit) and (not cluster.name in clusters_not_to_include):
					self.add(-1,cluster)
		# Add all clusters that you have in the collection to the GA recording database
		elif self.ga_recording_scheme == 'Set_energy_limits': 
			for cluster in collection:
				if (self.lower_energy_limit < cluster.energy < self.upper_energy_limit) and (not cluster.name in clusters_not_to_include):
					self.add(-1,cluster)
		# get rid of all the highest energy clusters that can not fit into the database
		if (not self.size == None) and (len(self) > self.size):
			self.sort_by_energy()
			while len(self) > self.size: # of if size is greater than current size 
				del self[-1] 
		if (not self.limit_datasize_of_database == None) and (os.stat(self.database_path).st_size > self.limit_datasize_of_database):
			self.sort_by_energy()
			while os.stat(self.database_path).st_size > self.limit_datasize_of_database: # of if size is greater than current size
				del self[-1]
		#database.metadata = {'title': str(name_of_database), 'key_descriptions': {'systems': ('Cluster', 'The cluster', ''), 'gen_made': ('Generation Created', 'The generation tthe cluster was created.', ''), 'cluster_energy': ('Cluster Energy', 'Potential energy of the cluster.', 'eV'), 'name': ('Name', 'Name of the cluster.', '')}, 'default_columns': ['name', 'cluster_energy', 'id']}

	def update_cluster_in_database_for_if_in_population(self, clusters_in_the_population, energies_of_clusters_removed_from_the_population):
		"""
		This method will update clusters in the database if that cluster was ever accepted into the population. 

		:param clusters_in_the_population: This is a list of the names of clusters that are in the population.
		:type  clusters_in_the_population: list of int
		"""
		def names_of_clusters_in_database(database):
			for row in database.select():
				yield row.name

		if self.ga_recording_scheme == 'All':
			with connect(self.database_path) as database:
				for name in clusters_in_the_population:
					row = database.update(name,ever_in_population=True)
		elif self.ga_recording_scheme == 'Limit_energy_height': 
			with connect(self.database_path) as database:
				for name in clusters_in_the_population:
					if name in names_of_clusters_in_database(database):
						row = database.update(name,ever_in_population=True)
		elif self.ga_recording_scheme == 'Set_higher_limit': 
			with connect(self.database_path) as database:
				for name, energy in zip(clusters_in_the_population,energies_of_clusters_removed_from_the_population):
					if energy <= self.upper_energy_limit:
						row = database.update(name,ever_in_population=True)
		elif self.ga_recording_scheme == 'Set_energy_limits': 
			with connect(self.database_path) as database:
				for name, energy in zip(clusters_in_the_population,energies_of_clusters_removed_from_the_population):
					if self.lower_energy_limit <= energy <= self.upper_energy_limit:
						row = database.update(name,ever_in_population=True)
						
	# -----------------------------------------------------------------------------------------------------
	# Methods for restoring the ga_recording_database from a particular generation. 

	def check_clusters_in_database(self,generation):
		"""
		Will check the clusters in the database and remove any cluster that was created during a most recent unsuccessful generation.

		:param generation: The current generation
		:type  generation: int

		"""
		# remove any files that will prevent it from being read.
		if os.path.exists(self.database_path+'.lock'):
			os.remove(self.database_path+'.lock')
		if os.path.exists(self.database_path+'-journal'):
			os.remove(self.database_path+'-journal')
		# print information about the progress bar loading
		if self.show_GA_Recording_Database_check_percentage:
			sys.stderr.write('The progress bar below shows the progress of reading and checking the GA Recording System database.\n')
		ids_to_remove = []
		# check clusters from the database
		with connect(self.database_path) as database:
			total_size_of_database = float(database.count())
			if self.show_GA_Recording_Database_check_percentage:
				counter = 0.0;
			# Get the last id from the database. The algorithm will cycle through from id=1 to id=last_id
			with database.managed_connection() as con: 
				cur = con.cursor()
				last_id = database.get_last_id(cur)
			# Check every cluster in the database
			for an_id in range(last_id):
				try:
					row = database.get(selection=an_id,columns=['id','key_value_pairs'],include_data=False,verbosity=0)
				except KeyError:
					continue
				if row.gen_made > generation:
					ids_to_remove.append(an_id)
				if self.show_GA_Recording_Database_check_percentage:
					counter += 1.0
					current_percentage = counter/total_size_of_database
					update_progress(current_percentage)
			# remove clusters that were created in the lastest non successful generation.
			database.delete(ids_to_remove)
			if self.show_GA_Recording_Database_check_percentage:
				update_progress(1.0)
		'''
		offset = 0; offset_max = 100; counter = 0.0;
		got_to_end_of_database = False
		with connect(self.database_path) as database:
			total_size_of_database = float(database.count())
		while not got_to_end_of_database:
			counter = 0
			with connect(self.database_path) as database:
				for row in database.select(columns=['id','key_value_pairs'],include_data=False,offset=offset,verbosity=0):
					if row.gen_made > generation:
						ids_to_remove.append(row.id)
					counter += 1.0
					current_percentage = counter/total_size_of_database
					update_progress(current_percentage)
				if counter < offset_max:
					offset += offset_max
				else:
					database.delete(ids_to_remove)
					got_to_end_of_database = True
					update_progress(1.0)
		'''

	def import_information_from_database(self,current_generation):
		"""
		Import any data from the database if it is needed. This should only be needed for the 'Limit_energy_height' scheme.

		:param current_generation: The current generation that your genetic algorithm trial is being resumed from
		:type  current_generation: int

		"""
		if self.write_initial_cluster_in_RAM:
			return 
		with connect(self.database_path) as database:
			for row in database.select():
				self.clusters.append((row.name,row.energy))
		self.sort_by_energy()

# ----------------------------------------------------------------------------------------------------------------------------

import os, sys
from shutil import rmtree, copytree, copyfile
from ase.db import connect

def get_size(size):
    """
	will convert the most human friendly version of the disk space of the database. 

	Input:
		size (float): the disk space of the database in bytes
    """
    power = 2**10
    n = 0
    Dic_powerN = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /=  power
        n += 1
    return size, Dic_powerN[n]+'bytes'

def make_folder(path_to_folder):
	"""
	Will remake a folder, even if it already exists.

	Input:
		path_to_folder (str.): the path to the folder to remake.
	"""
	if not os.path.exists(path_to_folder):
		os.mkdir(path_to_folder)

def convert_to_bytes(size):
	"""
	Will convert the size in any disk space format to bytes.

	:param size: The size of the database in any units
	:type  size: str.

	returns data_size: The size of the database in bytes
	rtype   data_size: float
	"""
	data_size = float(size[:-2]); data_size_type = size[-2:]
	if data_size_type == 'KB':
		data_size *= (1024.0 ** 1)
	elif data_size_type == 'MB':
		data_size *= (1024.0 ** 2)
	elif data_size_type == 'GB':
		data_size *= (1024.0 ** 3)
	elif data_size_type == 'TB':
		data_size *= (1024.0 ** 4)
	else:
		exit('Error')
	return data_size

class GA_Recording_System:
	"""
	This class is designed to record the clsuters that are created during the Organisms program run.

	:param ga_recording_information: This is a dictionary that contains all the information that it needs to record clusters made during the Organisms program as the user desires.
	:type  ga_recording_information (dict.):
	"""
	def __init__(self,ga_recording_information):
		####################################################################################################
		# determine the type of ga_recording_scheme to use, and the other settings associated to each ga_recording_scheme.
		if ga_recording_information == None or ga_recording_information == {}:
			self.ga_recording_information = {'ga_recording_scheme': 'None'}
		else:
			self.ga_recording_information = ga_recording_information
		if self.ga_recording_information['ga_recording_scheme'] in ['None', 'none', None]:
			self.ga_recording_information = {'ga_recording_scheme': 'None'}
		self.ga_recording_scheme = self._get_parameter('ga_recording_scheme',if_not_given_response='None')
		# Determine the name of this recording instance. THis is the name of the folder clusters will be recorded into.
		self.ga_recording_system_name = 'Recorded_Data'
		self.path_to_write_to = os.getcwd()+'/'+self.ga_recording_system_name
		self.ga_recording_system_name = self._get_parameter('ga_recording_system_name',if_not_given_response=self.ga_recording_system_name)
		# determine when to collect data during generations
		self.exclude_recording_cluster_screened_by_diversity_scheme = self._get_parameter('exclude_recording_cluster_screened_by_diversity_scheme',if_not_given_response=True)
		self.limit_number_of_clusters_recorded = self._get_parameter('limit_number_of_clusters_recorded',if_not_given_response='None') # determine the maximum number of clusters to record
		self.limit_size_of_database = self._get_parameter('limit_size_of_database',if_not_given_response='None')
		if not self.limit_size_of_database == None:
			self.limit_size_of_database = convert_to_bytes(self.limit_size_of_database)
		self.show_GA_Recording_Database_check_percentage = self._get_parameter('show_GA_Recording_Database_check_percentage',if_not_given_response=False)
		####################################################################################################
		# Set setting depending on the ga_recording_scheme chosen to use
		if self.ga_recording_scheme == 'All':
			self.clusters_database = GA_Recording_Database(self.path_to_write_to,self.limit_number_of_clusters_recorded,self.limit_size_of_database,ga_recording_scheme=self.ga_recording_scheme,show_GA_Recording_Database_check_percentage=self.show_GA_Recording_Database_check_percentage)
			self.directory = os.getcwd()+'/'+self.ga_recording_system_name
		elif self.ga_recording_scheme == 'Limit_energy_height':
			self.limit_energy_height_of_clusters_recorded = self._get_parameter('limit_energy_height_of_clusters_recorded',if_not_given_response=float('inf')) # Determine the maximum energy of a cluster to record, above the energy of the lowest energetic clusters obtained from this genetic algorithm.
			if self.limit_energy_height_of_clusters_recorded == float('inf'):
				print('Something to note in GA_Recording_System, in GA_Recording_System.py')
				print("You have set ga_recording_scheme == 'Limit_energy_height', but you have set (either written in you Run.py script or given by default) your limit_energy_height_of_clusters_recorded to greatest value it could be")
				print("It would be best to change your ga_recording_scheme input in your ga_recording_information dictionary to :")
				print("ga_recording_scheme == 'All'")
				print("Manually change this in your Run.py script before continuing.")
				exit('The genetic algorithm will finish without completing.')			
			self.clusters_database = GA_Recording_Database(self.path_to_write_to,self.limit_number_of_clusters_recorded,self.limit_size_of_database,ga_recording_scheme=self.ga_recording_scheme,limit_energy_height_of_clusters_recorded=self.limit_energy_height_of_clusters_recorded,show_GA_Recording_Database_check_percentage=self.show_GA_Recording_Database_check_percentage)
		elif self.ga_recording_scheme == 'Set_higher_limit':
			self.upper_energy_limit = self._get_parameter('upper_energy_limit',if_not_given_response=float('inf'))
			if self.upper_energy_limit == float('inf'):
				print('Something to note in GA_Recording_System, in GA_Recording_System.py')
				print("You have set ga_recording_scheme == 'Limit_energy_height', but you have set (either written in you Run.py script or given by default) your upper_energy_limit to greatest value it could be")
				print("It would be best to change your ga_recording_scheme input in your ga_recording_information dictionary to :")
				print("ga_recording_scheme == 'All'")
				print("Manually change this in your Run.py script before continuing.")
				exit('The genetic algorithm will finish without completing.')	
			self.clusters_database = GA_Recording_Database(self.path_to_write_to,self.limit_number_of_clusters_recorded,self.limit_size_of_database,ga_recording_scheme=self.ga_recording_scheme,upper_energy_limit=self.upper_energy_limit,show_GA_Recording_Database_check_percentage=self.show_GA_Recording_Database_check_percentage)
		elif self.ga_recording_scheme == 'Set_energy_limits':
			self.lower_energy_limit = self._get_parameter('lower_energy_limit',if_not_given_response=-float('inf'))
			self.upper_energy_limit = self._get_parameter('upper_energy_limit',if_not_given_response=float('inf'))
			if (self.lower_energy_limit == -float('inf')) and (self.upper_energy_limit == float('inf')):
				print('Something to note in GA_Recording_System, in GA_Recording_System.py')
				print("You have set ga_recording_scheme == 'Set_energy_limits', but you have set (either written in you Run.py script or given by default) your upper energy limit to the greatest value it could be and the lower energy limit to the lowest value it could be.")
				print("It would be best to change your ga_recording_scheme input in your ga_recording_information dictionary to :")
				print("ga_recording_scheme == 'All'")
				print("Manually change this in your Run.py script before continuing.")
				exit('The genetic algorithm will finish without completing.')
			self.clusters_database = GA_Recording_Database(self.path_to_write_to,self.limit_number_of_clusters_recorded,self.limit_size_of_database,ga_recording_scheme=self.ga_recording_scheme,lower_energy_limit=self.lower_energy_limit,upper_energy_limit=self.upper_energy_limit,show_GA_Recording_Database_check_percentage=self.show_GA_Recording_Database_check_percentage)
		elif self.ga_recording_scheme == 'None':
			pass
		else:
			exit('Error')
		####################################################################################################
		# make recording system folder
		if not self.ga_recording_scheme == 'None':
			self.directory = os.getcwd()+'/'+self.ga_recording_system_name
			make_folder(self.directory)
		####################################################################################################
		# Get the name for the information file.
		self.RC_Information_TXT_name = self.ga_recording_system_name+'_Information.txt'
		# Other features of the genetic algorithm to monitor.
		self.record_initial_population = self._get_parameter('record_initial_population',if_not_given_response=False)
		####################################################################################################
		# create required variables and files that are needed to record the stages of the algorithm after the desired generations as specified in saving_points_of_GA
		self.saving_points_of_GA = self._get_parameter('saving_points_of_GA',if_not_given_response=[])
		if not self.saving_points_of_GA == []:
			self.saving_points_in_GA_name = 'Saved_Points_In_GA_Run'
			self.directory_for_saving_points_in_GA = os.getcwd()+'/'+self.saving_points_in_GA_name
			if not os.path.exists(self.directory_for_saving_points_in_GA):
				os.mkdir(self.directory_for_saving_points_in_GA)
		####################################################################################################

	def __repr__(self):
		return str(self.__dict__)

	def add_metadata(self):
		"""
		This method is designed to assign the metadata o the ASE database, as in some versions of ASE this can not happen until at least one cluster has been added to the ASE database.
		"""
		if 'clusters_database' in self.__dict__.keys():
			self.clusters_database.add_metadata()

	def _get_parameter(self,parameter,if_not_given_response=None):
		"""
		This definition is designed to assign self variables to instance of Recording_Clusters. These variables are
		the variables required by Recording_Clusters

		This has been designed to be a private definition. 
		
		:param parameter: This is the parameter to obtain from self.ga_recording_information
		:type  parameter: str.
		:param if_not_given_response: This is the default value to assign the parameter parameter to in this class if it hasn't been given by the user. 
		:type  if_not_given_response: Any

		returns the value to assign a certain parameter to in this class.
		rtype   Any

		"""
		for key, value in self.ga_recording_information.items():
			if key == parameter:
				if value == 'inf':
					value = float('inf') 
				return value
		if if_not_given_response == None:
			print('Error in class Recording_Clusters, in Recording_Clusters.py')
			print('The variable "'+str(parameter)+'" was not entered into Recording_Clusters')
			print('Check this')
			import pdb; pdb.set_trace()
			exit()
		elif if_not_given_response == 'None':
			return None
		else:
			return if_not_given_response

	def add_collection(self,collection,offspring_to_remove):
		"""
		This will add the clusters to the GA_Recording_System database

		:param collection: The collection to be recorded
		:type  collection: Organisms.GA.Collection
		:param offspring_to_remove: This is a list of all the clusters not to write to the database, as they have been removed by the diversity operator, depending on if self.exclude_recording_cluster_screened_by_diversity_scheme is True or False.
		:type  offspring_to_remove: list of int
		"""
		if self.exclude_recording_cluster_screened_by_diversity_scheme:
			offspring_to_remove = offspring_to_remove
		else:
			offspring_to_remove = []
		if self.ga_recording_scheme in ['All','Limit_energy_height','Set_higher_limit','Set_energy_limits']:
			self.clusters_database.add_collection_to_database(collection, offspring_to_remove)

	def update_cluster_in_database_for_if_in_population(self,clusters_in_the_population,energies_of_clusters_removed_from_the_population):
		"""
		This method will update clusters in the database if that cluster was ever accepted into the population. 

		:param clusters_in_the_population: This is a list of the names of clusters that are in the population.
		:type  clusters_in_the_population: list of int
		:param energies_of_clusters_removed_from_the_population: This is a list of the energies of clusters that are in the population.
		:type  energies_of_clusters_removed_from_the_population: list of int

		"""
		if self.ga_recording_scheme == 'None':
			return
		self.clusters_database.update_cluster_in_database_for_if_in_population(clusters_in_the_population, energies_of_clusters_removed_from_the_population)

	#-----------------------------------------------------------------------------------------------------------------
	#-----------------------------------------------------------------------------------------------------------------
	#-----------------------------------------------------------------------------------------------------------------
	# Methods for restoring the ga_recording_system from some generation. 

	def resume_ga_recording_system_from_current_generation(self,resume_from_generation):
		"""
		Will check and restore the ga_recording_system is restored for a generation. 

		:param resume_from_generations: The generation that your genetic algorithm is up to.
		:type  resume_from_generation: int

		"""
		if self.ga_recording_scheme == 'None':
			return
		self.check_clusters_in_database(resume_from_generation)
		self.import_information_from_database(resume_from_generation)

	def check_clusters_in_database(self,generation):
		"""
		Will check the clusters in the database and remove any cluster that was created during a most recent unsuccessful generation.

		:param generation: The current generation
		:type  generation: int

		"""
		if self.ga_recording_scheme == 'None':
			return
		self.clusters_database.check_clusters_in_database(generation)

	def import_information_from_database(self,current_generation):
		"""
		Import any data from the database if it is needed. This should only be needed for the 'Limit_energy_height' scheme.

		:param current_generation: The current generation that your genetic algorithm trial is being resumed from
		:type  current_generation: int

		"""
		if self.ga_recording_scheme == 'None':
			return
		if self.ga_recording_scheme == 'All':
			return
		self.clusters_database.import_information_from_database(current_generation)

	#-----------------------------------------------------------------------------------------------------------------
	#-----------------------------------------------------------------------------------------------------------------
	#-----------------------------------------------------------------------------------------------------------------
	# The follow is methods for recording the initial population or the population at different generations. 

	def record_initial_populations(self,population):
		"""
		Will record the clusters in the initial population into GA_Recording_System.

		:param population: The initial population
		:type  population: Organisms.GA.Population
		"""
		if self.record_initial_population:
			name_of_database = 'Initial_'+population.name
			path_to_write_to = os.getcwd()+'/'+'Initial_'+population.name
			self.record_collection(population,name_of_database,path_to_write_to=path_to_write_to)

	def record_population_at_generation(self,population,current_generation):
		"""
		Will record the clusters in the initial population into GA_Recording_System at the current generation.

		:param population: The current population after the generation has completed
		:type  population: Organisms.GA.Population
		:param current_generation: The generation that your genetic algorithm is up to.
		:type  current_generation: int

		"""
		if current_generation in self.saving_points_of_GA:
			name_of_database = str(population.name)+'_Gen_'+str(current_generation)
			path_to_write_to = self.directory_for_saving_points_in_GA+'/'+str(population.name)+'_Gen_'+str(current_generation)
			self.record_collection(population,name_of_database,path_to_write_to=path_to_write_to)

	def record_collection(self,collection,name_of_database,path_to_write_to):
		"""
		This records an identical copy of the clusters in the population at a certain generation. 

		:param collection: The collection to record into GA_Recording_System.
		:type  collection: Organisms.GA.Collection
		:param name_of_database: Name of the database oto connect to
		:type  name_of_database: str.
		:param path_to_write_to: Path of the database or folder of xyz files to write to.
		:type  path_to_write_to: str. 
			
		"""
		os.mkdir(path_to_write_to)
		database = connect(path_to_write_to+'/'+name_of_database+'.db')
		for cluster in collection:
			database.write(cluster.deepcopy(),name=cluster.name,gen_made=cluster.gen_made,cluster_energy=cluster.energy)
		database.metadata = {'title': str(name_of_database), 'key_descriptions': {'systems': ('Cluster', 'The cluster', ''), 'gen_made': ('Generation Created', 'The generation tthe cluster was created.', ''), 'cluster_energy': ('Cluster Energy', 'Potential energy of the cluster.', 'eV'), 'name': ('Name', 'Name of the cluster.', '')}, 'default_columns': ['name', 'cluster_energy', 'id']}
	