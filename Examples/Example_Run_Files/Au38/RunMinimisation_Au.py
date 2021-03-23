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
	#######################################################################################
	cluster.pbc = False # make sure that the periodic boundry conditions are set off
	#######################################################################################
	# Perform the local optimisation method on the cluster.
	# Parameter sequence: [p, q, a, xi, r0]
	#
	# RGL parameters below from:
	# Crossover among structural motifs in transition and noble-metal clusters
	# F. Baletto, R. Ferrando, A. Fortunelli, F. Montalenti and C. Mottet, J. Chem. Phys., 2002, 116, 3856–3863.
	# https://doi.org/10.1063/1.1448484
	r0 = 4.07/(2.0**0.5)
	Gupta_parameters = {'Au': [10.53, 4.30, 0.2197, 1.855, r0]}
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
	except BaseException:
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
