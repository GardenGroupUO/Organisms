import time
from copy import deepcopy
from asap3.Internal.BuiltinPotentials import Gupta
from ase.optimize import FIRE

def Minimisation_Function(cluster,collection,cluster_name):
	#######################################################################################
	cluster.pbc = False # make sure that the periodic boundry conditions are set off
	#######################################################################################
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
			errorMessage = 'The optimisation of cluster ' + str(cluster_name) + ' did not optimise completely.'
			print(errorMessage, file=sys.stderr)
			print(errorMessage)
	except:
		print('Local Optimiser Failed for some reason.')
	endTime = time.time()
	####################################################################################################################
	# Write information about the algorithm
	Info = {}
	Info["INFO.txt"] = ''
	Info["INFO.txt"] += ("No of Force Calls: " + str(dyn.get_number_of_steps()) + '\n')
	Info["INFO.txt"] += ("Time (s): " + str(endTime - startTime) + '\n')
	#Info["INFO.txt"] += ("Cluster converged?: " + str(dyn.converged()) + '\n')
	####################################################################################################################
	return cluster, converged, Info