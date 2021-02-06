class Collections_Iterator:
	"""
	This iterator is designed to iterate through mutliple collections together, in such a way that we sample every cluster across a range of collections.
	This method is designed to work in place so that it take up minimal amount of space on ram.

	:param population: This is the population being used for this Genetic Run
	:type  population: Organisms.GA.Population
	:param offspring_pools: These are all the offspring_pools that are being used. This can be inputs as one offspring_pool, or a list of multiple offspring_pools
	:type  offspring_pools: Organisms.GA.Offspring_Pool or [Organisms.GA.Offspring_Pool,...]
	:param pass_first_cluster: Start with the first cluster in the population, or the second.
	:type  pass_first_cluster: bool.

	"""
	def __init__(self, population, offspring_pools=None, pass_first_cluster=False):
		self.population = population
		self.collections = [population]

		if not offspring_pools == None:
			if not isinstance(offspring_pools,list):
				self.collections += [offspring_pools]
			else:
				self.collections += offspring_pools

		self.length = len(self.population)
		if not offspring_pools == None:
			for offspring_pool in offspring_pools:
				self.length += len(offspring_pool)

		if pass_first_cluster == False:
			self.index = 0
			self.index_collections = 0
		else:
			self.index = 1
			if self.index >= len(self.collections[0]):
				self.index_collections = 1
			else:
				self.index_collections = 0

	def __iter__(self):
		return self

	def __next__(self):
		"""
		Move through the collections to return the next cluster from all the collections.

		Return
			cluster(Organisms.GA.Cluster): the next cluster in the collections.
		"""
		while True:
			if self.index_collections < len(self.collections):
				if self.index < len(self.collections[self.index_collections]):
					cluster = self.collections[self.index_collections][self.index]
					self.index += 1
					return cluster
				elif self.index == len(self.collections[self.index_collections]):
					self.index = 0
					self.index_collections += 1
				else:
					print('error')
					exit()
			elif self.index_collections == len(self.collections):
				raise StopIteration
			else:
				print('error')
				exit()
