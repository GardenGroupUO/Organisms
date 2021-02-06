import os
from ase.db import connect
from ase.io import read

from Organisms.GA.SCM_Scripts.TC_SCM_Methods import get_total_CNA_profile  as get_total_CNA_profile_T_SCM
from Organisms.GA.SCM_Scripts.AC_SCM_Methods import get_atomic_CNA_profile as get_total_CNA_profile_A_SCM
from Organisms.GA.SCM_Scripts.TC_SCM_Methods import get_CNA_similarity     as get_CNA_similarity_T_SCM
from Organisms.GA.SCM_Scripts.AC_SCM_Methods import get_CNA_similarity     as get_CNA_similarity_A_SCM

class Memory_Operator:

	def __init__(self,memory_operator_information):
		"""

		"""
		if memory_operator_information == {}:
			memory_operator_information['Method'] = 'Off'
		self.method = memory_operator_information['Method']
		if self.method in ['Off','off','OFF','False','false','FALSE',False,None,'None','none','']:
			self.method = 'Off'
		if self.method == 'Off':
			return
		self.rCut = memory_operator_information['rCut']
		self.cut_off_similarity = memory_operator_information['cut_off_similarity']
		if memory_operator_information['SCM Type'] == 'A-SCM':
			self.get_CNA_profile_method = get_total_CNA_profile_A_SCM
			self.get_CNA_similarity_method = get_CNA_similarity_A_SCM
		elif memory_operator_information['SCM Type'] == 'T-SCM':
			self.get_CNA_profile_method = get_total_CNA_profile_T_SCM
			self.get_CNA_similarity_method = get_CNA_similarity_T_SCM
		else:
			exit('Error')

		if self.method == 'after last epoch':
			pass
		elif self.method == 'population':
			self.max_repeat = memory_operator_information['max repeat']
			self.repeats_of_clusters_in_pop_per_generation = {}
		elif self.method == 'clusters in database':
			self.path_to_initial_clusters_database = memory_operator_information['Initial clusters database']
		else:
			exit('memory operator method')
		self.memory_CNA_profiles = []

		self.memory_operator_name = 'Memory_Operator_Data'
		if not os.path.exists(self.memory_operator_name):
			os.mkdir(self.memory_operator_name)
		self.memory_operator_database_name = 'Memory_Operator_Datbase.db'
		self.memory_operator_database_path = self.memory_operator_name+'/'+self.memory_operator_database_name
		self.have_setup_memory_operator = False

	def get_CNA_profile(self,cluster):
		"""

		"""
		return_list = []
		self.get_CNA_profile_method((cluster,self.rCut),return_list)
		cluster_CNA_profile = return_list[0]
		return cluster_CNA_profile

	def setup_from_database(self,last_cluster_name,current_generation):
		"""

		"""
		if self.method == 'Off':
			return
		elif self.method == 'clusters in database':
			#import multiprocessing as mp
			#manager = mp.Manager()
			#return_list = []#manager.list()
			with connect(self.path_to_initial_clusters_database) as database:
				for row in database.select():
					cluster = row.toatoms()
					cluster_CNA_profile = self.get_CNA_profile(cluster)
					self.memory_CNA_profiles.append(cluster_CNA_profile)	
		if not os.path.exists(self.memory_operator_database_path):
			with connect(self.memory_operator_database_path) as database:
				for row in database.select():
					if row.name <= last_cluster_name:
						cluster = row.toatoms()
						cluster_CNA_profile = self.get_CNA_profile(cluster)
						self.memory_CNA_profiles.append(cluster_CNA_profile)	
					else:
						del db[row.id]
		self.have_setup_memory_operator = True

	def __repr__(self):
		return str(self.__dict__)

	def is_too_similar(self,cluster_CNA_profile,memory_CNA_profile):
		"""

		"""
		similarity = self.get_CNA_similarity_method(cluster_CNA_profile,memory_CNA_profile)
		#print('similarity: '+str(similarity))
		return (similarity >= self.cut_off_similarity)

	def check_collection(self,collection):
		"""

		"""
		if (self.method == 'Off') or (len(self.memory_CNA_profiles) == 0):
			return []
		if not self.have_setup_memory_operator:
			exit('Error in memory operaotr')
		offspring_to_remove_because_too_similar_to_a_cluster_in_memory = []
		for index in range(len(collection)):
			offspring = collection[index]
			offspring_CNA_profile = self.get_CNA_profile(offspring)
			for memory_CNA_profile in self.memory_CNA_profiles:
				if self.is_too_similar(offspring_CNA_profile,memory_CNA_profile):
					offspring_to_remove_because_too_similar_to_a_cluster_in_memory.append((offspring.name,index))
					break
		offspring_to_remove_because_too_similar_to_a_cluster_in_memory.sort(key=lambda x:x[1])
		return offspring_to_remove_because_too_similar_to_a_cluster_in_memory

	def remove_similar_clusters_from_offsprng_pool(self,collection,offspring_to_remove_because_too_similar_to_a_cluster_in_memory,print_details):
		"""

		"""
		clusters_being_removed_by_memory_operator = []
		for cluster_name, cluster_index in offspring_to_remove_because_too_similar_to_a_cluster_in_memory[::-1]:
			cluster_being_removed_by_memory_operator = collection.pop(cluster_index)
			cluster_being_removed_by_memory_operator.ever_in_population = False
			cluster_being_removed_by_memory_operator.excluded_because_violates_predation_operator = False
			cluster_being_removed_by_memory_operator.initial_population = False
			cluster_being_removed_by_memory_operator.removed_by_memory_operator = True
			clusters_being_removed_by_memory_operator.append(cluster_being_removed_by_memory_operator)
		if print_details and (not len(clusters_being_removed_by_memory_operator) == 0):
			print('------------------------------------------------------------------------------------------------------------------------------')
			print('The following offspring were removed from the offspring pool because they were too similar to a cluster in the memory database')
			for cluster in clusters_being_removed_by_memory_operator:
				print('Cluster: '+str(cluster.name))
			print('------------------------------------------------------------------------------------------------------------------------------')
		return clusters_being_removed_by_memory_operator

	def is_similar_cluster_in_memory_operator(self,cluster):
		"""

		"""
		if (self.method == 'Off') or (len(self.memory_CNA_profiles) == 0):
			return False
		if not self.have_setup_memory_operator:
			exit('Error in memory operaotr')
		cluster_CNA_profile = self.get_CNA_profile(cluster)
		for memory_CNA_profile in self.memory_CNA_profiles:
			if self.is_too_similar(cluster_CNA_profile,memory_CNA_profile):
				return True
		return False

	def record_clusters_in_population_from_epoch(self, population):
		"""

		"""
		self.add_clusters_to_memory_operator(population)
		'''
		CNA_profiles = []
		for cluster in population:
			cluster_CNA_profile = self.get_CNA_profile(cluster)
			CNA_profiles.append((cluster.name, cluster_CNA_profile))
		similarities = {}
		for index1 in range(len(CNA_profiles)):
			name1, CNA_profile1 = CNA_profiles[index1]
			for index2 in range(index1+1,len(CNA_profiles)):
				name2, CNA_profile2 = CNA_profiles[index1]
				if name1 == name2:
					exit('errpr')
				comparison = (name1,name2) if (name1 < name2) else (name2,name1)
				similarities[comparison] = self.get_CNA_similarity_method(CNA_profile1,CNA_profile2)
		'''

	def look_through_population(self, population):
		"""

		"""
		updated_repeats_of_clusters_in_pop_per_generation = {}
		clusters_to_add_to_memory = []
		for cluster in population:
			number = self.repeats_of_clusters_in_pop_per_generation.get(cluster.name, default=0) + 1
			if number == self.max_repeat:
				clusters_to_add_to_memory.append(cluster)
			else:
				updated_repeats_of_clusters_in_pop_per_generation[cluster.name] = number
		self.repeats_of_clusters_in_pop_per_generation = updated_repeats_of_clusters_in_pop_per_generation
		if not len(clusters_to_add_to_memory):
			self.add_clusters_to_memory_operator(clusters)

	def add_clusters_to_memory_operator(self,clusters):
		"""

		"""
		if self.method == 'Off' or self.method == 'clusters in database':
			return
		with connect(self.memory_operator_database_path) as database:
			for cluster in clusters:
				database.write(cluster,name=cluster.name,gen_made=cluster.gen_made)
				cluster_CNA_profile = self.get_CNA_profile(cluster)
				self.memory_CNA_profiles.append(cluster_CNA_profile)