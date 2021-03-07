from ase.io import read
from Organisms import make_energy_vs_similarity_results

# ===========================================================================================================
# Information for processing data
#
# The path to where the genetic algorithm was run from (the directory where Run.py is found). 
path_to_ga_trial = '.' 
# The rCut value for the common neighbour analysis, in units of Angstroms
rCut = 1.355 # Angstroms
# The ase.Atoms object of the cluster to compare all clusters from the genetic algorithm to. 
# In this example, we are comparing all clusters to the LJ98 global minimum.
clusters_to_compare_against = read('LJ98_GM.xyz')
# This is the calculator used to initially locally minimise ONLY the clusters_to_compare_against cluster 
# just to make sure this cluster is a local minimum. 
elements = [10]; epsilon = [1]; sigma = [1]; rCut = 1000
calculator = LennardJones(elements, epsilon, sigma, rCut=rCut, modified=True)
# ===========================================================================================================

# ===========================================================================================================
# Information for plotting data
#
# This setting will create plots that plot the energy vs similarity over generations, including generation plots of the eras between epoches. 
# This setting requires process_over_generations = True to be used.
make_epoch_plots = True
# This setting will create a video that shows how clusters were created per generations. 
# This setting requires process_over_generations = True to be used.
get_animations = True
# This setting will create a video that shows only the energies and similarities of clusters in the population over generation. 
# This setting requires process_over_generations = True to be used.
get_animations_do_not_include_offspring = True
# This setting will indicate if you want to make svg files along with the png files that are made during this program
make_svg_files = False
# place all these settings into the plotting_settings dictionary. 
plotting_settings = {'make_epoch_plots': make_epoch_plots, 'get_animations': get_animations, 'get_animations_do_not_include_offspring': get_animations_do_not_include_offspring, 'make_svg_files': make_svg_files}
# ===========================================================================================================

# ===========================================================================================================
# Run the make_energy_vs_similarity_results program
make_energy_vs_similarity_results(path_to_ga_trial, rCut, clusters_to_compare_against, calculator, plotting_settings=plotting_settings)
# ===========================================================================================================