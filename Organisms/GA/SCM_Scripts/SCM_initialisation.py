import numpy as np

def get_SCM_methods(SCM_Scheme):
	"""
	This method will provide the methods needed to obtain the CNA_profile and similarity_profile, using either the T-SCM or the A-SCM. 

	:param SCM_Scheme: This determines if the SCM scheme being used is the "T-SCM" or "A-SCM". Must be one of those two schemes.
	:type  SCM_Scheme: str.
	"""
	if SCM_Scheme == 'A-SCM':
		from Organisms.GA.SCM_Scripts.AC_SCM_Methods import get_CNA_profile, get_CNA_similarities
	elif SCM_Scheme == 'T-SCM':
		from Organisms.GA.SCM_Scripts.TC_SCM_Methods import get_CNA_profile, get_CNA_similarities
	else:
		print('Error in initialisation of CNA_Database, in CNA_Database.py')
		print('self.SCM_Scheme must be either "T-SCM" or "A-SCM".')
		print('self.SCM_Scheme = '+str(SCM_Scheme))
		print('Check this.')
		import pdb; pdb.set_trace()
		exit()
	return get_CNA_profile, get_CNA_similarities

def get_rCut_values(rCut_low,rCut_high,rCut_resolution):
	"""
	This method will give a lost of rCut values that you want to perform the CNA across, in Angstroms

	:parm rCut_low: This is the lowest rCut value you want to obtain the CNA for.
	:type rCut_low: float
	:parm rCut_high: This is the highest rCut value you want to obtain the CNA for.
	:type rCut_high: float
	:parm rCut_resolution: This is the resolution of the rCut values you are performing all the CNA's with. The resolution can be given as one of two forms. 

		* If given as a float, rCut_resolution is the difference between rCut values that will be sampled. Note that your input for rCut_resolution is not divisible by (rCut_high-rCut_low), then rCut_high will not be included in rCuts.
		* If given as a int, rCut_resolution is the number of rCut values in the list rCuts, evenly distributed between (and including) rCut_low and rCut_high.

	:type rCut_resolution: float or int

	:returns: A list of all the rCut values you want the CNA to sample.
	:rtype:   list of floats
	"""
	if isinstance(rCut_resolution,float):
		rCuts = list(np.arange(rCut_low,rCut_high+rCut_resolution,rCut_resolution))
	elif isinstance(rCut_resolution,int):
		rCuts = list(np.linspace(rCut_low,rCut_high,num=rCut_resolution,endpoint=True))
	else:
		print('Error in class CNA_Diversity_Scheme, in CNA_Diversity_Scheme.py')
		print('self.rCut_resolution must be either a float or an int.')
		print('self.rCut_resolution = '+str(rCut_resolution))
		print('Check this.')
		print('This program will not end.')
		exit()
	for index in range(len(rCuts)-1,-1,-1):
		rCuts[index] = round(rCuts[index],10)
	return rCuts

def get_rCuts(self,Predation_Information):
	"""
	Obtain the values for values of rCut the user wishes to investigate.

	:param Predation_Information: This contains all the information needed by the Predation Operator you want to use to run.
	:type  Predation_Information: dict.

	:returns: A list of all the rCut values you want the CNA to sample.
	:rtype:   list of floats
	
	"""
	# An initial check to make sure of you have parameters
	if ('lattice_constant' in Predation_Information):
		if any([(name in ['rCut','rCut_low','rCut_high','rCut_resolution']) for name in Predation_Information]):
			print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
			print('You have included the "lattice_constant" parameter in your Predation_Information')
			print("but you have also included 'rCut' and/or 'rCut_low','rCut_high','rCut_resolution' in the Predation_Information")
			print('Check the settings in the Predation_Information')
			print('Predation_Information = '+str(Predation_Information))
			import pdb; pdb.set_trace()
			exit('This program will exit without completing')
	else:
		if any([(name in ['single_nn_measurement','nn_low','nn_high','nn_resolution']) for name in Predation_Information]):
			print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
			print('You have not included the "lattice_constant" parameter in your Predation_Information')
			print("but you have included 'single_nn_measurement' and/or 'nn_low','nn_high','nn_resolution' in the Predation_Information")
			print('Check the settings in the Predation_Information')
			print('Predation_Information = '+str(Predation_Information))
			import pdb; pdb.set_trace()
			exit('This program will exit without completing')

	# Perform a check on the single_nn_measurement, nn_low, nn_high, and nn_resolution inputs in Predation_Information
	if ('lattice_constant' in Predation_Information):
		self.lattice_constant = float(Predation_Information['lattice_constant'])
		self.fnn_distance = lattice_constant / (2.0 ** 0.5)
		if (('nn_low' in Predation_Information) or ('nn_high' in Predation_Information) or ('nn_resolution' in Predation_Information)):
			if not (('nn_low' in Predation_Information) and ('nn_high' in Predation_Information) and ('nn_resolution' in Predation_Information)):
				print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
				print('If you are wanting to have a range of nn values, you need to include the following in Predation_Information:')
				print('\t* nn_low')
				print('\t* nn_high')
				print('\t* nn_resolution')
				print('Make sure you have all of these in Predation_Information.')
				print('Predation_Information = '+str(Predation_Information))
				import pdb; pdb.set_trace()
				exit('This program will exit without completing')
			elif ('single_nn_measurement' in Predation_Information):
				print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
				print('In Predation_Information, you have included single_nn_measurement as well as nn_low, nn_high, and/or nn_resolution.')
				print('You can only enter into Predation_Information either single_nn_measurement, or all of nn_low, nn_high, and nn_resolution')
				print('Only inlclude the following if you want to have a range of nn values:')
				print('\t* nn_low')
				print('\t* n_high')
				print('\t* rn_resolution')
				print('Only include single_nn_measurement if you want to include only want to sample the similarity at one value of single_nn_measurement.')
				print('Predation_Information = '+str(Predation_Information))
				import pdb; pdb.set_trace()
				exit('This program will exit without completing')
			else:
				multiple_rCut = True; simple_rCut = False
				self.nn_low = float(Predation_Information['nn_low'])
				if not (1.0 <= nn_low <= 2.0):
					print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
					print('nn_low must be between 1.0 and 2.0')
					print('nn_low = '+str(nn_low))
					print('Check this')
					exit('This program will exit without completing')
				self.nn_high = float(Predation_Information['nn_high'])
				if not (1.0 <= nn_high <= 2.0):
					print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
					print('nn_high must be between 1.0 and 2.0')
					print('nn_high = '+str(nn_high))
					print('Check this')
					exit('This program will exit without completing')
				self.nn_resolution = Predation_Information['nn_resolution']
				if not nn_resolution % 1.0 == 0:
					print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
					print('nn_resolution must be a whole number')
					print('nn_resolution = '+str(nn_resolution))
					print('Check this')
					exit('This program will exit without completing')
				self.nn_resolution = int(nn_resolution)
				self.rCut_low = self.fnn_distance *self. nn_low
				self.rCut_high = self.fnn_distance * self.nn_high
				self.rCut_resolution = self.nn_resolution
		elif 'single_nn_measurement' in Predation_Information:
			if (('nn_low' in Predation_Information) or ('nn_high' in Predation_Information) or ('nn_resolution' in Predation_Information)):
				print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
				print('In Predation_Information, you have included single_nn_measurement as well as nn_low, nn_high, and/or nn_resolution.')
				print('You can only enter into Predation_Information either single_nn_measurement, or all of nn_low, nn_high, and nn_resolution')
				print('Only inlclude the following if you want to have a range of single_nn_measurement values:')
				print('\t* nn_low')
				print('\t* nn_high')
				print('\t* nn_resolution')
				print('Only include single_nn_measurement if you want to include only want to sample the similarity at one value of single_nn_measurement.')
				print('Predation_Information = '+str(Predation_Information))
				import pdb; pdb.set_trace()
				exit('This program will exit without completing')
			else:
				multiple_rCut = False; simple_rCut = True
				self.single_nn_measurement = float(Predation_Information['single_nn_measurement'])
				if not (1.0 <= single_nn_measurement <= 2.0):
					print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
					print('single_nn_measurement must be between 1.0 and 2.0')
					print('single_nn_measurement = '+str(single_nn_measurement))
					print('Check this')
					exit('This program will exit without completing')
				self.rCut = self.fnn_distance * self.single_nn_measurement
		else:
			print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
			print('In Predation_Information, you have or have not included single_nn_measurement as well as nn_low, nn_high, and/or nn_resolution.')
			print('You can only enter into Predation_Information either single_nn_measurement, or all of nn_low, nn_high, and nn_resolution')
			print('Only include the following if you want to have a range of nn values:')
			print('\t* nn_low')
			print('\t* nn_high')
			print('\t* nn_resolution')
			print('Only include single_nn_measurement if you want to include only want to sample the similarity at one value of rCut.')
			print('Predation_Information = '+str(Predation_Information))
			import pdb; pdb.set_trace()
			exit('This program will exit without completing')
	# lattice constant nearest neighbour distances have not been given. Using given rCut values
	else:
		if (('rCut_low' in Predation_Information) or ('rCut_high' in Predation_Information) or ('rCut_resolution' in Predation_Information)):
			if not (('rCut_low' in Predation_Information) and ('rCut_high' in Predation_Information) and ('rCut_resolution' in Predation_Information)):
				print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
				print('If you are wanting to have a range of rCut values, you need to include the following in Predation_Information:')
				print('\t* rCut_low')
				print('\t* rCut_high')
				print('\t* rCut_resolution')
				print('Make sure you have all of these in Predation_Information.')
				print('Predation_Information = '+str(Predation_Information))
				import pdb; pdb.set_trace()
				exit('This program will exit without completing')
			elif ('rCut' in Predation_Information):
				print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
				print('In Predation_Information, you have included rCut as well as rCut_low, rCut_high, and/or rCut_resolution.')
				print('You can only enter into Predation_Information either rCut, or all of Cut_low, rCut_high, and rCut_resolution')
				print('Only inlclude the following if you want to have a range of rCut values:')
				print('\t* rCut_low')
				print('\t* rCut_high')
				print('\t* rCut_resolution')
				print('Only include rCut if you want to include only want to sample the similarity at one value of rCut.')
				print('Predation_Information = '+str(Predation_Information))
				import pdb; pdb.set_trace()
				exit('This program will exit without completing')
			else:
				multiple_rCut = True; simple_rCut = False
				self.rCut_low = float(Predation_Information['rCut_low'])
				self.rCut_high = float(Predation_Information['rCut_high'])
				self.rCut_resolution = Predation_Information['rCut_resolution']
		elif ('rCut' in Predation_Information):	
			if (('rCut_low' in Predation_Information) or ('rCut_high' in Predation_Information) or ('rCut_resolution' in Predation_Information)):
				print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
				print('In Predation_Information, you have or or have not included rCut as well as rCut_low, rCut_high, and/or rCut_resolution.')
				print('You can only enter into Predation_Information either rCut, or all of Cut_low, rCut_high, and rCut_resolution')
				print('Only inlclude the following if you want to have a range of rCut values:')
				print('\t* rCut_low')
				print('\t* rCut_high')
				print('\t* rCut_resolution')
				print('Only include rCut if you want to include only want to sample the similarity at one value of rCut.')
				print('Predation_Information = '+str(Predation_Information))
				import pdb; pdb.set_trace()
				exit('This program will exit without completing')
			else:		
				multiple_rCut = False; simple_rCut = True
				self.rCut = float(Predation_Information['rCut'])
		else:
			print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
			print('In Predation_Information, you have included rCut as well as rCut_low, rCut_high, and/or rCut_resolution.')
			print('You can only enter into Predation_Information either rCut, or all of Cut_low, rCut_high, and rCut_resolution')
			print('Only inlclude the following if you want to have a range of rCut values:')
			print('\t* rCut_low')
			print('\t* rCut_high')
			print('\t* rCut_resolution')
			print('Only include rCut if you want to include only want to sample the similarity at one value of rCut.')
			print('Predation_Information = '+str(Predation_Information))
			import pdb; pdb.set_trace()
			exit('This program will exit without completing')
	# Make the set of rCuts
	if multiple_rCut:
		rCut_low = Predation_Information['rCut_low']
		rCut_high = Predation_Information['rCut_high']
		rCut_resolution = Predation_Information['rCut_resolution']
		rCuts = get_rCut_values(rCut_low,rCut_high,rCut_resolution)
	elif simple_rCut:
		rCut = Predation_Information['rCut']
		rCuts = [rCut]
	else:
		print('Error in creation of class SCM_Predation_Operator, in SCM_Predation_Operator.py')
		print('')
		import pdb; pdb.set_trace()
		exit()
	return rCuts # return rCuts to initialisation of SCM_Predation_Operator


	