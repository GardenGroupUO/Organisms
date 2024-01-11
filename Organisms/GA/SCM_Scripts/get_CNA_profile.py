
#import numpy as np

from multiprocessing import Process, Queue


def get_tasks(all_input_data):
	"""
	This is a generator that allows many total_CNA_profiles to be obtained at many rCut values in parallel. 

	The all_input_data is in the format:

	all_input_data = [(cluster1, [all rCuts to measure in cluster1 a list]), (cluster2, [all rCuts to measure in cluster2 a list]), ...]
	
	Clusters as given as Organisms.GA.Cluster objects. 

	rCuts are given as a liust of floats to be read in a for loop. 

	:param all_input_data: This is a list of all the tasks you would like to perform.
	:type  all_input_data: list

	:returns: Yields a tuple of (the cluster, rCut)
	:rtype:   (Organisms.GA.Cluster, float)

	"""
	for cluster, rCuts in all_input_data:
		for rCut in rCuts:
			yield (cluster,rCut)


def get_CNA_profile(all_input_data, get_single_CNA_method, no_of_cpus=1):
	'''
	This def will return the CNA profile of a cluster at a range of given values of rCut.

	:param cluster: This is the cluster to obtain the CNA profile of.
	:type  cluster: Either Cluster or ase.Atoms
	:param rCuts: The range of values of rCuts to obtain the CNA profile of.
	:type  rCuts: float

	:returns: This returns the name of the cluster, and the atomic_CNA_profiles. 
	:rtype:   (int, Counter)
	'''

	tasks_that_are_done = Queue()

	# creating processes
	number_of_jobs_performed = 0
	processes = []
	data_keys = []
	for cluster, rCut in get_tasks(all_input_data):
		cluster_name = cluster.name
		if cluster_name not in data_keys:
			data_keys.append(cluster_name)
		proc = Process(target=get_single_CNA_method, args=(cluster, rCut, True, tasks_that_are_done))
		processes.append(proc)
		proc.start()
		number_of_jobs_performed += 1
		if len(processes) >= no_of_cpus:
			processes[0].join()
			del processes[0]

	# completing process
	while len(processes) > 0:
		processes[0].join()
		del processes[0]

	# Sort data
	data = {cluster_name: [[], []] for cluster_name in data_keys}
	for _ in range(number_of_jobs_performed):
		task = tasks_that_are_done.get()
		cluster_name, rCut, total_CNA_profile = task
		data[cluster_name][0].append(rCut)
		data[cluster_name][1].append(total_CNA_profile)

	if not tasks_that_are_done.empty():
		print('Error in def get_CNA_profile, in get_CNA_profile.py')
		print('Queue is not empty')
		print('Check this')
		import pdb; pdb.set_trace(0)
		exit('This program with exit without completing')

	for key in data.keys():
		rCuts, total_CNA_profiles = data[key]
		total_CNA_profiles_sorted_by_rCuts = [total_CNA_profile for _,total_CNA_profile in sorted(zip(rCuts,total_CNA_profiles))]
		data[key] = total_CNA_profiles_sorted_by_rCuts

	data = sorted(data.items())
	return data