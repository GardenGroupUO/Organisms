

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

class LoD_Comparison_Database:
	"""
	This is a database that holds all the entries of CNA_Entry objects.
	"""
	def __init__(self):
		self.database = Tree()

	def __len__(self):
		"""
		Get the number of clusters in the database.
		"""
		return len(self.database)

	def __getitem__(self,cluster_dir):
		"""
		This def will return the branch of the Tree database you want to access.

		:param cluster_name: The is the name of the cluster you would like to obtain CNA Diversity information about.
		:type  cluster_name: int

		:returns: A branch of a tree. 
		:rtypes: Tree branch (dict) 

		"""
		tree_branch = self.database[cluster_dir] # This is new, check out if needed or if it breaks the algorithm from working.
		if tree_branch == {}:
			del self.database[cluster_dir]
			print('Error in def __getitem__ of Class CNA_Database of Diversity_Scheme.py')
			print('Something is not correct with inputs cluster_dir')
			print('This entry does not yet exist in self.CNA_database')
			print('cluster_dir = '+str(cluster_dir))
			print('Check this out')
			import pdb; pdb.set_trace()
			exit()
		return tree_branch

	def reset(self):
		"""
		Reset the LoD database with a new database
		"""
		del self.database
		self.database = Tree()

	def keys(self):
		"""
		give the names of the clusters in the database

		:returns: The list of the names of the clusters in the database. 
		:rtype:   list of ints

		"""
		return self.database.keys()

	def get_cluster_names(self,order=False):
		"""
		Will provide a list of all the names of all the clusters in the Collection

		:param order: This tag will tell this method whether the user would like the list of names given in order. 
		:type  order: bool

		Returns:
			List of the names of all the clusters in the Population
		"""
		cluster_names = list(self.keys())
		if order == True:
			cluster_names.sort()
		return cluster_names

	def get_entry(self,dir_1,dir_2):
		"""
		This def will return the CNA results from the comparison of two clusters.

		:param name_1: the name of the first cluster you want to compare with.
		:type  name_1: int
		:param name_2: the name of the second cluster you want to compare with.
		:type  name_2: int

		:returns: The CNA_Entry that contains all the CNA information about the comparison of these two clusters.
		:rtypes: CNA_Entry

		"""
		CNA_entry_1 = self.database[dir_1][dir_2]; CNA_entry_2 = self.database[dir_1][dir_2]
		if CNA_entry_1 == {} or CNA_entry_2 == {}:
			print('Error in class CNA_Database, in CNA_Database.py')
			print('There is no entry in the CNA_Database between '+str(dir_1)+' and '+str(dir_2))
			print('dir_1 = '+str(dir_1))
			print('dir_2 = '+str(dir_2))
			print('self.database['+str(dir_1)+']['+str(dir_2)+'] = '+str(self.database[dir_1][dir_2]))
			print('self.database['+str(dir_2)+']['+str(dir_1)+'] = '+str(self.database[dir_2][dir_1]))
			print('Check this.')
			import pdb; pdb.set_trace()
			exit()
		elif not CNA_entry_1 is CNA_entry_2:
			print('Error in class CNA_Database, in CNA_Database.py')
			print('self.database[dir_1][dir_2] is not the same as self.database[dir_2][dir_1]')
			print('dir_1 = '+str(dir_1))
			print('dir_2 = '+str(dir_2))
			print('self.database['+str(dir_1)+']['+str(dir_2)+'] = '+str(self.database[dir_1][dir_2]))
			print('self.database['+str(dir_2)+']['+str(dir_1)+'] = '+str(self.database[dir_2][dir_1]))
			print('This should not be the case. What should be true is self.database[dir_1][dir_2] == self.database[dir_2][dir_1] == CNA_Entry(cluster1,cluster2).')
			print('Check this.')
			import pdb; pdb.set_trace()
			exit()
		return CNA_entry_1

	def add(self, dir_1, dir_2, result):
		"""
		This def will obtain the CNA Information for the comparison of name_1 and name_2, and add it to the CNA_Database

		:param name_1: The name of the first cluster to compare against.
		:type  name_1: int
		:param name_2: The name of the second cluster to compare against.
		:type  name_2: int
		:param result: The result of the comparison of the IDCM. True if they are structurally similar by the IDCM, False if not.
		:type  result: bool

		"""
		# Get the CNA comparisons of the two cluters
		if dir_1 == dir_2:
			print('Error in def add of Class CNA_Database of Diversity_Scheme.py')
			print('cluster_1 and cluster_2 have the same dir')
			print('cluster_1.dir = '+str(dir_1))
			print('cluster_2.dir = '+str(dir_2))
			print('Check this out')
			import pdb; pdb.set_trace()
			exit()
		elif (not self.database[dir_1][dir_2] == {}) and (not self.database[dir_2][dir_1] == {}) and (not self.database[dir_1][dir_2] is self.database[dir_2][dir_1]):
			print('Error in class CNA_Database, in CNA_Database.py')
			print('self.database[dir_1][dir_2] is not the same as self.database[dir_2][dir_1]')
			print('dir_1 = '+str(dir_1))
			print('dir_2 = '+str(dir_2))
			print('self.database['+str(dir_1)+']['+str(dir_2)+'] = '+str(self.database[dir_1][dir_2]))
			print('self.database['+str(dir_2)+']['+str(dir_1)+'] = '+str(self.database[dir_2][dir_1]))
			print('This should not be the case. What should be true is self.database[dir_1][dir_2] == self.database[dir_2][dir_1] == CNA_Entry(cluster1,cluster2).')
			print('Check this.')
			import pdb; pdb.set_trace()
			exit()
		#new_entry = CNA_Entry(dir_1,CNA_profile_dir_1,dir_2,CNA_profile_dir_2,self.rCut_low,self.rCut_high,self.rCut_resolution,self.get_CNA_similarities_method,self.get_comparison_method)
		self.database[dir_1][dir_2] = result
		self.database[dir_2][dir_1] = result

	def remove(self,dir_to_remove):
		"""
		Remove all entries that exists in the database that are associated with a particular cluster.

		:param name_to_remove: The name of the cluster you would like to remove from the CNA_Database.
		:type  name_to_remove: int

		"""
		LoD_entries_for_other_dirs = self.database[dir_to_remove].keys()
		# delete entries that include dir_to_remove in all other branches in the CNA_Database
		for LoD_entries_for_other_dir in LoD_entries_for_other_dirs:
			del self.database[LoD_entries_for_other_dir][dir_to_remove]
		# remove the complete branch associated with dir_to_remove
		del self.database[dir_to_remove]

	def which_clusters_in_LoD_comparison_database_are_similar(self):
		"""
		This method will return a dict of all the similar clusters in the LoD database, where pairs of clusters have been deemed structurally similar by the IDCM. 

		:returns: A dictionary of all the clusters that have been deemed structurally similar to each other. The format of this dictionary is {name_1: [name_2, name_3, ..., names of all the clusters that name_1 is structurally similar to by the IDCM], ...}. 
		:rtypes: dict. 

		"""
		identical_pairs = {}
		clusters_in_database = list(self.keys())
		# This will make a 2D matrix (as a dict) of similarity data.
		for index1 in range(len(clusters_in_database)):
			name1 = clusters_in_database[index1]
			for index2 in range(index1+1,len(clusters_in_database)):
				name2 = clusters_in_database[index2]
				if self[name1][name2]:
					identical_pairs.setdefault(name1,[]).append(name2)
					identical_pairs.setdefault(name2,[]).append(name1)
		return identical_pairs

	def is_cluster_pair_in_the_database(self,dir_1,dir_2):
		"""
		Determine if a CNA entry exists for two clusters in the database

		:param name_1: The name of the first cluster you would like to look for an entry in the CNA_Database.
		:type  name_1: int
		:param name_2: The name of the second cluster you would like to look for an entry in the CNA_Database.
		:type  name_2: int

		:returns: True if this cluster pair is in the database, False if not. 
		:rtypes: bool

		"""
		if self.database[dir_1][dir_2] == {}:
			if not self.database[dir_2][dir_1] == {}:
				print('Error in class CNA_Database, in CNA_Database.py')
				print('The Tree is not full')
				print('There is an entry for self.database[dir_1][dir_2], but not for self.database[dir_2][dir_1].')
				print('dir_1 = '+str(dir_1))
				print('dir_2 = '+str(dir_2))
				print('self.database['+str(dir_1)+']['+str(dir_2)+'] = '+str(self.database[dir_1][dir_2]))
				print('self.database['+str(dir_2)+']['+str(dir_1)+'] = '+str(self.database[dir_2][dir_1]))
				print('This should not be the case. What should be true is self.database[dir_1][dir_2] == self.database[dir_2][dir_1] == CNA_Entry(cluster1,cluster2).')
				print('Check this.')
				import pdb; pdb.set_trace()
				exit()
			del self.database[dir_2][dir_1]
			del self.database[dir_1][dir_2]
			return False
		else:
			if self.database[dir_2][dir_1] == {}:
				print('Error in class CNA_Database, in CNA_Database.py')
				print('The Tree is not full')
				print('There is an entry for self.database[dir_1][dir_2], but not for self.database[dir_2][dir_1].')
				print('dir_1 = '+str(dir_1))
				print('dir_2 = '+str(dir_2))
				print('self.database['+str(dir_1)+']['+str(dir_2)+'] = '+str(self.database[dir_1][dir_2]))
				print('self.database['+str(dir_2)+']['+str(dir_1)+'] = '+str(self.database[dir_2][dir_1]))
				print('This should not be the case. What should be true is self.database[dir_1][dir_2] == self.database[dir_2][dir_1] == CNA_Entry(cluster1,cluster2).')
				print('Check this.')
				import pdb; pdb.set_trace()
				exit()
			elif not self.database[dir_1][dir_2] is self.database[dir_2][dir_1]:
				print('Error in class CNA_Database, in CNA_Database.py')
				print('self.database[dir_1][dir_2] is not the same as self.database[dir_2][dir_1]')
				print('dir_1 = '+str(dir_1))
				print('dir_2 = '+str(dir_2))
				print('self.database['+str(dir_1)+']['+str(dir_2)+'] = '+str(self.database[dir_1][dir_2]))
				print('self.database['+str(dir_2)+']['+str(dir_1)+'] = '+str(self.database[dir_2][dir_1]))
				print('This should not be the case. What should be true is self.database[dir_1][dir_2] == self.database[dir_2][dir_1] == CNA_Entry(cluster1,cluster2).')
				print('Check this.')
				import pdb; pdb.set_trace()
				exit()
			return True

	def LoD_Similarity_Analysis(self,dir_1,dir_2):
		"""
		This def will obtain the max similarity percentage from the compararison of two clusters, name_1 and name_2.

		:param name_1: The name of the first cluster you would like to look for an entry in the CNA_Database.
		:type  name_1: int
		:param name_2: The name of the second cluster you would like to look for an entry in the CNA_Database.
		:type  name_2: int

		:returns: The result from the IDCM. This will be True if this cluster pair is in the database, False if not. 
		:rtypes: bool

		"""
		LoD_entry = self.get_entry(dir_1,dir_2)
		return LoD_entry
		
	def are_all_entries_false(self,all_collections):
		"""
		This method checks if all entries in the database are false. This method performs this after clusters have been removed from the population or offspring_pool due to violating the IDCM predatino operator. At this point, all entries should be false. 
		
		:param all_collections: This is a list of the population and the offspring pool.
		:type  all_collections: list of Organisms.GA.Collections.Collections

		"""
		for dir1, tree_branch in self.database.items():
			for dir2, similarity_result in tree_branch.items(): 
				if similarity_result == True:
					print('Error in LoD_Comparison_Database')
					print('Found two identical clusters in database.')
					print('This should not be the case at this point in the GA.')
					print('cluster1: '+str(dir1)+', cluster2: '+str(dir2))
					print('------------------------------------------------------------')
					self.make_database_table()
					print('------------------------------------------------------------')
					print('Check this')
					import pdb; pdb.set_trace()
					exit('This program will exit without completing')
		size_of_all_collections = sum([len(a) for a in all_collections])
		if not len(self.database.keys()) == size_of_all_collections:
			print('Error1')
			import pdb; pdb.set_trace()
			exit()

		for dir1, tree_branch in self.database.items():
			if not len(tree_branch) == size_of_all_collections - 1:
				print('Error2')
				import pdb; pdb.set_trace()
				exit()

	def check_for_issues(self, population):
		"""
		This method check to make sure there are no issue with the LoD Database after the natural selection process

		:param population: This is the population
		:type  population: Organisms.GA.Population.Population
		"""
		all_cluster_names = population.get_cluster_names(order=True)
		all_cluster_names_in_database = self.get_cluster_names(order=True)
		if not all_cluster_names == all_cluster_names_in_database: 
			print("The lists are not identical, check_for_issues, LoD Database") 
			import pdb; pdb.set_trace()
			exit()

		for dir1, tree_branch in self.database.items():
			for dir2, similarity_result in tree_branch.items(): 
				if similarity_result == True:
					print('Error in LoD_Comparison_Database')
					print('During Generation, No Epoch')
					print('Found two identical clusters in database.')
					print('This should not be the case at this point in the GA.')
					print('cluster1: '+str(dir1)+', cluster2: '+str(dir2))
					print('------------------------------------------------------------')
					#self.make_database_table()
					print('------------------------------------------------------------')
					print('Check this')
					import pdb; pdb.set_trace()
					exit('This program will exit without completing')

	def make_database_table(self):
		"""
		This method prints a table of the database. 
		"""
		all_cluster_names_in_database = self.get_cluster_names(order=True)
		row_format ="{:>7}" * (len(all_cluster_names_in_database) + 1)
		print(row_format.format("", *all_cluster_names_in_database))
		for cluster_name1 in all_cluster_names_in_database:
			similarities = []
			for cluster_name2 in all_cluster_names_in_database: 
				if cluster_name1 == cluster_name2:
					similarity = '--'
				else:
					similarity = str(self.database[cluster_name1][cluster_name2])
				similarities.append(similarity)
			#import pdb; pdb.set_trace()
			print(row_format.format(cluster_name1, *similarities))










