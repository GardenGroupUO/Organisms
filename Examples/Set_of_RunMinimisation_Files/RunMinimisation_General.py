import time
from copy import deepcopy
from asap3.Internal.BuiltinPotentials import Gupta
from ase.optimize import FIRE
from subprocess import Popen

def Minimisation_Function(cluster,collection,cluster_name):
	#######################################################################################
	cluster.pbc = What_you_want # make sure that the periodic boundry conditions are set off
	#######################################################################################
	# Perform the local optimisation method on the cluster.
	startTime = time.time();
	#Pre-calculation
	Popen(['run','external','program'])
	#Post-calculation
	endTime = time.time()
	####################################################################################################################
	# Write information about the algorithm
	Info = {}
	Info["INFO.txt"] = ''
	Info["INFO.txt"] += ("No of Force Calls: " + str(number_of_force_calls) + '\n')
	Info["INFO.txt"] += ("Time (s): " + str(endTime - startTime) + '\n')
	#Info["INFO.txt"] += ("Cluster converged?: " + str(dyn.converged()) + '\n')
	####################################################################################################################
	return cluster, converged, Info