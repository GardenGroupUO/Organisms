'''
AC_SRA_Methods.py, Geoffrey Weal, 20/11/2018

This script is designed to include all the methods for performing structural recognition 
task in terms of the Atom Comparison version of the Structural Recognition Algorithm.

'''

from asap3.analysis.localstructure import FullCNA
from collections import Counter
import sys
import multiprocessing as mp

#############################################################################################

def get_total_CNA_profile(input_data, return_list):
	(system,rCut) = input_data
	fullCNA_atoms = FullCNA(system,rCut)
	_,total_CNA_profile = fullCNA_atoms.get_normal_and_total_cna()
	#return Counter(total_CNA_profile)
	return_list.append(Counter(total_CNA_profile))

def get_tasks(system, rCuts):
	for rCut in rCuts:
		yield (system,rCut)

def get_CNA_profile(cluster, rCuts):
	'''
	This def will return the CNA profile of a cluster at a range of given values of rCut.

	:param cluster: This is the cluster to obtain the CNA profile of.
	:type  cluster: Either Cluster or ase.Atoms
	:param rCuts: The range of values of rCuts to obtain the CNA profile of.
	:type  rCuts: float

	'''
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
			p = mp.Process(target=get_total_CNA_profile, args=(task,return_list))
			p.run()
		counter += max_task_execution
		CNA_profile += list(return_list)
	return CNA_profile

#############################################################################################

def get_CNA_similarity(cluster_1_CNA,cluster_2_CNA):
	'''
	Get the similarity for the two clusters at a particular value of rCut.

	:param cluster_1_CNA: the CNA profile of cluster 1 at rCut
	:type  cluster_1_CNA: asap3.analysis.localstructure.FullCNA
	:param cluster_2_CNA: the CNA profile of cluster 2 at rCut
	:type  cluster_2_CNA: asap3.analysis.localstructure.FullCNA
	:param total_no_of_atoms: The total number of atoms in the cluster
	:type  total_no_of_atoms: int

	'''
	tc_1_at_one_rCut = Counter(cluster_1_CNA)
	tc_2_at_one_rCut = Counter(cluster_2_CNA)

	total_CNA_signatures_in_common = tc_1_at_one_rCut & tc_2_at_one_rCut
	Union_of_total_CNAs = tc_1_at_one_rCut | tc_2_at_one_rCut

	sum_all_total_CNA_signatures_in_common = sum(total_CNA_signatures_in_common.values())
	sum_all_Union_of_total_CNAs = sum(Union_of_total_CNAs.values())
	try:
		similarity = (float(sum_all_total_CNA_signatures_in_common)/float(sum_all_Union_of_total_CNAs))*100.0
	except ZeroDivisionError as error:
		error_message = '\n'
		error_message += '--------------------------------------------------------'+'\n'
		error_message += 'Error in def get_CNA_similarity, in TC_SCM_Methods.py'+'\n'
		error_message += 'Recieved the following error'+'\n'
		error_message += str(error)+'\n'
		error_message += 'The general problem that causes this to occur is that one or more rCut values that are being assessed are to low.'+'\n'
		error_message += 'This means that the CNA/SCM finds no pairs of atoms full stop throughout a cluster, thus giving a zero division error.'+'\n'
		error_message += 'Check this out'+'\n'
		error_message += 'Note: if you are happy with this issue however, you can replace the "raise ZeroDivisionError(error_message) from error" line of code with "print(error_message)" to only give this message and not exit this program in def get_CNA_similarity, in TC_SCM_Methods.py'+'\n'
		#error_message += '--------------------------------------------------------'+'\n'
		#print(error_message)
		error_message += 'As this a issue, the GA will finish without completing.'+'\n'
		error_message += '--------------------------------------------------------'+'\n'
		raise ZeroDivisionError(error_message) from error
	return similarity

def get_CNA_similarities(cluster_1_CNA_profile, cluster_2_CNA_profile):
	"""
	Get the full similarity profile of the two clusters.

	:param cluster_1_CNA_profile: the full CNA profile of cluster 1 for all values of rCut.
	:type  cluster_1_CNA_profile: [asap3.analysis.localstructure.FullCNA ,...]
	:param cluster_2_CNA_profile: the full CNA profile of cluster 2 for all values of rCut.
	:type  cluster_2_CNA_profile: [asap3.analysis.localstructure.FullCNA ,...]

	"""
	CNA_similarities = []
	for index in range(len(cluster_1_CNA_profile)):
		cluster_1_CNA = cluster_1_CNA_profile[index]; cluster_2_CNA = cluster_2_CNA_profile[index]; 
		similarity = get_CNA_similarity(cluster_1_CNA,cluster_2_CNA)
		CNA_similarities.append(similarity)
	return CNA_similarities
