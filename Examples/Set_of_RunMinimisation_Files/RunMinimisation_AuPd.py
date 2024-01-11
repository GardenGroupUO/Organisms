'''
RunMinimisation.py, GRW, 8/6/17
 
This python program is designed to input the POSCAR file and use it
with Atomic Simulation Environment (ASE) to minimise the given structure
using an empirical potential.
 
The program will take the output translate it into a OUTCAR file which
the bpga will use.
 
Required inputs: BeforeOpt
Required to outputs: AfterOpt.traj, INFO.txt
Other outputs: Trajectory file.
 
'''
import sys
import time
from asap3.Internal.BuiltinPotentials import Gupta
from ase.optimize import FIRE

def Minimisation_Function(cluster,collection,cluster_name):
	####################################################################################################################
	cluster.pbc = False
	####################################################################################################################
	# Perform the local optimisation method on the cluster.
	# Parameter sequence: [p, q, a, xi, r0]
	#Gupta_parameters = {'Au': [10.529999999999999, 4.2999999999999998, 0.21970000000000001, 1.855, 2.8779245994292486]}
	Gupta_parameters = {'Pd': [10.867, 3.742, 0.1746, 1.718, 2.7485], 'Au': [10.229, 4.036, 0.2061, 1.79, 2.884], ('Au','Pd'): [10.54, 3.89, 0.19, 1.75, 2.816]}
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
	except Exception:
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
