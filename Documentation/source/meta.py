metadata = {}
metadata['title'] = 'Genetic Algorithm Database'
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

title = metadata['title']
default_columns = metadata['default_columns']
key_descriptions = metadata['key_descriptions']
