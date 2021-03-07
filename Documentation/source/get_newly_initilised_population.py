from Organisms import GetNewlyInitilisedPopulation
###############################################################################################################################################
cluster_makeup = {"Cu": 37}
from RunMinimisation import Minimisation_Function
nPool = 30
r_ij = 3.4
vacuumAdd = 10.0
###############################################################################################################################################
# This switch tells the genetic algorithm the type of diversity scheme they want to place on the genetic algoithm.
lc = 2.556
first_nn = lc; second_nn = (2.0**0.5)*lc; diff = second_nn - first_nn
rCut_low = first_nn + (1.0/3.0)*diff; rCut_low = round(rCut_low,1)
rCut_high = first_nn + (2.0/3.0)*diff; rCut_high = round(rCut_high,1) - 0.1
rCut_resolution = 0.1
CNA_contribution = 0.0
#Diversity_Information = {'Diversity_Switch':'Off'}
#Diversity_Information = {'Diversity_Switch':'Energy Diversity', 'energy_diversity_mode': 'simple', 'round_energy': 2}
#Diversity_Information = {'Diversity_Switch':'Energy Diversity', 'energy_diversity_mode': 'comprehensive', 'minimum_energy_diff': 0.025}
Diversity_Information = {'Diversity_Switch':'AC-SRA','rCut_low':rCut_low,'rCut_high':rCut_high,'rCut_resolution':rCut_resolution,'CNA_contribution':CNA_contribution} 
###############################################################################################################################################
rounding_criteria = 10
folder_with_user_created_clusters = None #'User_Clusters'
###############################################################################################################################################
GetNewlyInitilisedPopulation(nPool,cluster_makeup,r_ij,vacuumAdd,Minimisation_Function,Diversity_Information,rounding_criteria,folder_with_user_created_clusters)
###############################################################################################################################################