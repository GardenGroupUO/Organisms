'''
AC_SRA_Methods.py, Geoffrey Weal, 20/11/2018

This script is designed to include all the methods for performing structural recognition 
task in terms of the Atom Comparison version of the Structural Recognition Algorithm.

'''

from asap3.analysis.localstructure import FullCNA
from collections import Counter
import sys
import multiprocessing as mp

######################################################################

def get_atomic_CNA_profile(input_data):
	"""
	This method will obtain the Atomic CNA profile

	:param input_data: Contains the cluster to perform the CNA on at the rCut value rCut. 
	:type  input_data: (Organisms.GA.Cluster, float)

	:returns: The atomic CNA profile.
	:rtype:   Counter
	"""
	(system,rCut) = input_data
	fullCNA_atoms = FullCNA(system,rCut)
	CNA_profile_on_each_atom = fullCNA_atoms.get_normal_cna()
	for index in range(len(CNA_profile_on_each_atom)):
		CNA_profile_of_an_atom = list(CNA_profile_on_each_atom[index].items())
		CNA_profile_of_an_atom.sort(key=lambda sign:sign[0])
		CNA_profile_on_each_atom[index] = str(CNA_profile_of_an_atom)
	return Counter(CNA_profile_on_each_atom)

def get_tasks(system, rCuts):
	"""
	This is a generator that allows many atomic_CNA_profiles to be obtained at many rCut values in parallel
	
	:param system: This is the cluster to obtain the atomic_CNA_profiles for
	:type  system: Organisms.GA.Cluster
	:param rCuts: This is the rCut value to to obtain the atomic_CNA_profiles at.
	:type  rCuts: float

	:returns: Yields a tuple of (the cluster, rCut)
	:rtype:   (Organisms.GA.Cluster, float)

	"""
	for rCut in rCuts:
		yield (system,rCut)

def get_CNA_profile(input_data):
	'''
	This def will return the CNA profile of a cluster at a range of given values of rCut.

	:param cluster: This is the cluster to obtain the CNA profile of.
	:type  cluster: Either Cluster or ase.Atoms
	:param rCuts: The range of values of rCuts to obtain the CNA profile of.
	:type  rCuts: float

	:returns: This resutrn the name of the cluster, and the atomic_CNA_profiles. 
	:rtype:   (int, Counter)
	'''
	cluster, rCuts = input_data
	system = cluster
	manager = mp.Manager()

	counter = 0
	max_task_execution = 80
	CNA_profile = []
	while counter < len(rCuts):
		ind_start = counter
		ind_end   = ind_start + max_task_execution
		if counter > len(rCuts):
			counter = len(rCuts)
		tasks = get_tasks(system, rCuts[ind_start:ind_end])
		return_list = manager.list()
		for task in tasks:
			p = mp.Process(target=get_atomic_CNA_profile, args=(task,return_list))
			p.run()
		counter += max_task_execution
		CNA_profile += list(return_list)
	return (system.name,CNA_profile)

#############################################################################################

def get_CNA_similarity(cluster_1_CNA,cluster_2_CNA,total_no_of_atoms):
	'''
	Get the similarity for the two clusters at a particular value of rCut.

	:param cluster_1_CNA: the CNA profile of cluster 1 at rCut
	:type  cluster_1_CNA: asap3.analysis.localstructure.FullCNA
	:param cluster_2_CNA: the CNA profile of cluster 2 at rCut
	:type  cluster_2_CNA: asap3.analysis.localstructure.FullCNA
	:param total_no_of_atoms: The total number of atoms in the cluster
	:type  total_no_of_atoms: int
	
	'''
	common_atom_signatures = (Counter(cluster_1_CNA) & Counter(cluster_2_CNA))
	total_no_common_atoms = sum(common_atom_signatures.values())
	similarity = float(total_no_common_atoms)/float(total_no_of_atoms)*100.0
	return similarity

def get_CNA_similarities(input_data):
	"""
	Get the full similarity profile of the two clusters.

	input_data contains two parameters

	:param name_1: Name of the first cluster
	:type  name_1: int
	:param name_2: Name of the second cluster
	:type  name_2: int
	:param cluster_1_CNA_profile: the full CNA profile of cluster 1 for all values of rCut.
	:type  cluster_1_CNA_profile: [asap3.analysis.localstructure.FullCNA ,...]
	:param cluster_2_CNA_profile: the full CNA profile of cluster 2 for all values of rCut.
	:type  cluster_2_CNA_profile: [asap3.analysis.localstructure.FullCNA ,...]

	:returns: returns the name of the two clusters, and the similarity profile.
	:rtype:   (int, int, list of float)

	"""
	name_1, name_2, cluster_1_CNA_profile, cluster_2_CNA_profile = input_data
	CNA_similarities = []
	if not sum(cluster_1_CNA_profile[0].values()) == sum(cluster_2_CNA_profile[0].values()):
		print('Error in def get_CNA_similarities, in AC_SRA_Methods.py')
		print('cluster_1_CNA_profile and cluster_2_CNA_profile are not the same size')
		print('They should be the same size as they should have been examined across the same rCut values.')
		print('len(cluster_1_CNA_profile) = '+str(len(cluster_1_CNA_profile)))
		print('len(cluster_2_CNA_profile) = '+str(len(cluster_2_CNA_profile)))
		print('Check this out.')
		import pdb; pdb.set_trace()
		exit()
	total_no_of_atoms = sum(cluster_1_CNA_profile[0].values())
	for index in range(len(cluster_1_CNA_profile)):
		cluster_1_CNA = cluster_1_CNA_profile[index]; cluster_2_CNA = cluster_2_CNA_profile[index]; 
		similarity = get_CNA_similarity(cluster_1_CNA,cluster_2_CNA,total_no_of_atoms)
		CNA_similarities.append(similarity)
	return name_1, name_2, CNA_similarities
