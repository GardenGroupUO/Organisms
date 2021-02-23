#!/usr/bin/python

import sys
import numpy as np

from asap3.Internal.BuiltinPotentials import Gupta
from asap3.Internal.BuiltinPotentials import LennardJones

from make_energy_vs_similarity_results_Main_Programs.processing_methods import processing_genetic_algorithm_data
from make_energy_vs_similarity_results_Main_Programs.plotting_methods   import plotting_genetic_algorithm_data


data_path = sys.argv[1]
gm_min_XYZ = sys.argv[2]
cluster_type = sys.argv[3]
energy_of_global_minimum = float(sys.argv[4])
energy_decimal_places = int(sys.argv[5])

lattice_constant =  4.07
r0 = lattice_constant/((2.0)**(0.5))
Gupta_parameters = {'Au': [10.53, 4.30, 0.2197, 1.855, r0]}
cutoff = 1000 # This is usually set to 
rCut = 1000
delta = 0.15
#calculator = Gupta(Gupta_parameters, cutoff=cutoff, delta=delta,debug=False)
elements = [10]; sigma = [1]; epsilon = [1];
calculator = LennardJones(elements, epsilon, sigma, rCut=rCut, modified=True)

def get_rCuts():
	second_nn = round(lattice_constant,4)
	first_nn = round(lattice_constant/(2.0**0.5),4)
	diff = second_nn - first_nn
	rCut_low = first_nn + (1.0/3.0)*diff
	rCut_high = first_nn + (2.0/3.0)*diff
	rCuts = np.linspace(rCut_low,rCut_high,78,endpoint=True)
	for index in range(len(rCuts)):
		rCuts[index] = round(rCuts[index],4)
	return rCuts
rCuts = get_rCuts()
print('rCuts: '+str(rCuts))


def make_file():
	LJ_gm_cluster = Atoms()
	with open(LJ_gm_minTXT,'r') as LJ_positions:
		for line in LJ_positions:
			xx, yy, zz = line.rstrip().split()
			atom = Atom(symbol='Au', position=(xx, yy, zz))
			LJ_gm_cluster.append(atom)







cluster_to_compare_against = ?
calculator = ?
rCuts,energy_of_global_minimum,energy_decimal_places
all_similarities, all_energies, all_generations = processing_genetic_algorithm_data(path_to_ga_trial, cluster_to_compare_against)
exit()
plotting_genetic_algorithm_data(path_to_ga_trial, all_similarities, all_energies, all_generations)





