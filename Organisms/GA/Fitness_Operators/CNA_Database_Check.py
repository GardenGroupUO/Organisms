from Organisms.GA.SCM_Scripts.SCM_initialisation import get_rCuts

def CNA_Database_Check(self,fitness_information, predation_operator):

	# perform checks to make sure that the cna_database is being used appropriately between the SCM predation operator and the structure + energy fitness operator. 
	# --------------------------------------------------- #
	if ('Use Predation Information' in fitness_information):
		self.use_predation_information = fitness_information['Use Predation Information']
	else:
		self.use_predation_information = False

	have_SCM_Scheme = ('SCM Scheme' in fitness_information)

	have_rCut_high = ('rCut_high' in fitness_information)
	have_rCut_low = ('rCut_low' in fitness_information)
	have_rCut_resolution = ('rCut_resolution' in fitness_information)
	have_rCut = ('rCut' in fitness_information)
	
	have_lattice_constant = ('lattice_constant' in fitness_information)
	have_nn_high = ('nn_high' in fitness_information)
	have_nn_low = ('nn_low' in fitness_information)
	have_nn_resolution = ('nn_resolution' in fitness_information)
	have_single_nn_measurement = ('single_nn_measurement' in fitness_information)

	have_settings = (have_SCM_Scheme,have_rCut_high,have_rCut_low,have_rCut_resolution,have_rCut,have_lattice_constant,have_nn_high,have_nn_low,have_nn_resolution,have_single_nn_measurement)
	
	# ----------------------------------------------------------------------------------------------------------------------------------------
	# You are using the SCM predation operator and use_predation_information == True, so this fitness operator should use the same cna_database as the predation operator
	if   (self.predation_switch == 'SCM')     and     self.use_predation_information:
		Checks_for_if_predation_switch_equals_SCM_predation_and_use_predation_information_is_true(self,fitness_information,have_settings)
		will_make_new_cna_database = False # use the same database as the SCM predation operator
	# You are using the SCM predation operator but use_predation_information == False, so this fitness operator should use its own cna_database 
	elif (self.predation_switch == 'SCM')     and not self.use_predation_information:
		Checks_for_if_predation_switch_equals_SCM_predation_or_use_predation_information_is_true(self,fitness_information,predation_operator,have_settings)
		will_make_new_cna_database = True # You want to have a new CNA database that only the structure + energy fitness operator uses.
	# You are not using the SCM predation operator but use_predation_information == True, these two conflict with eachother. Stop the program
	elif (not self.predation_switch == 'SCM') and     self.use_predation_information:
		print('ERROR in def SCM_options, in Class SCM_and_Energy_Fitness_Operator, in SCM_and_Energy_Fitness_Operator.py/SCM_and_Energy_Fitness_Operator_Options.py')
		print("You are not using the SCM operator, however you have set the 'Use Predation Information' switch in your fitness_information dictionary as True.")
		print("You can't use the same information from the Predation operator unless the SCM predation operator is used")
		print('Check this.')
		exit('This program will finish without completing.')
	# You are not using the SCM predation operator and use_predation_information == False, so this fitness operator should use its own cna_database 
	elif (not self.predation_switch == 'SCM') and not self.use_predation_information:
		Checks_for_if_predation_switch_equals_SCM_predation_or_use_predation_information_is_true(self,fitness_information,predation_operator,have_settings)
		will_make_new_cna_database = True # You want to have a new CNA database that only the structure + energy fitness operator uses.
	else:
		print('ERROR in def SCM_options, in Class SCM_and_Energy_Fitness_Operator, in SCM_and_Energy_Fitness_Operator.py/SCM_and_Energy_Fitness_Operator_Options.py')
		print('Something weird has happened because you should not have entered into this part of the code')
		exit('Weird error. Cancelling program before it begins. Check your inputs and possibly this code.')
	return will_make_new_cna_database
	# ----------------------------------------------------------------------------------------------------------------------------------------

def Checks_for_if_predation_switch_equals_SCM_predation_and_use_predation_information_is_true(self,fitness_information,have_settings):
	have_SCM_Scheme,have_rCut_high,have_rCut_low,have_rCut_resolution,have_rCut,have_lattice_constant,have_nn_high,have_nn_low,have_nn_resolution,have_single_nn_measurement = have_settings
	if (have_SCM_Scheme or have_rCut_high or have_rCut_low or have_rCut_resolution or have_rCut or have_lattice_constant or have_nn_high or have_nn_low or have_nn_resolution or have_single_nn_measurement):
		print('ERROR in def SCM_options, in Class SCM_and_Energy_Fitness_Operator, in SCM_and_Energy_Fitness_Operator.py/SCM_and_Energy_Fitness_Operator_Options.py')
		print("You are using the SCM operator and have set the 'Use Predation Information' switch in your fitness_information dictionary to True.")
		settings_to_mention = []
		names = ['SCM Scheme','rCut_high','rCut_low','rCut_resolution','rCut','lattice_constant','nn_high','nn_low','nn_resolution','single_nn_measurement']
		for name in names:
			if name in fitness_information:
				settings_to_mention.append(name)
		print('You have also included the following settings in the fitness_information dictionary: '+' '.join(settings_to_mention))
		print('For clarity of the input settings for future readers of your input, we require that if you use the SCM predation operator and set the "Use Predation Information" switch in your fitness_information dictionary to True')
		print('then do not include any of the following settings in your input fitness_information dictionary: '+' '.join(names))
		print()
		print('Your fitness_information dictionary is: '+str(fitness_information))
		print('Check this.')
		exit('This program will finish without completing.')

def Checks_for_if_predation_switch_equals_SCM_predation_or_use_predation_information_is_true(self,fitness_information,predation_operator,have_settings):
	have_SCM_Scheme,have_rCut_high,have_rCut_low,have_rCut_resolution,have_rCut,have_lattice_constant,have_nn_high,have_nn_low,have_nn_resolution,have_single_nn_measurement = have_settings
	if not 'SCM Scheme' in fitness_information:
		print('ERROR in def SCM_options, in Class SCM_and_Energy_Fitness_Operator, in SCM_and_Energy_Fitness_Operator.py/SCM_and_Energy_Fitness_Operator_Options.py')
		print('You need to include the "SCM Scheme" setting. This could be either the T-SCM or the A-SCM.')
		print('Your fitness_information dictionary is: '+str(fitness_information))
		print('Check this.')
		exit('This program will finish without completing.')
	have_all_settings_for_rCuts = (have_rCut_high and have_rCut_low and have_rCut_resolution)
	have_all_settings_for_rCut  = (have_rCut)
	have_all_settings_for_nns   = (have_lattice_constant and have_nn_high and have_nn_low and have_nn_resolution)
	have_all_settings_for_nn    = (have_lattice_constant and have_single_nn_measurement)
	one_of_settings_for_rCuts = (have_rCut_high or have_rCut_low or have_rCut_resolution)
	one_of_settings_for_rCut  = (have_rCut)
	one_of_settings_for_nns   = (have_nn_high or have_nn_low or have_nn_resolution)
	one_of_settings_for_nn    = (have_single_nn_measurement)
	if   have_all_settings_for_rCuts:
		if (one_of_settings_for_rCut or one_of_settings_for_nns or one_of_settings_for_nn or have_lattice_constant):
			multiple_settings_error(fitness_information); exit()
	elif have_all_settings_for_rCut:
		if (one_of_settings_for_rCuts or one_of_settings_for_nns or one_of_settings_for_nn or have_lattice_constant):
			multiple_settings_error(fitness_information); exit()
	elif have_all_settings_for_nns:
		if (one_of_settings_for_rCuts or one_of_settings_for_rCut or one_of_settings_for_nn):
			multiple_settings_error(fitness_information); exit()
	elif have_all_settings_for_nn:
		if (one_of_settings_for_rCuts or one_of_settings_for_rCut or one_of_settings_for_nns):
			multiple_settings_error(fitness_information); exit()
	else:
		print('ERROR in def SCM_options, in Class SCM_and_Energy_Fitness_Operator, in SCM_and_Energy_Fitness_Operator.py/SCM_and_Energy_Fitness_Operator_Options.py')
		print('You can only include one of the following sets of settings for the fitness_information dictionary')
		print('These settings are to determine what rCut value(s) to sample with the structure + energy fitness operator.')
		print('Either one of the following set:')
		print('    -> rCut_high, rCut_low, rCut_resolution')
		print('    -> rCut')
		print('    -> lattice_constant, nn_high, nn_low, nn_resolution')
		print('    -> lattice_constant, single_nn_measurement')
		print()
		print('Your fitness_information dictionary is: '+str(fitness_information))
		print('Check this.')
		exit('This program will finish without completing.')
	# Make sure that the CNA database in the SCM predation operator would not be the same as the one that will be used in the fitness operator. 
	if (self.predation_switch == 'SCM'):
		check_rCuts_in_fitness_operator = sorted(get_rCuts(self,fitness_information))
		if check_rCuts_in_fitness_operator == sorted(predation_operator.rCuts):
			print('ERROR in def SCM_options, in Class SCM_and_Energy_Fitness_Operator, in SCM_and_Energy_Fitness_Operator.py/SCM_and_Energy_Fitness_Operator_Options.py')
			print('The values of rCut that you will use for your SCM predation method and the structure + energy fitness operator are the same')
			print('This may be because in either the predation or fitness operator you use nearest neighbour settings and in the other you use rCut settings')
			print('In any case, double check your settings for your predation and fitness operators, or if you can not find a problem potentially check the code.')
			print()
			print('Your fitness_information dictionary is: '+str(fitness_information))
			print('Your predation_operator is: '+str(predation_operator))
			print()
			print('Check this.')
			import pdb; pdb.set_trace()
			exit('This program will finish without completing.')

def multiple_settings_error(fitness_information):
	print('ERROR in def SCM_options, in Class SCM_and_Energy_Fitness_Operator, in SCM_and_Energy_Fitness_Operator.py/SCM_and_Energy_Fitness_Operator_Options.py')
	print('You have include conflicting settings in your fitness_information dictionary for the structure + energy fitness operator')
	print('You need to include only one of the following sets of settings for the fitness_information dictionary to tell the structure + energy fitness operator what rCut value(s) to sample.')
	print('Either one of the following set:')
	print('    -> rCut_high, rCut_low, rCut_resolution')
	print('    -> rCut')
	print('    -> lattice_constant, nn_high, nn_low, nn_resolution')
	print('    -> lattice_constant, single_nn_measurement')
	print()
	settings_to_mention = []
	names = ['rCut_high','rCut_low','rCut_resolution','rCut','lattice_constant','nn_high','nn_low','nn_resolution','single_nn_measurement']
	for name in names:
		if name in fitness_information:
			settings_to_mention.append(name)
	print('You have included the following settings in the fitness_information dictionary: '+' '.join(settings_to_mention))
	print()
	print('Your fitness_information dictionary is: '+str(fitness_information))
	print('Check this.')
	exit('This program will finish without completing.')

