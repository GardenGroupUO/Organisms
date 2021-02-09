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
from ase import Atom, Atoms
from ase.io import read as ase_read
from ase.io import write as ase_write
#from ase.calculators.lj import LennardJones
import time
from ase.data import atomic_numbers
from asap3.Internal.BuiltinPotentials import LennardJones
from ase.optimize import BFGS, FIRE
import sys
 
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
	rCut = 1000
	#sigma = 1; epsilon = 1; lj_calc = LennardJones(sigma=sigma, epsilon=epsilon,rc=rCut)
	elements = [atomic_numbers[cluster[0].symbol]]; sigma = [1]; epsilon = [1]; 
	lj_calc = LennardJones(elements, epsilon, sigma, rCut=rCut, modified=True)
	cluster.set_calculator(lj_calc)
	dyn = FIRE(cluster,logfile=None)
	startTime = time.time(); converged = False
	try:
		dyn.run(fmax=0.01,steps=5000)
		converged = dyn.converged()
		if not converged:
			import os
			name = os.path.basename(os.getcwd())
			errorMessage = 'The optimisation of cluster ' + name + ' did not optimise completely.'
			print(errorMessage, file=sys.stderr)
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
