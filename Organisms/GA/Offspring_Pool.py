import os, shutil
from Organisms.GA.Collection import Collection

class Offspring_Pool(Collection):
	"""
	This class is designed to hold the offspring that are made during the Organisms program.

	:param name: The name of the Offspring_Pool. The names of all the collections should be different to prevent confusion, but this shouldn't affect how this program works.
	:type  name: str.
	:param offspring_pool_size: The maximum number of clusters in the collection
	:type  offspring_pool_size: int 

	"""
	def __init__(self,name,offspring_pool_size):
		Collection.__init__(self,name,offspring_pool_size,have_database=False)

	def sort_by_fitness(self):
		"""
		Sort the offspring in the Offspring_Pool by fitness
		"""
		self.clusters.sort(key=lambda cluster: cluster.fitness, reverse=True)

	def clean(self):
		"""
		Remove all the clusters in the collection.
		"""
		cleaned_offspring_names = []
		for index in range(len(self)-1,-1,-1):
			offspring_name = self[index].name
			cleaned_offspring_names.append(offspring_name)
			del self[index]
		return cleaned_offspring_names
