import os, time

class GA_Program_Details:
	"""
	This class is designed to keep track of the process of the genetic algorithm run.

	:param GA_Program: This is the main genetic algorithm program this class will be writing about
	:type  GA_Program: Organisms.GA.GA_Program: 
	:param is_new_ga: This determines if to write all the details about this genetic algorithm to a file. You only need to do this if the genetic algorithm is just beginning from generation 0. Default: True.
	:type  is_new_ga: bool.
	"""
	def __init__(self,GA_Program,is_new_ga=True):
		self.Run_path = GA_Program.Run_path
		self.details_filename = 'GA_Run_Details.txt'
		# Recording data about this genetic algorithm run.
		self.number_of_matings = 0
		self.number_of_successful_matings = 0
		#self.number_of_mutation = [0]*len(GA_Program.mutTypes)
		#self.number_of_successful_mutation = [0]*len(GA_Program.mutTypes)
		self.no_of_explosions = 0
		self.no_of_not_converged = 0
		self.create(is_new_ga)

	##############################################################################################################

	def create(self, is_new_ga): #add new variable
		"""
		This definition will create a file containing the details of this genetic algorithm on the disk.

		:param is_new_ga: This determines if to write all the details about this genetic algorithm to a file. You only need to do this if the genetic algorithm is just beginning from generation 0.
		:type  is_new_ga: bool.
		"""
		if is_new_ga:
			if not os.path.exists(self.Run_path+'/'+self.details_filename):
				self.open('w')
				self.close()
			else:
				print('Error in def create of class GAProgram_Details, in GAProgram_Details.py')
				print(str(self.details_filename)+' in '+str(self.Run_path)+' already exists.')
				print('Check this.')
				print('The program is finishing without performing any part of the genetic algorithm.')
				exit() 
		else:
			if not os.path.exists(self.Run_path+'/'+self.details_filename):
				print('Error in def create of class GAProgram_Details, in GAProgram_Details.py')
				print(str(self.details_filename)+' in '+str(self.Run_path)+' does not exist, however the GA is being resumed, so should already have a '+str(self.details_filename)+' file.')
				print('Check this.')
				print('The program is finishing without performing any part of the genetic algorithm.')
				exit() 

	def start_clock(self):
		"""
		Get the Starting time for this genetic algorithm, which will be used to time each generation.
		"""
		self.startTime = time.time()

	def end_clock(self, generation):
		"""
		Get the end time taken for a generation to run.

		:param generation: The generation that was run. 
		:type  generation: int

		returns time_taken: The time taken for the generation to run in seconds. 
		rtype   time_taken: float
		"""
		endTime = time.time()
		time_taken = endTime - self.startTime
		del self.startTime
		self.open('a')
		self.GA_Run_Details.write(str(generation)+': '+str(time_taken)+' s\n')
		self.close()
		return time_taken

	def ending_details(self):
		"""
		This def will write the finishing remarks of the genetic algorithm to GA_Run_Details
		"""
		self.endTime = time.time()

		self.open("w+")
		self.GA_Run_Details.write("The Genetic Algorithm finished successfully.\n")
		self.GA_Run_Details.write("This program took " + str((self.endTime - self.startTime)) + " s to run.\n")
		self.GA_Run_Details.write("\n")
		self.GA_Run_Details.write("DETAILS\n")
		self.GA_Run_Details.write("\n")
		self.GA_Run_Details.write("Number of Instances where cluster creation was restarted due to the cluster exploding: "+str(self.no_of_explosions)+"\n")
		self.GA_Run_Details.write("Number of Instances where cluster creation was restarted due to the local optimisation not converging: "+str(self.no_of_not_converged)+"\n")
		self.close()

	##############################################################################################################
		
	def open(self,read_type):
		"""
		This will open the GA_Run_Details text file that is being recorded to.

		This is designed to be a private definition

		:param read_type: This is the way to open the file, either read (r), write (w), or append (a).
		:type  read_type: char
		"""
		self.GA_Run_Details = open(self.Run_path+'/'+self.details_filename, str(read_type))

	def close(self):
		"""
		This will close the GA_Run_Details text file that is being recorded to.

		This is designed to be a private definition
		"""
		self.GA_Run_Details.close()
