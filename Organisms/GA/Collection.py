import os 
from numpy import zeros
from shutil import copyfile, rmtree
from ase.io import read as ase_read
from ase.io import write as ase_write
from ase.db import connect
from ase.visualize import view

from statistics import mean
from multiprocessing import Process
import multiprocessing as mp

from Organisms.GA.Cluster import Cluster
from Organisms.GA.EnergyProfile import tail, remove_end_lines_from_text

class Collection:
	"""
	This is the foundation of the object used to store clusters in the population, the offspring, and for recording clusters made during the genetic algorithm using the GA_Recording_System.py

	:param path: The path that clusters will be written to disk. Default: None, meaning will write to same path as your execution Run.py file. 
	:type  path: str. 
	:param name: Name of the Collection. This can be any name you like, it is just to note what the collection is. All collections should have a unique name if possible to prevent confusion, however this will not break the program.
	:type  name: str. 
	:param size: This is the number of clusters that should be in the collection. In this version of the Organisms program, the number of clusters in the population and made during Creation of Offspring should be consistant throughout the genetic algorithm process.
	:type  size: int 
	:param write_collection_history: This will tell the collection to record a txt file of what clusters were in the collection over the generations Organisms performs. Default: False
	:type  write_collection_history: bool.
	:param write_files_as: This tells the collection if and how to write clusters to the disk (Default: "database"). There are three options:
							
							* "database" if you want the Collection to make a database
							* "xyz" if you want the Collection to make xyz files
							* None, "None" or "none" if you do not want the Collection to make any cluster files
	:type  write_files_as: str.

	"""
	def __init__(self,name,size,path=None,have_database=False,write_collection_history=False,write_cluster_in_RAM=True):
		# Write main details for Collection object.
		self.name = name
		self.size = size
		self.write_cluster_in_RAM = write_cluster_in_RAM
		# sort out if writing clusters to database:
		if self.write_cluster_in_RAM:
			self.clusters = []
		else:
			self.no_of_clusters_counter = 0
		#############################
		# Options about how to write clusters to disk.
		#############################
		# preparing folders to write information to for Collection 
		if path == None:
			self.path = os.getcwd()+'/'+self.name
		else:
			self.path = path
		self.have_database = have_database
		self.write_collection_history = write_collection_history
		if self.have_database or self.write_collection_history:
			self.make_collection_folder()
		#############################
		# set up database or folders for recording clusters to disk.
		# and if the database exists, make sure that it has been turned to read and write
		if self.have_database:
			self.database_path = self.path+'/'+str(self.name)+'.db'
		#############################
		# set up history writing folders for Collection
		if self.write_collection_history:
			self.create_collection_history()
		####################################################################################################################

	def __repr__(self):
		return '<Collection: '+str(self.name)+'> current size: '+str(len(self))+'; Clusters: '+str(self.clusters)

	def information(self):
		tostring =  '--------------------------------------------------------------------------\n'
		tostring += '<Collection: '+str(self.name)+'> current size: '+str(len(self))+'\n'
		for cluster in self.clusters:
			tostring += 'Cluster: '+str(cluster.name)+'; Energy: '+str(cluster.energy)+'; Fitness: '+str(cluster.fitness)+'\n'
		tostring += '--------------------------------------------------------------------------\n'
		return tostring

	def add_metadata(self):
		"""
		Due to an issue with some versions of ASE, this method will write metadata to the ASE database, if a database is being used to store cluster information.
		"""
		if self.have_database:
			metadata = {}
			metadata['title'] = str(self.name)
			metadata['default_columns'] = ['name', 'cluster_energy', 'id']
			# ----------------------------------------------------
			metadata['key_descriptions'] = {}
			metadata['key_descriptions']['name'] = ('Name', 'Name of the cluster.', '')
			metadata['key_descriptions']['gen_made'] = ('Generation Created', 'The generation the cluster was created.', '')
			metadata['key_descriptions']['cluster_energy'] = ('Cluster Energy', 'Potential energy of the cluster.', 'energy_units')
			metadata['key_descriptions']['ever_in_population'] = ('ever_in_population','This variable indicates if the cluster was ever in the population. If an offspring was made and was not ever accepted into the population, this variable will be False. If the cluster had been in the population for even one generation, this variable will be True.','bool')
			metadata['key_descriptions']['excluded_because_violates_predation_operator'] = ('excluded_because_violates_predation_operator','This variable will determine if a cluster was excluded from the population because it violated the predation operator.','bool')
			metadata['key_descriptions']['initial_population'] = ('initial_population','This variable will indicate if the cluster was apart of a newly created population.','bool')
			metadata['key_descriptions']['removed_by_memory_operator'] = ('removed_by_memory_operator','This variable will indicate if a cluster is removed because it resembles a cluster in the memory operator.','bool')
			# ----------------------------------------------------
			with connect(self.database_path) as database:
				database.metadata =  metadata.copy()
				database._metadata = metadata.copy()

	def make_collection_folder(self):
		"""
		Will create the directory for self.path if it does not exist.
		"""
		if not os.path.exists(self.path):
			os.mkdir(self.path)
		
	def __len__(self):
		"""
		Will return the number of clusters in the collection
		"""
		return len(self.clusters)

	def __getitem__(self,ith):
		"""
		Will return the cluster in the collection at the ith position.

		Inputs:
			ith (int): the index for the cluster that you want to get from the Collectino

		Returns:
			The cluster that you want to obtain from the Collections
		"""
		return self.clusters[ith]

	def __setitem__(self,ith,cluster):
		"""
		Will set a cluster at the ith position in the Collections.

		Inputs:
			ith (int): The index for the cluster that you want to get from the Collection
			cluster (Organisms.GA.Cluster): The Cluster that you want to set in the ith position of the Collection.

		"""
		self.clusters[ith] = cluster

	def __delitem__(self,ith):
		"""
		Remove the cluster at the ith position

		Inputs:
			ith (int): The index for the cluster that you want to get from the Collection

		"""
		self.remove(ith)

	# ---------------------------------------------------------------------------------------------------------------------------------------
	# methods to get names and energies of clusters

	def get_clusters(self):
		"""
		Returns all the clusters that the collection contains in a list

		Returns:
			all the clusters that the collection (list)
		"""
		return self.clusters

	def get_cluster_energies(self):
		"""
		Returns all the clusters that the collection contains in a list

		Returns:
			all the clusters that the collection (list)
		"""
		return [cluster.energy for cluster in self.clusters]

	def get_cluster_from_name(self,name):
		"""
		This method will return the cluster in the Collection with the name "name"

		Inputs:
			name (int): The name of the cluster you want to obtain from the Collection.

		Returns:
			The cluster in the Collection with the name "name" (Organisms.GA.Cluster)
		"""
		index = self.get_index(name)
		return self[index]

	def get_cluster_names(self,order=False):
		"""
		Will provide a list of all the names of all the clusters in the Collection

		Inputs:
			order (bool.): This tag will tell this method whether the user would like the list of names given in order. 

		Returns:
			List of the names of all the clusters in the Population
		"""
		if self.write_cluster_in_RAM:
			cluster_names = [cluster.name for cluster in self.clusters]
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
			self.clusters.sort(key=lambda cluster: cluster.name)
		else:
			import pdb; pdb.set_trace()
			exit('Cant do this')

	def sort_by_energy(self):
		"""
		This method will sort the clusters in the list by their energy (from lowest energy to highest energy).  
		"""
		if self.write_cluster_in_RAM:
			self.clusters.sort(key=lambda cluster: cluster.energy)
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
				if self.clusters[index].name == name_to_find:
					return index
		else:
			print('Error in def get_index in class Collection, in Collection.py')
			print('You can use this method as the collection is not recording clusters in the RAM')
			print('Check your setting for write_cluster_in_RAM for '+str(self))
			exit('This program will exit without completing')
		print('Error in def get_index in Collection.py: Could not find the cluster that has the name = '+str(name_to_find))
		print('Check this')
		import pdb; pdb.set_trace()
		exit('This program will exit without completing.')

	def view_cluster(self,ith):
		"""
		Allow the user to visually look at the cluster using the ASE gui. This is a debugging method.

		Inputs:
			ith (int): the index of the ith cluster in the Collection to view in the ASE gui.
		"""
		self[ith].view()

	# ---------------------------------------------------------------------------------------------------------------------------------------
	# Add, remove, and replacing functions

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
				self.clusters.append(cluster)
			else:
				self.clusters.insert(index,cluster)
		else:
			self.no_of_clusters_counter += 1
		# adds the cluster in the collection to disk
		if self.have_database:
			self.add_to_database(cluster)

	def remove(self, index):
		"""
		Removes a cluster to the Collection.

		Index:
			index (int): the index of the ith cluster in the Collection 
		"""
		# remove the cluster in the collection from the disk
		if self.have_database:
			self.remove_to_database(self.clusters[index])
		# Deletes the cluster from the Collection
		if self.write_cluster_in_RAM:
			del self.clusters[index]
		else:
			self.no_of_clusters_counter -= 1

	def replace(self, index, new_cluster):
		"""
		Will replace the ith cluster in the Collection with a new cluster. Uses the self.remove and self.add methods.

		Inputs:
			index (int): the index of the ith cluster in the Collection 
			new_cluster (Organisms.GA.Cluster): The new cluster to add at the ith position in the Collection
		"""
		self.remove(index)
		self.add(index, new_cluster)

	def pop(self,ith):
		"""
		Pops the cluster at the ith positiion of the Collection and returns it.

		Inputs:
			ith (int): The index for the cluster that you want to get from the Collection

		Returns:
			The cluster that you want to obtain from the Collections (Organisms.GA.Cluster)
		"""
		cluster = self.clusters[ith]
		del self[ith]
		return cluster

	# ---------------------------------------------------------------------------------------------------------------------------------------
	# methods to get the mean, max and min energies of clusters in the collection. 

	def mean_energy(self):
		"""
		The mean energy of the clusters in the population. 

		returns mean_energy: This is the mean energy of the cluster
		rtype   mean_energy: float
		"""
		cluster_energies = [cluster.energy for cluster in self.clusters]
		return mean(cluster_energies)

	def max_energy(self):
		"""
		The maximum energy of the clusters in the population. 

		returns maximum_energy: This is the maximum energy of the cluster
		rtype   maximum_energy: float
		"""
		cluster_energies = [cluster.energy for cluster in self.clusters]
		return max(cluster_energies)

	def min_energy(self):
		"""
		The minimum energy of the clusters in the population. 

		returns minimum_energy: This is the minimum energy of the cluster
		rtype   minimum_energy: float
		"""
		cluster_energies = [cluster.energy for cluster in self.clusters]
		return min(cluster_energies)

	def get_max_mean_min_energies(self):
		"""
		The maximum, mean, and minimum energy of the clusters in the population. 

		returns maximum_energy: This is the maximum energy of the cluster
		rtype   maximum_energy: float
		returns mean_energy: This is the mean energy of the cluster
		rtype   mean_energy: float
		returns minimum_energy: This is the minimum energy of the cluster
		rtype   minimum_energy: float
		"""
		cluster_energies = [cluster.energy for cluster in self.clusters]
		return max(cluster_energies), mean(cluster_energies), min(cluster_energies)

	def is_there_an_energy_range(self,rounding):
		"""
		Determines if there is a range of energies in the collection

		:param rounding: The rounding of the energy of the cluster
		:type  rounding: float

		returns Is there a range of energies in the collection
		rtype   bool
		"""
		cluster_energies = [cluster.energy for cluster in self.clusters]
		if round(max(cluster_energies),rounding) == round(min(cluster_energies),rounding):
			return False
		else:
			return True

	# ---------------------------------------------------------------------------------------------------------------------------------------
	# Methods for entering clusters into the database

	def add_to_database(self,cluster,center=False):
		"""
		Allows the user to write a cluster in the collection to a ASE database

		Inputs:
			cluster (Organisms.GA.Cluster): The cluster to add to the database.
		"""
		with connect(self.database_path) as database:
			cluster_to_database = cluster.deepcopy()
			if center:
				#unit_cell = cluster_to_database.get_cell()
				#cell_lengths = unit_cell.lengths()
				#middle_of_cell = cell_lengths/2.0
				cluster_to_database.center() #about=middle_of_cell)
			database.write(cluster_to_database,name=cluster.name,gen_made=cluster.gen_made,cluster_energy=cluster.energy,ever_in_population=cluster.ever_in_population,excluded_because_violates_predation_operator=cluster.excluded_because_violates_predation_operator,initial_population=cluster.initial_population,removed_by_memory_operator=cluster.removed_by_memory_operator)

	def remove_to_database(self,cluster):
		"""
		Allows the user to remove a cluster in the collection from the  ASE database

		Inputs:
			cluster (Organisms.GA.Cluster): The cluster to remove from the database.
		"""
		with connect(self.database_path) as database:
			cluster_id_to_remove = database.get(name=cluster.name).id
			del database[cluster_id_to_remove]

	def does_contain_database(self,backup):
		"""
		Does the collection contain a backup file.

		:param backup: If true, look for the backup database file. If false, look for the original database file. 
		:type  backup: bool.

		returns does_database_exist: Returns if either the database file or the backup database file exists. 
		rtype   does_database_exist: bool.

		"""
		if backup:
			return os.path.exists(self.database_path+'.backup.db')
		else:
			return os.path.exists(self.database_path)

	def delete_collection_database(self):
		"""
		This method will remove the whole database for this Collection from the disk.
		"""
		if os.path.exists(self.database_path):
			os.remove(self.database_path)

	# ----------------------------------------------------->
	# The following methods are for backing up the database.
	# ----------------------------------------------------->

	def backup_database(self):
		"""
		This method will make a backup of all the clusters in the Collection as a ASE database
		"""
		if self.have_database:
			copyfile(self.database_path, self.database_path+'.backup.db')

	def remove_backup_database(self):
		"""
		This method will remove the backup of all the clusters in the Collection, which will be in the format of a ASE database.
		"""
		if self.have_database:
			os.remove(self.database_path+'.backup.db')

	def remove_backup_database_if_exists(self):
		"""
		This method will remove the backup of all the clusters in the Collection, which will be in the format of a ASE database.
		"""
		if self.have_database:
			if os.path.exists(self.database_path+'.backup.db'):
				os.remove(self.database_path+'.backup.db')

	def move_backup_database_to_normal_backup(self):
		"""
		This method will remove the original database file and replace it with the backup database file. 
		"""
		if not self.have_database:
			return
		if os.path.exists(self.database_path):
			os.remove(self.database_path)
		copyfile(self.database_path+'.backup.db', self.database_path)
		os.remove(self.database_path+'.backup.db')

	# --------------------------------------------------------------------------------->
	# The following methods are for importing clusters from the database into the memory
	# --------------------------------------------------------------------------------->

	def import_clusters_from_database_to_memory(self, current_generation, clusters_in_resumed_population, clusters_in_resumed_population_energies, decimal_place):
		"""
		This method will attempt at obtaining the clustrs from the database and placing them in the collection in the RAM.

		This method is currently set up for reading the population, but if needed it can be reworked for general purpose.

		:param current_generation: The current generation
		:type  current_generation: float
		:param clusters_in_resumed_population: The names of the clusters in the current population 
		:type  clusters_in_resumed_population: list of int
		:param clusters_in_resumed_population_energies: The energies of the clusters in the current population 
		:type  clusters_in_resumed_population_energies: list of floats
		:param decimal_place: The number of decimal places that energies are rounded to in your genetic algorithm run
		:type  decimal_place: int

		returns did_clusters_come_from_backup: Did the imported clusters come from the backup database or the original. True if from the backup database, False if from the original backup.
		rtype   did_clusters_come_from_backup: bool.

		"""
		# determine if the collection wants to have clusters in its memory.
		use_backup_file = self.check_database_and_determine_if_to_use_backup()
		if not self.write_cluster_in_RAM:
			return 
		# method for loading clusters from a database and placing it into the RAM.
		def load_clusters_from_database_to_RAM(database_path,current_generation,clusters_in_resumed_population,clusters_in_resumed_population_energies,decimal_place,self):
			clusters = self.read_collection_database(database_path,current_generation)
			cluster_dict = {cluster.name: cluster for cluster in clusters}
			if self.check_clusters_in_database(cluster_dict, clusters_in_resumed_population, clusters_in_resumed_population_energies, decimal_place):
				self.add_clusters_into_RAM(cluster_dict, clusters_in_resumed_population)
			else:
				print('Error')
				import pdb; pdb.set_trace()
		# If the backup database exists, will gather all clusters from the backup, since this likely means that the last generation did not complete. 
		# Otherwise, will get clusters from the current database.
		if use_backup_file: # Getting data from current Current_Population_details.txt.backup and Population.db.backup.db
			path_to_database_db_to_use = self.database_path+'.backup.db'
		else:               # use data from the current Current_Population_details.txt and Population.db
			path_to_database_db_to_use = self.database_path
		# Load data from the collection database into the RAM
		load_clusters_from_database_to_RAM(self.database_path,current_generation,clusters_in_resumed_population,clusters_in_resumed_population_energies,decimal_place,self)
		# if use_backup_file = True,  data was obtained from backup files
		# if use_backup_file = False, data was obtained from original files
		return use_backup_file

	def check_database_and_determine_if_to_use_backup(self):
		"""
		This method will remove any journal or lock files associated with the database, as well as check that either the database or the backup is functional and can be used to allowing your genetic algorithm trial to resume. 
		
		returns did_use_backup_database: True means the backup database was used. False means the original database was used.
		rtype   did_use_backup_database: bool.
		"""
		database_files_to_check = (self.database_path+'-journal', self.database_path+'.lock', self.database_path+'.backup.db-journal', self.database_path+'.backup.db.lock')
		for database_file in database_files_to_check:
			if os.path.exists(database_file):
				os.remove(database_file)
		if (not os.path.exists(self.database_path+'.backup.db') and not os.path.exists(self.database_path)):
			print('Error in def check_database_and_determine_if_to_use_backup, class Collection, in Collection.py')
			error_message  = 'Population database error\n'
			error_message += 'Could not find neither\n'
			error_message += '--> '+str(self.database_path+'.backup.db')+'\n'
			error_message += '--> '+str(self.database_path)+'\n'
			error_message += 'Can not resume the genetic algorithm if the GA does not have either of these databases.'
			error_message += 'This algortihm will finish without completing.'
			exit(error_message)
		if os.path.exists(self.database_path+'.backup.db'):
			working, results = self.assess_clusters_in_database(self.database_path+'.backup.db')
			if working:
				print('The backup database is all good. Will use the backup database')
				return True # return True to say that the genetic algorithm will use the data from the backup population database
			print('There was an issue with clusters in the backup of the database.')
			print(str(results))
			print('Checking the original database')
		# something went wrong with the backup database file. Will attempt to get the clusters in the population from the original database. 
		working, results = self.assess_clusters_in_database(self.database_path)
		if working:
			print('The original database is all good. Will use the original database')
			return False # return False to say that the genetic algorithm will use the data from the original population database
		print('Error in def check_database_and_determine_if_to_use_backup, class Collection, in Collection.py')
		print('There was an issue with the last cluster:')
		print('----------------------------------------------')
		print(results)
		print('----------------------------------------------')
		print('Check this')
		exit('This program will exit without finishing.')

	def assess_clusters_in_database(self,database_path):
		"""
		This algorithm will check to make sure that there are no technical issues with the database, whether that is the original or the backup database.

		:param database_path: The path to the database
		:type  database_path: str.

		returns is_database_working: Is true if there are no technical issues with the database, False if there are technical issues.
		rtype   is_database_working: bool.
		returns reason_for_issue: Return a None object if everything is all good, otherwise returns the exception detailing the issues with the database or the name of the cluster that caused issues. 
		rtype   is_database_working: None or str.

		"""
		cluster_names_in_database = []
		try:
			with connect(database_path) as database:
				for cluster_row in database.select():
					ase_cluster = cluster_row.toatoms()
					ase_cluster_name = cluster_row.name
					if ase_cluster_name in cluster_names_in_database:
						return (False, ase_cluster_name)
					cluster_names_in_database.append(ase_cluster_name)
		except Exception as exception:
			return (False, exception)
		if not len(cluster_names_in_database) == self.size:
			return (False, Exception('Not enough clusters in the database.\nDatabase size: '+str(len(cluster_names_in_database))+'\nSize of cluster: '+str(self.size)+'.'))
		return (True, None)

	def read_collection_database(self,database_path,current_generation=None):
		"""
		This method will read the clusters in the database. Furthermore, this method is also designed to repair the collection database by removing any clusters that were created after the current generation if desired.

		:param database_path: The path to the database. 
		:type  database_path: str. 
		:param current_generation: The current generation that your genetic algorithm trial is being resumed from
		:type  current_generation: int

		returns clusters: This is a list of all the clusters from the database
		rtype   clusters: list of Organisms.GA.Clusters

		"""
		# Get clusters from database
		clusters = []
		cluster_to_delete = []
		with connect(database_path) as database:
			for cluster_row in database.select():
				if current_generation == None or cluster_row.gen_made <= current_generation:
					ase_cluster = cluster_row.toatoms()
					cluster = Cluster(ase_cluster)
					cluster.custom_verify_cluster(cluster_row.name,cluster_row.gen_made,cluster_row.cluster_energy,cluster_row.ever_in_population,cluster_row.excluded_because_violates_predation_operator,cluster_row.initial_population)
					clusters.append(cluster)
				else:
					cluster_to_delete.append(cluster.id)
		database.delete(cluster_to_delete)
		return clusters

	def remove_clusters_from_database_that_are_from_unsuccessful_generations(self,database_path,current_generation=None):
		"""
		This method will go through the database and delete any clusters of unsuccessful generations. 

		:param database_path: The path to the database. 
		:type  database_path: str. 
		:param current_generation: The current generation that your genetic algorithm trial is being resumed from
		:type  current_generation: int

		"""
		if current_generation == None:
			return
		with connect(database_path) as database:
			cluster_to_delete = []
			for cluster_row in database.select():
				if cluster_row.gen_made > current_generation:
					cluster_to_delete.append(cluster_row.gen_made)
			database.delete(cluster_to_delete)
		
	def check_clusters_in_database(self, cluster_dict, cluster_names, cluster_energies, decimal_place):
		"""
		This method will check that the database contains all the clusters you need and does not have any issues.

		:param cluster_dict: This is a dicionary of all the clusters from the database, given as {cluster_name: Cluster}
		:type  cluster_dict: {int: ASE.Cluster}
		:param cluster_names: list of the names of the clusters that are needed for the collection
		:type  cluster_names: list of int
		:param cluster_energies: list of the energies of the clusters that are needed for the collection
		:type  cluster_energies: list of float

		returns is_database_all_good: True means the database is all good and contains all the clusters needed to restore the collection, as well as comfirming they are of the correct energy. False means something is not working with the database, the database does not contain a required cluster, or there is an issue with clusters not having the energy that they should have. 
		rtype   is_database_all_good: bool.
		"""
		try:
			for cluster_name, cluster_energy in zip(cluster_names,cluster_energies):
				if not cluster_name in cluster_dict.keys():
					print('Note for clusters in cluster: Can not find cluster '+str(cluster_name)+' in the Population database')
					print('Cluster that can not be found: '+str(cluster_name))
					print('Clusters in the population database: '+str(cluster_dict.keys()))
					return False
				cluster = cluster_dict[cluster_name]
				if not round(cluster.energy,decimal_place) == round(cluster_energy,decimal_place):
					print('Found a cluster in the population that has a different energy to that cluster as recorded in the database.')
					print('Energy of cluster as recorded in EnergyProfile.txt: '+str(round(cluster_energy,decimal_place)))
					print('Energy of cluster as recorded in the database: '+str(round(cluster.energy,decimal_place)))
					return False
			return True
		except:
			return False

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
				self.clusters.append(cluster)

	# ---------------------------------------------------------------------------------------------------------------------------------------
	############################# HISTORY FILE METHODS #############################
	# The history file is mainly created for the Population to keep track of the   #
	# clusters that were made during the Organisms program.                           #
	################################################################################

	def history_file_name(self,end_name=None):
		"""
		Get the name of the history file for this Collection.

		Inputs:
			end_name (str): The suffix of the name for the history gfile.
		"""
		if end_name == None:
			self.history_path = self.path+'/'+str(self.name)+"_history.txt"
		else:
			self.history_path = self.path+'/'+str(self.name)+"_history_"+str(end_name)+".txt"

	def get_history_path(self):
		"""
		Return the path to the history file

		Returns:
			the path to the history file
		"""
		return self.history_path

	def open(self,w_or_a):
		"""
		This opens the profile pool text file

		Inputs:
			w_or_a = 'Indicates how to open the file, whether to open it as a new file ("w") or to append information to the history file ("a").
		"""
		self.history_file = open(self.get_history_path(),str(w_or_a))

	def close(self):
		"""
		This closes the history text file.
		"""
		self.history_file.close()
		del self.history_file

	def create_collection_history(self):
		"""
		This definition will create the history file. 

		This includes the folder, contents of the folder and beginning to write the history file.

		It also included information about the clusters in the collection file when it was first created.
		"""
		if not self.write_collection_history:
			return
		self.history_file_name()
		if os.path.exists(self.get_history_path()):
			return
		self.open('w')
		self.history_file.write("This file records all the information about the clusters in the pool and other details about the clusters in the pool. \n")
		self.history_file.write("--------------------------------\n")
		self.history_file.write("OVERALL DETAILS\n")
		self.history_file.write("Collection name: "+str(self.name)+"\n")
		#self.profile.write("Cluster: ")
		#for element in self.cluster_makeup:
		#	self.profile.write(str(element) + " " + str(self.cluster_makeup[element]) + " ")
		#self.profile.write("\n")
		self.history_file.write("--------------------------------\n")
		self.close()

	def add_to_history_file(self,generation_number,is_epoch=False,epoch_due_to_population_energy_convergence=None):
		"""
		This definition will add the information of the population. This is suppose to be used after each generation has completed. 

		:param generation_number: The current generation that the genetic algorithm run has just performed.
		:type  generation_number: int 
		:param is_epoch: Has an epoch just occurred
		:type  is_epoch: bool.
		:param epoch_due_to_population_energy_convergence: If an epoch occurred, was it because the energy of the clusters converged.
		:type  epoch_due_to_population_energy_convergence: bool.

		"""
		if not self.write_collection_history:
			return
		self.open('a')
		if is_epoch:
			self.history_file.write('#-----------------------------------------------------------------------------\n')
			if epoch_due_to_population_energy_convergence:
				self.history_file.write('# -> Reset populationas the clusters in the population converged upon the same energy\n')
			else:
				self.history_file.write('# -> Reset population as reached epoch\n')
			self.history_file.write('#-----------------------------------------------------------------------------\n')
		self.history_file.write("GA Iteration: " + str(generation_number) + "\n")
		self.history_file.write("Clusters in Pool:\t")
		for cluster in self:
			self.history_file.write(str(cluster.name)+"("+str(cluster.gen_made)+")\t")
		self.history_file.write("\n")
		self.history_file.write("Energies of Clusters:\t")
		for cluster in self:
			self.history_file.write(str(cluster.energy) + "\t")
		self.history_file.write("\n")
		self.close()

	def check_PoolProfileTXT_exists(self):
		"""
		This definition checks to see if the PoolProfile folder exists
		"""
		return os.path.exists(self.history_file) and os.path.isfile(self.history_file)

	def check_historyfile(self,resume_from_generation):
		'''
		This method will check the history file to make sure that it does not contain any information from a failed generation.

		If it does contain information from failed generations, it will delete those lines from the history file.

		:param generation_number: The current generation that the genetic algorithm run has just performed.
		:type  generation_number: int 

		'''
		while True:
			counter = 0
			lines_to_remove = 0
			last_lines_in_historyfile = tail(self.history_path,9)[::-1]
			for line in last_lines_in_historyfile:
				line = line.decode("utf-8") 
				if line.startswith('GA Iteration:'):
					line = line.rstrip()
					generation = int(line.replace('GA Iteration:',''))
					if generation > resume_from_generation:
						counter += 1
						lines_to_remove = counter
					elif generation == resume_from_generation:
						break
					elif generation < resume_from_generation:
						print('Error in def check_historyfile, in class Collection, in Collection.py')
						print('The last generation in the '+str(self.history_path)+' is less than the resumed generation.')
						print('Check the Population_history file for this GA run before continuing. There may be an issue here')
						print('Last generation in the Population_history file: '+str(generation))
						print('Generation to resume from: '+str(resume_from_generation))
						import pdb; pdb.set_trace()
						exit('The genetic algorithm will finished without starting.')
				else:
					counter += 1
			if lines_to_remove > 0:
				print('Removing the last '+str(lines_to_remove)+' from '+str(self.history_path))
				remove_end_lines_from_text(self.history_path, lines_to_remove)
			else:
				break
		last_lines_in_historyfile = tail(self.history_path,3)
		historyfile_generation = int(last_lines_in_historyfile[0].decode("utf-8").rstrip().replace('GA Iteration:',''))
		if historyfile_generation == resume_from_generation:
			return
		else:
			print('Error in def check_historyfile, in class Collection, in Collection.py')
			print('The last generation in the '+str(self.history_path)+' is less than the resumed generation.')
			print('Check the Population_history file for this GA run before continuing. There may be an issue here')
			print('Last generation in the Population_history file: '+str(historyfile_generation))
			print('Generation to resume from: '+str(resume_from_generation))
			import pdb; pdb.set_trace()
			exit('The genetic algorithm will finished without starting.')
