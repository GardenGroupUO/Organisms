from math import tanh, exp

class Fitness_Function:
	"""
	This class is designed to calculator the fitness value of a cluster, given a value of rho_i. 
	This class will include all the relavant information required, such as parameters, needed for the functions to convert rho_i into a fitness value.
	
	:param entries: This is a dictionary that contains all the input variables required for the fitness function. 
	:type  entries: dict.
	"""
	def __init__(self,**entries):
		self.__dict__.update(entries)
		if self.function == 'exponential':
			self.function = self.exponential_function
		elif self.function == 'tanh':
			self.function = self.tanh_function
		elif self.function == 'linear':
			self.linear_function = linear_function
		elif self.function == 'direct':
			self.linear_function = direct_function
		else:
			print('Error in initiating the Fitness_Function object.')
			print('The "function" input must be either (and including function variables):')
			print('    exponential (alpha)')
			print('    tanh')
			print('    linear (gradient,coefficent)')
			print('    direct_function')
			print('Correct for this and try running the genetic algorithm again.')
			exit ('This algorithm will exit without completing')
		self.check_parameters()

	def check_parameters(self):
		if self.function == 'exponential':
			self.function = self.exponential_function
			has_alpha = 'alpha' in self.__dict__.keys()
			if not (has_alpha):
				print('Error in class Fitness_Function, in Fitness_Function.py')
				print('To use the exponential fitness function, you must include variables for "alpha".')
				print('What you currently include:')
				print('    alpha: '+str(has_alpha))
				print('')
				print('Information about the fitness function: '+str(self.__dict__))
				print('Check this out.')
				exit('The genetic algorithm will exit without completing.')
		elif self.function == 'tanh':
			pass
		elif self.function == 'linear':
			has_gradient = 'gradient' in self.__dict__.keys()
			has_coefficient = 'coefficient' in self.__dict__.keys()
			if not (has_gradient and has_coefficient):
				print('Error in class Fitness_Function, in Fitness_Function.py')
				print('To use the linear fitness function, you must include variables for "gradient" and "coefficient".')
				print('What you currently include:')
				print('    gradient: '+str(has_gradient))
				print('    coefficient: '+str(has_coefficient))
				print('')
				print('information about the fitness function: '+str(self.__dict__))
				print('Check this out.')
				exit('The genetic algorithm will exit without completing.')
		elif self.function == 'direct':
			pass

	def get_fitness(self,rho_i):
		"""
		This def will give the fitness value for a given value of rho_i

		:param rho_i: a value
		:type  rho_i: float

		:returns: value
		:rtypes: float

		"""
		try:
			value = self.function(rho_i)
		except OverflowError as err:
			value = float('inf') 
		return value

	# ----------------------------------------------------------------------------------------------------------

	def exponential_function(self,rho_i):
		"""
		This definition is designed to return the result of the exp function for this genetic algorithm.

		Equation written as required in the genetic algorithm.

		:param rho_i: a value
		:type  rho_i: float
		:param alpha: a value
		:type  alpha: float

		:returns: value
		:rtypes: float

		"""
		try:
			value = exp(-1.0*float(self.alpha)*float(rho_i))
		except OverflowError as err:
			value = float('inf') 
		return value

	def tanh_function(self,rho_i):
		"""
		This definition is designed to return the result of the tanh function for this genetic algorithm.

		Equation written as required in the genetic algorithm.

		:param rho_i: a value
		:type  rho_i: float

		:returns: value
		:rtypes: float

		"""
		return 0.5*(1.0 - tanh(2.0*float(rho_i) - 1.0))

	def linear_function(self,rho_i):
		"""
		This definition is designed to return the result of the linear function for this genetic algorithm.

		Equation written as required in the genetic algorithm.

		:param rho_i: a value
		:type  rho_i: float
		:param gradient: a value
		:type  gradient: float
		:param coefficent: a value
		:type  coefficent: float

		:returns: value
		:rtypes: float

		"""
		try:
			value = self.gradient*float(rho_i) + self.coefficent
		except OverflowError as err:
			value = float('inf') 
		return value

	def direct_function(self,rho_i):
		"""
		This definition is designed to return the value for rho_i without any mathematical changes to it.

		Equation written as required in the genetic algorithm.

		:param rho_i: a value
		:type  rho_i: float

		:returns: rho_i
		:rtypes: float

		"""
		return rho_i

	# ----------------------------------------------------------------------------------------------------------