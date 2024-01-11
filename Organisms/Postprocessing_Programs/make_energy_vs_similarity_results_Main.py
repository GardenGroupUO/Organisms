# ------------------------------------------------------------------------------------------------------------------------- %
# Initialise make_energy_ver_similarity_results program.
def check_plotting_settings(process_over_generations,get_animations):
	if process_over_generations == False and get_animations == True:
		print('Error using the make_energy_vs_similatity_results program')
		print('If you want to created animated plots of your genetic algorithm over generations, you need to set:')
		print('   * process_over_generations = True')
		print('Check your plotting settings')
		print()
		print('   * process_over_generations: '+str(process_over_generations))
		print('   * get_animations: '+str(get_animations))
		print()
		print('Check your settings and then try again.')
		print()
		print('This program will finish without completing.')
		exit()	

def make_dir(folder_path):
	if not os.path.exists(folder_path):
		os.mkdir(folder_path)

# ------------------------------------------------------------------------------------------------------------------------- %
# Minimise cluster if so desired
from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.data_from_genetic_algorithm_methods import minimise_cluster as minimise_cluster_function
def minimise_cluster(cluster_to_compare_against,calculator):
	cluster_to_compare_against = minimise_cluster_function(cluster_to_compare_against,calculator)
	return cluster_to_compare_against

# ------------------------------------------------------------------------------------------------------------------------- %
# Processing Data
import os 
from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.processing_methods import get_filenames
from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.processing_methods import get_energy_and_CNA_profile_data_from_GA_Recording_Database, check_energy_and_CNA_profile_data_in_file
from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.processing_methods import get_similarity_data, check_similarity_data_in_file
def processing_genetic_algorithm_data(path_to_ga_trial,rCut,clusters_to_compare_against,folder_path,no_of_cpus=1):
	print('-----------------------------------------------------------------------------------------------------------')
	print('Getting energy and similarity data from the GA_Recording_Database')
	# process energy and CNA Profile data from the GA_Recording_Database
	energy_and_GA_data_filename, CNA_Profile_data_filename, databaseDB_filename = get_filenames(path_to_ga_trial)
	no_issues,next_cluster_line_counter_energy_and_GA=check_energy_and_CNA_profile_data_in_file(energy_and_GA_data_filename, CNA_Profile_data_filename)
	get_energy_and_CNA_profile_data_from_GA_Recording_Database(energy_and_GA_data_filename,CNA_Profile_data_filename,databaseDB_filename,rCut,no_issues=no_issues,start_from=next_cluster_line_counter_energy_and_GA,no_of_cpus=no_of_cpus)
	# process similarity data from the GA_Recording_Database
	for index in range(len(clusters_to_compare_against)):
		cluster_to_compare_against = clusters_to_compare_against[index]
		cluster_to_compare_number = index+1
		similarity_data_filename = folder_path+'/similarity_data_cluster_'+str(cluster_to_compare_number)+'.txt'
		no_issues, next_cluster_line_counter_similarity = check_similarity_data_in_file(similarity_data_filename)
		get_similarity_data(path_to_ga_trial,cluster_to_compare_against,rCut,similarity_data_filename,no_issues=no_issues,start_from=next_cluster_line_counter_similarity)

# ------------------------------------------------------------------------------------------------------------------------- %
# Place data in memory
from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.processing_methods import get_energy_and_CNA_profile_data_from_file
from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.processing_methods import get_similarity_data_from_file
def place_genetic_algorithm_data_in_memory(path_to_ga_trial, clusters_to_compare_against, folder_path):
	print('-----------------------------------------------------------------------------------------------------------')
	print('Getting data from the GA about clusters in the population and offspring over generation')
	energy_and_ga_data = get_energy_and_CNA_profile_data_from_file(path_to_ga_trial)
	similarity_data = []
	for cluster_number in range(1,len(clusters_to_compare_against)+1):
		similarity_data_filename = folder_path+'/similarity_data_cluster_'+str(cluster_number)+'.txt'
		similarity_datum = get_similarity_data_from_file(similarity_data_filename,cluster_number)
		similarity_data.append(similarity_datum)
	print('-----------------------------------------------------------------------------------------------------------')
	return energy_and_ga_data, similarity_data

# ------------------------------------------------------------------------------------------------------------------------- %
# Further process data from files
from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.processing_methods import get_information_about_when_clusters_were_created_during_the_GA
def process_genetic_algorithm_data_in_memory_into_other_pieces_of_data(path_to_ga_trial, energy_and_ga_data, similarity_datum):
	print('-----------------------------------------------------------------------------------------------------------')
	plotting_datum = get_information_about_when_clusters_were_created_during_the_GA(path_to_ga_trial,energy_and_ga_data,similarity_datum)
	print('-----------------------------------------------------------------------------------------------------------')
	return plotting_datum

# ------------------------------------------------------------------------------------------------------------------------- %
# Plotting Data
from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.plotting_methods import make_energy_vs_similatity_plot_without_generations
def plotting_genetic_algorithm_data(cluster_folder_path, energy_and_ga_data, similarity_datum, name_cluster, make_svg_files, energy_units='eV'):
	print('-----------------------------------------------------------------------------------------------------------')
	print('Make energy vs similarity plots that do not involve generations')
	make_energy_vs_similatity_plot_without_generations(cluster_folder_path, energy_and_ga_data, similarity_datum, name_cluster, make_svg_files, energy_units=energy_units)
	print('-----------------------------------------------------------------------------------------------------------')

from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.plotting_methods import get_plots_for_each_epoch
def plotting_genetic_algorithm_data_over_generations(cluster_folder_path, plotting_datum, name_cluster, make_svg_files, energy_units='eV'):
	print('-----------------------------------------------------------------------------------------------------------')
	print('Make energy vs similarity plots that do involve generations. These include separate epoch plots.')
	all_similarities, all_energies, all_generations, populations_Per_generation, offspring_Per_generation, restart_gens, between_restart_gens, runs_between_epochs = plotting_datum
	get_plots_for_each_epoch(populations_Per_generation, restart_gens, cluster_folder_path, 'plotting_data_cluster_'+str(name_cluster), make_svg_files, energy_units=energy_units)
	print('-----------------------------------------------------------------------------------------------------------')

from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.plotting_methods import perform_animations
def make_animations(cluster_folder_path, plotting_datum, name_cluster, gps=1, max_time=None, label_generation_no=False, label_no_of_epochs=False, energy_units='eV'):
	print('-----------------------------------------------------------------------------------------------------------')
	print('Making animated energy vs similarity plots of the population and offspring over generations')
	all_similarities, all_energies, all_generations, populations_Per_generation, offspring_Per_generation, restart_gens, between_restart_gens, runs_between_epochs = plotting_datum
	if label_generation_no:
		label_generation_no = restart_gens
	if label_no_of_epochs:
		label_no_of_epochs = restart_gens
	perform_animations(populations_Per_generation, offspring_Per_generation, cluster_folder_path, gps=gps, max_time=max_time, label_generation_no=label_generation_no, label_no_of_epochs=label_no_of_epochs, energy_units=energy_units)
	print('-----------------------------------------------------------------------------------------------------------')

from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results_Main_Programs.plotting_methods import perform_animations_no_offspring
def make_animations_no_offspring(cluster_folder_path, plotting_datum, name_cluster, gps=1, max_time=None, label_generation_no=False, label_no_of_epochs=False, energy_units='eV'):
	print('-----------------------------------------------------------------------------------------------------------')
	print('Making animated energy vs similarity plots of the population over generations. Offspring are not included in this animation')
	all_similarities, all_energies, all_generations, populations_Per_generation, offspring_Per_generation, restart_gens, between_restart_gens, runs_between_epochs = plotting_datum
	if label_generation_no:
		label_generation_no = restart_gens
	if label_no_of_epochs:
		label_no_of_epochs = restart_gens
	perform_animations_no_offspring(populations_Per_generation, cluster_folder_path, gps=gps, max_time=max_time, label_generation_no=label_generation_no, label_no_of_epochs=label_no_of_epochs, energy_units=energy_units)
	print('-----------------------------------------------------------------------------------------------------------')

# ------------------------------------------------------------------------------------------------------------------------- %
# Setting up the plotting setting for this program
def get_setting(plotting_settings,key,default_value):
	return plotting_settings.setdefault(key,default_value)

def get_plotting_settings(plotting_settings):
	#process_over_generations = get_setting(plotting_settings,'process_over_generations',False)
	make_epoch_plots = get_setting(plotting_settings,'make_epoch_plots',False)
	get_animations = get_setting(plotting_settings,'get_animations',False)
	get_animations_do_not_include_offspring = get_setting(plotting_settings,'get_animations_do_not_include_offspring',False)
	make_svg_files = get_setting(plotting_settings,'make_svg_files',False)
	gps = get_setting(plotting_settings,'gps',1)
	max_time = get_setting(plotting_settings,'max_time',None)
	label_generation_no = get_setting(plotting_settings,'label_generation_no',False)
	label_no_of_epochs = get_setting(plotting_settings,'label_no_of_epochs',False)
	energy_units = get_setting(plotting_settings,'energy_units','eV')
	return make_epoch_plots, get_animations, get_animations_do_not_include_offspring, make_svg_files, gps, max_time, label_generation_no, label_no_of_epochs, energy_units

# ------------------------------------------------------------------------------------------------------------------------- %
# Processing the data
def make_energy_vs_similarity_results_Main(path_to_ga_trial, rCut, clusters_to_compare_against, calculator=None, no_of_cpus=1, plotting_settings={}):
	# Get the plotting setting for this program
	make_epoch_plots, get_animations, get_animations_do_not_include_offspring, make_svg_files, gps, max_time, label_generation_no, label_no_of_epochs, energy_units = get_plotting_settings(plotting_settings)
	# make similarity folder to place data into
	folder_path = path_to_ga_trial+'/Similarity_Investigation_Data'
	make_dir(folder_path)
	# Processing data methods
	if not isinstance(clusters_to_compare_against,list):
		clusters_to_compare_against = [clusters_to_compare_against.copy()]
	clusters_to_compare_against_optimised = []
	for cluster_to_compare_against in clusters_to_compare_against:
		cluster_to_compare_against_optimised = minimise_cluster(cluster_to_compare_against, calculator)
		clusters_to_compare_against_optimised.append(cluster_to_compare_against_optimised)
	processing_genetic_algorithm_data(path_to_ga_trial, rCut, clusters_to_compare_against_optimised, folder_path, no_of_cpus)
	energy_and_ga_data, similarity_data = place_genetic_algorithm_data_in_memory(path_to_ga_trial, clusters_to_compare_against_optimised, folder_path)
	# plotting data methods
	for index in range(len(similarity_data)):
		ref_cluster_name = index+1	
		similarity_datum = similarity_data[index]
		cluster_folder_path = path_to_ga_trial+'/Similarity_Investigation_Data/Ref_Cluster_'+str(ref_cluster_name)
		make_dir(cluster_folder_path)
		plotting_genetic_algorithm_data(cluster_folder_path, energy_and_ga_data, similarity_datum, ref_cluster_name, make_svg_files, energy_units=energy_units)
		if any([make_epoch_plots,get_animations,get_animations_do_not_include_offspring]):
			plotting_datum = process_genetic_algorithm_data_in_memory_into_other_pieces_of_data(path_to_ga_trial, energy_and_ga_data, similarity_datum)
			if make_epoch_plots:
				plotting_genetic_algorithm_data_over_generations(cluster_folder_path, plotting_datum, ref_cluster_name, make_svg_files, energy_units=energy_units)
			if get_animations_do_not_include_offspring:
				make_animations_no_offspring(cluster_folder_path, plotting_datum, ref_cluster_name, gps=gps, max_time=max_time, label_generation_no=label_generation_no, label_no_of_epochs=label_no_of_epochs, energy_units=energy_units)
			if get_animations:
				make_animations(cluster_folder_path, plotting_datum, ref_cluster_name, gps=gps, max_time=max_time, label_generation_no=label_generation_no, label_no_of_epochs=label_no_of_epochs, energy_units=energy_units)
