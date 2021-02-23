import sys
import numpy as np
#from check_LJ_Sims_Get_results_v3 import get_data
#from check_LJ_Sims_Process_results_v4 import process_data
from check_Sims_Get_results_v2 import get_data
from check_Sims_Process_results_v2 import process_data
from asap3.Internal.BuiltinPotentials import Gupta
from asap3.Internal.BuiltinPotentials import LennardJones
#python run_birdpoo_plotter.py Population GM.xyz LJ -543.67 2

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

get_data(data_path,gm_min_XYZ,cluster_type,calculator,rCuts,energy_of_global_minimum,energy_decimal_places)
process_data(data_path,gm_min_XYZ,cluster_type,calculator,rCuts,energy_of_global_minimum,energy_decimal_places)
#get_data(data_path,gm_min_XYZ,cluster_type)
#process_data(data_path,gm_min_XYZ,cluster_type)
