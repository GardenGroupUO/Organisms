from CheckInitilisedPopulationAgainstDiversitySchemes import CheckInitilisedPopulationAgainstDiversitySchemes
###############################################################################################################################################
name_to_initial_population_folder = 'Initialised_Population'
###############################################################################################################################################
cluster_makeup = {"Cu": 37}
from RunMinimisation import Minimisation_Function
nPool = 30
r_ij = 3.4
boxtoplaceinlength = 'default'
vacuumAdd = 10.0
###############################################################################################################################################
# This switch tells the genetic algorithm the type of diversity scheme they want to place on the genetic algoithm.
lc = 2.556
first_nn = lc; second_nn = (2.0**0.5)*lc; diff = second_nn - first_nn
rCut_low = first_nn + (1.0/3.0)*diff; rCut_low = round(rCut_low,1)
rCut_high = first_nn + (2.0/3.0)*diff; rCut_high = round(rCut_high,1) - 0.1
rCut_resolution = 0.05
CNA_contribution = 0.0
Diversity_Information_Off = {'Diversity_Switch':'Off'}
Diversity_Information_Simple_2dp = {'Diversity_Switch':'Energy Diversity', 'energy_diversity_mode': 'simple', 'round_energy': 2}
Diversity_Information_Simple_6dp = {'Diversity_Switch':'Energy Diversity', 'energy_diversity_mode': 'simple', 'round_energy': 6}
Diversity_Information_Comprehensive_2dp = {'Diversity_Switch':'Energy Diversity', 'energy_diversity_mode': 'comprehensive', 'minimum_energy_diff': (10.0)**(-2.0)}
Diversity_Information_Comprehensive_6dp = {'Diversity_Switch':'Energy Diversity', 'energy_diversity_mode': 'comprehensive', 'minimum_energy_diff': (10.0)**(-6.0)}
Diversity_Information_AC_SRA = {'Diversity_Switch':'AC-SRA','rCut_low':rCut_low,'rCut_high':rCut_high,'rCut_resolution':rCut_resolution,'CNA_contribution':CNA_contribution} 

list_of_Diversity_Information = []
list_of_Diversity_Information.append(Diversity_Information_Off)
list_of_Diversity_Information.append(Diversity_Information_Simple_2dp)
list_of_Diversity_Information.append(Diversity_Information_Simple_6dp)
list_of_Diversity_Information.append(Diversity_Information_Comprehensive_2dp)
list_of_Diversity_Information.append(Diversity_Information_Comprehensive_6dp)
list_of_Diversity_Information.append(Diversity_Information_AC_SRA)
###############################################################################################################################################
rounding_criteria = 10
###############################################################################################################################################
CheckInitilisedPopulationAgainstDiversitySchemes(name_to_initial_population_folder,nPool,cluster_makeup,r_ij,vacuumAdd,Minimisation_Function,list_of_Diversity_Information,rounding_criteria)
###############################################################################################################################################