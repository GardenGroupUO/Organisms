####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################

from ase import Atom, Atoms
from ase.io import read as ase_read
from ase.io import write as ase_write
from asap3.Internal.BuiltinPotentials import Gupta
from ase.optimize import BFGS, FIRE
import sys
import time
 
from ase.visualize import view

def Minimisation_Function(cluster,collection,cluster_dir):
	####################################################################################################################
	# Read the BeforeOpt file and record the elements, the
	# number of each element in the cluster and their positions
	#cluster = ase_read("BeforeOpt",format='vasp')
	cluster.pbc = False
	####################################################################################################################
	#Construct atoms using the ASE class "Atoms".
	####################################################################################################################
	# Perform the local optimisation method on the cluster.
	# Parameter sequence: [p, q, a, xi, r0]
	Gupta_parameters = {'Cu': [10.960, 2.2780, 0.0855, 1.224, 2.556]}
	cluster.set_calculator(Gupta(Gupta_parameters, cutoff=1000, debug=False))
	dyn = FIRE(cluster,logfile=None)
	startTime = time.time(); converged = False
	try:
		dyn.run(fmax=0.01,steps=5000)
		converged = dyn.converged()
		if not converged:
			import os
			name = os.path.basename(os.getcwd())
			errorMessage = 'The optimisation of cluster ' + name + ' did not optimise completely.'
			#print sys.stderr >> errorMessage
			print(errorMessage)
	except:
		print('Local Optimiser Failed for some reason.')
	endTime = time.time()
	#ase_write('AfterOpt.traj',cluster)
	####################################################################################################################
	# Write information about the algorithm
	Info = {}
	Info["INFO.txt"] = ''
	Info["INFO.txt"] += ("No of Force Calls: " + str(dyn.get_number_of_steps()) + '\n')
	Info["INFO.txt"] += ("Time (s): " + str(endTime - startTime) + '\n')
	#Info.write("Cluster converged?: " + str(dyn.converged()) + '\n')
	####################################################################################################################
	return cluster, converged, Info

####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################

from ase.io import read
from ase import Atom, Atoms
import numpy as np

from asap3.analysis.localstructure import FullCNA
from collections import Counter
import sys
import multiprocessing as mp

#############################################################################################

def get_total_CNA_profile(input_data, return_list):
	(system,rCut) = input_data
	fullCNA_atoms = FullCNA(system,rCut)
	_,total_CNA_profile = fullCNA_atoms.get_normal_and_total_cna()
	return_list.append(Counter(total_CNA_profile))

def get_CNA_profile(input_data):
	'''
	This def will return the CNA profile of a cluster at a range of given values of rCut.

	:param cluster: This is the cluster to obtain the CNA profile of.
	:type  cluster: Either Cluster or ase.Atoms
	:param rCuts: The range of values of rCuts to obtain the CNA profile of.
	:type  rCuts: float

	'''
	cluster, rCuts = input_data
	system = cluster
	counter = 0
	added = 80
	CNA_profile = []
	while counter < len(rCuts):
		ind_start = counter
		ind_end   = ind_start + added
		if counter > len(rCuts):
			counter = len(rCuts)
		print(ind_start)
		tasks = [(system, rCut) for rCut in rCuts[ind_start:ind_end]]
		manager = mp.Manager()
		return_list = manager.list()
		for task in tasks:
			p = mp.Process(target=get_total_CNA_profile, args=(task,return_list))
			p.run()
		counter += added
		CNA_profile += list(return_list)
	return (system.name,CNA_profile)

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

	similarity = (float(sum_all_total_CNA_signatures_in_common)/float(sum_all_Union_of_total_CNAs))*100.0
	return similarity

def get_CNA_similarities(input_data):
	"""
	Get the full similarity profile of the two clusters.

	:param cluster_1_CNA_profile: the full CNA profile of cluster 1 for all values of rCut.
	:type  cluster_1_CNA_profile: [asap3.analysis.localstructure.FullCNA ,...]
	:param cluster_2_CNA_profile: the full CNA profile of cluster 2 for all values of rCut.
	:type  cluster_2_CNA_profile: [asap3.analysis.localstructure.FullCNA ,...]

	"""
	name_1, name_2, cluster_1_CNA_profile, cluster_2_CNA_profile = input_data
	CNA_similarities = []
	for index in range(len(cluster_1_CNA_profile)):
		cluster_1_CNA = cluster_1_CNA_profile[index]; cluster_2_CNA = cluster_2_CNA_profile[index]; 
		similarity = get_CNA_similarity(cluster_1_CNA,cluster_2_CNA)
		CNA_similarities.append(similarity)
	return name_1, name_2, CNA_similarities

#############################################################################################

def get_cluster(name):
	cluster = read(name)
	cluster_new = Atoms()
	for atom in cluster:
		xx = atom.x
		yy = atom.y
		zz = atom.z
		symbol = atom.symbol
		new_atom = Atom(symbol,(xx,yy,zz))
		cluster_new.append(new_atom)
	cluster_new.name = name
	cluster_new.set_cell((10,10,10))
	return cluster_new

####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################

import matplotlib.pyplot as plt
def make_plot(rCuts, CNA_similarities,r_low,r_high):
	plt.scatter(rCuts, CNA_similarities, s=9)
	x_diff = r_high - r_low
	x_axis_1 = r_low + x_diff*0.25
	x_axis_2 = r_low + x_diff*0.50
	x_axis_3 = r_low + x_diff*0.75
	ticks = [r_low,x_axis_1,x_axis_2,x_axis_3,r_high]
	labels = ['1','1.25','1.5','1.75','2']
	xlim_diff = 0.025
	plt.xlim([r_low - xlim_diff*x_diff,r_high + xlim_diff*x_diff])
	plt.xticks(ticks, labels, fontsize=16)
	plt.xlabel('$r_{cut}$ (units of nearest neighbour)',fontsize=18)
	plt.ylim([2,102])
	plt.yticks(range(0,101,20), fontsize=16)
	plt.ylabel('Similarity (%)',fontsize=18)
	plt.tight_layout()
	plt.savefig('CNA_plot_over_rCut.png')
	#plt.savefig('CNA_plot_over_rCut.eps')
	plt.savefig('CNA_plot_over_rCut.svg')

####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################

cluster_1 = get_cluster('1149.xyz')
cluster_2 = get_cluster('2619.xyz')
Gupta_parameters = {'Cu': [10.960, 2.2780, 0.0855, 1.224, 2.556]}
cluster_1.set_calculator(Gupta(Gupta_parameters, cutoff=1000, debug=False))
cluster_1.get_potential_energy()
cluster_2.set_calculator(Gupta(Gupta_parameters, cutoff=1000, debug=False))
cluster_2.get_potential_energy()

lattice_constant = 3.62
r_eq = lattice_constant/(2.0**0.5)

r_high = lattice_constant
r_low = r_eq
r_nums = 1000

rCuts = np.linspace(r_low,r_high,num=r_nums,endpoint=True)
name_1, cluster_1_CNA_profile = get_CNA_profile((cluster_1,rCuts))
name_2, cluster_2_CNA_profile = get_CNA_profile((cluster_2,rCuts))

task = (name_1,name_2,cluster_1_CNA_profile,cluster_2_CNA_profile)
name_1, name_2, CNA_similarities = get_CNA_similarities(task)

make_plot(rCuts,CNA_similarities,r_low,r_high)

#import pdb; pdb.set_trace()

#############################################################################################
