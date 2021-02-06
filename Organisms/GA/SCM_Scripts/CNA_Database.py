'''
CNA_Database.py, Geoffrey Weal, 29/10/2018

This script holds the information required to make a CNA_database.

'''
import os, sys, time
import multiprocessing as mp
from Organisms.GA.SCM_Scripts.MyPool import MyPool
from Organisms.GA.SCM_Scripts.Similarity_Profile import Similarity_Profile

class Tree(dict): #WeakValueDictionary()
	"""
	This is a Tree designed for the CNA_Database to hold references of CNA_Entry.
	"""
	def __missing__(self, key):
		"""
		This rewrites the __missing__ component of a dict to work as a tree.
		"""
		value = self[key] = type(self)()
		return value

	def see_tree(self):
		"""
		This shown the clusters in the database
		"""
		toString = ''
		for key, value in self:
			toString += str(key)+': '+str(sorted([key2 for key2, value2 in self[key]]))+'\n'
		return toString

def cna_profile_generator(collection,rCuts):
	"""
	This is a generator that returns the clusters in the collection with the rCut values to scan across. 

	:param collection: A collection
	:type  collection: Organisms.GA.Collection
	:param rCuts: The list of clusters to scan across with the SCM. 
	:type  rCuts: list of float

	:returns: a tuple of the cluster the rCut values to scan across with the SCM
	"""
	for cluster in collection:
		yield cluster,rCuts

def initial_similarity_profile_generator(collection,cna_database):
	"""
	This is a generator that returns the clusters in the collection with the rCut values to scan across. 

	:param collection: A collection
	:type  collection: Organisms.GA.Collection
	:param cna_database: The list of clusters to scan across with the SCM. 
	:type  cna_database: list of float

	:returns: a tuple of the names of the clusters and their associated CNA profiles.
	:rtype:   (int, int, Counter, Counter)
	"""
	for index_1 in range(len(collection)):
		name_1 = collection[index_1].name
		for index_2 in range(index_1+1,len(collection)):
			name_2 = collection[index_2].name
			if not cna_database.is_pair_in_the_database(name_1,name_2):
				cna_profile_1 = cna_database.cna_profile_database[name_1]
				cna_profile_2 = cna_database.cna_profile_database[name_2]
				yield name_1, name_2, cna_profile_1, cna_profile_2

def similarity_profile_generator(population,offsprings,cna_database):
	"""
	This is a generator that returns the clusters in the collection with the rCut values to scan across. 

	:param population: The population
	:type  population: Organisms.GA.Population
	:param offsprings: The collection of offspring
	:type  offsprings: Organisms.GA.Offspring_Pool
	:param cna_database: The list of clusters to scan across with the SCM. 
	:type  cna_database: list of float

	:returns: a tuple of the names of the clusters and their associated CNA profiles.
	:rtype:   (int, int, Counter, Counter)
	"""
	for cluster_pop in population:
		for offspring in offsprings:
			name_pop = cluster_pop.name
			name_off = offspring.name
			if not cna_database.is_pair_in_the_database(name_pop,name_off):
				cna_profile_cluster_pop = cna_database.cna_profile_database[name_pop]
				cna_profile_offspring   = cna_database.cna_profile_database[name_off]
				yield name_pop, name_off, cna_profile_cluster_pop, cna_profile_offspring
	#initial_similarity_profile_generator(offsprings,cna_database)
	for index_1 in range(len(offsprings)):
		name_1 = offsprings[index_1].name
		for index_2 in range(index_1+1,len(offsprings)):
			name_2 = offsprings[index_2].name
			if not cna_database.is_pair_in_the_database(name_1,name_2):
				cna_profile_1 = cna_database.cna_profile_database[name_1]
				cna_profile_2 = cna_database.cna_profile_database[name_2]
				yield name_1, name_2, cna_profile_1, cna_profile_2

class CNA_Database:
	"""
	This is a database that holds all the entries of CNA_Entry objects.

	:param rCuts: These are the rCut values to scan the CNA across. 
	:type  rCuts: float
	:param population: 
	:type  population: Organisms.GA.Population
	:param cut_off_similarity: The maximum similarity above which to be considered similar enough to exclude offspring from being accessed into future generations. 
	:type  cut_off_similarity: float
	:param get_cna_profile_method: This is the method to get the CNA Profile, either from the T-SCM or the A-SCM. 
	:type  get_cna_profile_method: __func__
	:param get_similarity_profile_method: This is the method that uses the CNA profiles of two clusters in order to give the similarity profile between the two clusters, Whether this is obtained by the T-SCM or the A-SCM. 
	:type  get_similarity_profile_method: __func__
	:param no_of_cpus: The number of cpu to use to obtain the similarity profile between two clusters
	:type  no_of_cpus: int
	:param debug: Get data to use to debug the SCM. Default: False
	:type  debug: bool. 

	"""
	def __init__(self,rCuts,population,cut_off_similarity,get_cna_profile_method,get_similarity_profile_method,no_of_cpus,debug):

		self.cna_profile_database = {}
		self.similarity_profile_database = Tree()

		self.rCuts = rCuts
		self.population = population
		self.cut_off_similarity = cut_off_similarity
		self.get_cna_profile_method = get_cna_profile_method
		self.get_similarity_profile_method = get_similarity_profile_method
		self.no_of_cpus = no_of_cpus
		self.debug = debug

	def reset(self):
		"""
		Reset the CNA profiles of generated clusters and the similarity profile database.
		"""
		self.cna_profile_database = {}
		self.similarity_profile_database = Tree()

	def get_details(self):
		"""
		Retun the information about the CNA Database, including:

		:returns: The cut_off_similarity, get_cna_profile_method, get_similarity_profile_method, no_of_cpus, debug
		:rtype:   (float, __func__, __func__, int, bool)
		"""
		return (self.cut_off_similarity, self.get_cna_profile_method, self.get_similarity_profile_method, self.no_of_cpus, self.debug)

	def __len__(self):
		"""
		Get the number of clusters in the database.

		:returns: The number of CNA profiles that have been recorded. 
		:rtype:   int
		"""
		return len(self.cna_profile_database)

	def keys(self):
		"""
		Return a list of the names of all the clusters in the database

		:returns: A list of the names of all the clusters in the database
		:rtype:   list of int
		"""
		return list(self.cna_profile_database.keys())

	def __getitem__(self,name):
		"""
		Return the similariy_profile of cluster name:

		:param name: The name of the cluster
		:type  name: int

		:returns: The similarity profile for cluster name.
		:rtype:   list of float
		"""
		try:
			return self.similarity_profile_database[name]
		except:
			print("Error in Def __getitem__ in class CNA_Database, in CNA_Database.py")
			print('You are trying to get cluster '+str(name))
			print('But this does not exist in the CNA database')
			print('Clusters in the database: '+str(self.keys()))
			print('Check this out')
			import pdb; pdb.set_trace()
			exit('This program will exit without completing')

	def add(self,collection,initialise=False):
		"""
		Add the similarity data of the clusters in the collection to the CNA_Database

		:param collection: The clusters to add to the CNA_Database
		:type  collection: Organisms.GA.Collection
		:param initialise: Are the clusters from a newly created population. Default: False
		:type  initialise: bool
		"""
		# First, add all the CNA profiles to the cna_profile_database
		CNA_Profiles_to_make = cna_profile_generator(collection,self.rCuts)
		start_time = time.time()
		with MyPool(processes=self.no_of_cpus) as pool:
			results = pool.map_async(self.get_cna_profile_method, CNA_Profiles_to_make)
			results.wait()
		data = results.get()
		end_time = time.time()
		print('Processing CNA Profiles took '+str(end_time - start_time)+' seconds.')
		for cluster_dir, cluster_CNA_profile in data:
			self.cna_profile_database[cluster_dir] = cluster_CNA_profile
		# Second, get the the similarity profiles and add them to the database.
		if initialise:
			CNA_Similarities_to_make = initial_similarity_profile_generator(collection,self)
		else:
			CNA_Similarities_to_make = similarity_profile_generator(self.population,collection,self)
		start_time = time.time()
		with mp.Pool(processes=self.no_of_cpus) as pool:
			results = pool.map_async(self.get_similarity_profile_method, CNA_Similarities_to_make)
			results.wait()
		data = results.get()
		end_time = time.time()
		print('Processing CNA similarities took '+str(end_time - start_time)+' seconds.')
		for name_1, name_2, cna_similarity in data:
			similarity_profile = Similarity_Profile(name_1, name_2, cna_similarity)
			self.similarity_profile_database[name_1][name_2] = similarity_profile
			self.similarity_profile_database[name_2][name_1] = similarity_profile
		##########################################################################

	def remove(self,names_to_remove):
		"""
		Remove all entries that exists in the database that are associated with a particular cluster.

		:param name_to_remove: The name of the cluster you would like to remove from the CNA_Database.
		:type  name_to_remove: int

		"""
		# Take a note of the clusters that will not be removed from the CNA_Database
		# These will be used to help efficiently remove cluster entries in similarity_profile_database
		# that are not needed anymore.
		names_to_look_though = list(self.similarity_profile_database.keys())
		for name_to_remove in names_to_remove:
			if name_to_remove in names_to_look_though:
				names_to_look_though.remove(name_to_remove)
		# remove all cluster entries that are no longer needed in self.cna_profile_database and self.similarity_profile_database
		for name_to_remove in names_to_remove:
			del self.cna_profile_database[name_to_remove]
			del self.similarity_profile_database[name_to_remove]
			for name_to_look_at in names_to_look_though:
				del self.similarity_profile_database[name_to_look_at][name_to_remove]

	def is_pair_in_the_database(self,dir_1,dir_2):
		"""
		Determine if a CNA entry exists for two clusters in the similarity_profile_database

		:param name1: The dir of the first cluster you would like to look for an entry in the CNA_Database.
		:type  name1: int
		:param name2: The dir of the second cluster you would like to look for an entry in the CNA_Database.
		:type  name2: int

		:returns: True if the similarity profile for cluster name1 and name2, False if not.
		:rtype:   bool
		"""
		if dir_1 == dir_2:
			print('Error in class CNA_Database, in CNA_Database.py')
			print('dir_1 and dir_2 are the same')
			print('dir_1 = '+str(dir_1))
			print('dir_2 = '+str(dir_2))
			print('Check this.')
			import pdb; pdb.set_trace()
			exit('This program will exit without completing')
		if self.similarity_profile_database[dir_1][dir_2] == {}:
			if not self.similarity_profile_database[dir_2][dir_1] == {}:
				print('Error in class CNA_Database, in CNA_Database.py')
				print('The Tree is not full')
				print('There is an entry for self.similarity_profile_database[dir_1][dir_2], but not for self.similarity_profile_database[dir_2][dir_1].')
				print('dir_1 = '+str(dir_1))
				print('dir_2 = '+str(dir_2))
				print('self.similarity_profile_database['+str(dir_1)+']['+str(dir_2)+'] = '+str(self.similarity_profile_database[dir_1][dir_2]))
				print('self.similarity_profile_database['+str(dir_2)+']['+str(dir_1)+'] = '+str(self.similarity_profile_database[dir_2][dir_1]))
				print('This should not be the case. What should be true is self.similarity_profile_database[dir_1][dir_2] == self.similarity_profile_database[dir_2][dir_1] == CNA_Entry(cluster1,cluster2).')
				print('Check this.')
				import pdb; pdb.set_trace()
				exit('This program will exit without completing')
			del self.similarity_profile_database[dir_2][dir_1]
			del self.similarity_profile_database[dir_1][dir_2]
			return False
		else:
			if self.similarity_profile_database[dir_2][dir_1] == {}:
				print('Error in class CNA_Database, in CNA_Database.py')
				print('The Tree is not full')
				print('There is an entry for self.similarity_profile_database[dir_1][dir_2], but not for self.similarity_profile_database[dir_2][dir_1].')
				print('dir_1 = '+str(dir_1))
				print('dir_2 = '+str(dir_2))
				print('self.similarity_profile_database['+str(dir_1)+']['+str(dir_2)+'] = '+str(self.similarity_profile_database[dir_1][dir_2]))
				print('self.similarity_profile_database['+str(dir_2)+']['+str(dir_1)+'] = '+str(self.similarity_profile_database[dir_2][dir_1]))
				print('This should not be the case. What should be true is self.similarity_profile_database[dir_1][dir_2] == self.similarity_profile_database[dir_2][dir_1] == CNA_Entry(cluster1,cluster2).')
				print('Check this.')
				import pdb; pdb.set_trace()
				exit('This program will exit without completing')
			elif not self.similarity_profile_database[dir_1][dir_2] is self.similarity_profile_database[dir_2][dir_1]:
				print('Error in class CNA_Database, in CNA_Database.py')
				print('self.similarity_profile_database[dir_1][dir_2] is not the same as self.similarity_profile_database[dir_2][dir_1]')
				print('dir_1 = '+str(dir_1))
				print('dir_2 = '+str(dir_2))
				print('self.similarity_profile_database['+str(dir_1)+']['+str(dir_2)+'] = '+str(self.similarity_profile_database[dir_1][dir_2]))
				print('self.similarity_profile_database['+str(dir_2)+']['+str(dir_1)+'] = '+str(self.similarity_profile_database[dir_2][dir_1]))
				print('This should not be the case. What should be true is self.similarity_profile_database[dir_1][dir_2] == self.similarity_profile_database[dir_2][dir_1] == CNA_Entry(cluster1,cluster2).')
				print('Check this.')
				import pdb; pdb.set_trace()
				exit('This program will exit without completing')
			return True

	def get_similar_clusters_in_database(self):
		"""
		Get clusters in the clusters that are deemed structurally similar in the CNA_Database

		:returns: a list of the names of all the clusters thaat are similar to each other.
		:rtype:   list of int
		"""
		too_similar_database = {}
		names_in_database = list(self.keys())
		for index1 in range(len(names_in_database)):
			name1 = names_in_database[index1]
			for index2 in range(index1+1,len(names_in_database)):
				name2 = names_in_database[index2]
				if self.get_max_similarity(name1,name2) >= self.cut_off_similarity:
					too_similar_database.setdefault(name1,[]).append(name2)
					too_similar_database.setdefault(name2,[]).append(name1)
		return too_similar_database

	def get_all_averages_for_a_cluster(self,cluster_name):
		"""
		Get the averages SCM similarities of a cluser compared to every other clusrer in the similarity profile.

		:param cluster_name: Cluster to get the averages similarities of.
		:type  cluster_name: list of floats

		:returns: all the average similarities between cluster_name any every other cluster in the database. 
		:rtype:   list of float
		"""
		all_cna_averages = [cna_entry.average for _,cna_entry in self.similarity_profile_database[cluster_name].items()]
		return all_cna_averages

	def check_database(self, population):
		"""
		Check the database to make sure there are the correct number of entries in the database.

		:param population: The population
		:type  population: Organisms.GA.Population
		"""
		if not len(self.similarity_profile_database) == len(population):
			print('Issue') 
			import pdb; pdb.set_trace()
			exit('Issue') 
		for branch in self.similarity_profile_database.values():
			if not len(branch) == len(population)-1:
				print('Issue') 
				import pdb; pdb.set_trace()
				exit('Issue') 

	def get_max_similarity(self,name_1,name_2):
		"""
		This def will obtain the max similarity percentage from the compararison of two clusters, name_1 and name_2.

		:param name_1: The name of the first cluster you would like to look for an entry in the CNA_Database.
		:type  name_1: int
		:param name_2: The name of the second cluster you would like to look for an entry in the CNA_Database.
		:type  name_2: int

		:returns: returns the maximum similarity between cluster name_1 and name_2
		:rtype:   float
		"""
		similarity_profile = self.similarity_profile_database[name_1][name_2]
		try:
			return similarity_profile.similarity_max
		except:
			print('Error in def CNA_Analysis of Class CNA_Database of Diversity Scheme.')
			print('This def can not obtain a similarity_category')
			print('This probably means that an entry does not exist')
			print('name_1 = '+str(name_1))
			print('name_2 = '+str(name_2))
			print('self.database['+str(name_1)+']['+str(name_2)+'] = '+str(similarity_profile))
			print('Other information')
			print('self.similarity_profile_database['+str(name_1)+'] = '+str(self.similarity_profile_database[name_1]))
			print('self.similarity_profile_database['+str(name_2)+'] = '+str(self.similarity_profile_database[name_2]))
			#self.print_cna_database_details()
			print('Check this out.')
			import pdb; pdb.set_trace()
			exit()

	def print_cna_database_details(self):
		"""
		Print information about the database. 
		"""
		print('Clusters recorded in the CNA Profile Database: '+str(list(self.cna_profile_database.keys())))
		print('Clusters recorded in the Similarity Profile Database: '+str(list(self.similarity_profile_database.keys())))
		print('')
		print('Average similarities between clusters in the Similarity Profile Database:')
		self.make_simple_table(self.similarity_profile_database)

	def make_simple_table(self,similarity_profile_database):
		"""
		This is a simpled table that can be printed to the terminal that shows all the similarities between clusters in the population + offspring

		:param similarity_profile_database: This is the CNA database that contains all similarity information of clusters in rhe population and offspring.
		:type  similarity_profile_database: Organisms.GA.SCM_Scripts.CNA_Database.CNA_Database

		"""
		similarity_profile_database_keys = sorted(list(similarity_profile_database.keys()))
		similarity_profile_database_list = sorted(list(similarity_profile_database.items()))
		row_format ="{:>4}" * (len(similarity_profile_database_list) + 1)
		print(row_format.format("", *similarity_profile_database_keys))
		for cluster_name, similarity_data in similarity_profile_database_list:
			similarity_data = list(similarity_data.items())
			similarity_data_format = []
			for column, similarity_datum in similarity_data:
				try:
					similarity_data_format.append((column, str(similarity_datum.average)))
				except:
					similarity_data_format.append((column, str(similarity_datum)))
			similarity_data_format += [(cluster_name,'-')]
			similarity_data_format.sort()
			import pdb; pdb.set_trace()
			for index in range(len(similarity_data_format)):
				similarity_data_format[index] = similarity_data_format[index][1]
			import pdb; pdb.set_trace()
			print(row_format.format(cluster_name, *similarity_data_format))








