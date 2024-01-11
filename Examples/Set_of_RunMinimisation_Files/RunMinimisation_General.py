import time
from subprocess import Popen

def Minimisation_Function(cluster,collection,cluster_name):
	#######################################################################################
	cluster.pbc = What_you_want # make sure that the periodic boundry conditions are set off
	#######################################################################################
	# Perform the local optimisation method on the cluster.
	startTime = time.time();
	#Pre-calculation
	try:
		Popen(['run','external','program'])
	except Exception:
		print('Local Optimiser Failed for some reason.')
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