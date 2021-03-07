import os
import time
from datetime import datetime

class Timer:
	"""
	This class is designed to time the genetic algorithm, as well as to determine if the algorithm has run for longer than is desired by the total_length_of_running_time variable.

	:param total_length_of_running_time: This is the length of time to run the algorithm for before safely finishing the algorithm. The time is given in hours
	:type  total_length_of_running_time: float
	"""
	def __init__(self,total_length_of_running_time):
		self.total_length_of_running_time = total_length_of_running_time # Hours
		if not self.total_length_of_running_time == None:
			self.total_length_of_running_time *= (60.0*60.0) # turns the time in to seconds. 
		self.start_time = time.time()

	def get_total_length_of_running_time(self):
		'''
		Return the maximum amount of time to run the genetic algorithm for, in hours.

		:returns: total_length_of_running_time, the maximum amount of time to run the genetic algorithm for, in hours.
		:rtype:   float or str.
		'''
		if self.total_length_of_running_time == None: 
			return 'Indefinitely'
		else:
			return str(self.total_length_of_running_time/(60.0*60.0))+' hours'

	def has_elapsed_time(self):
		"""
		This determines if the cluster has exceeded the desired running time.
		"""
		if self.total_length_of_running_time == None:
			return False
		elapsed_time = time.time() - self.start_time
		return (elapsed_time > self.total_length_of_running_time)

	def print_elapsed_time(self):
		"""
		Returns the current running time of the algorithm
		"""
		elapsed_time = time.time() - self.start_time
		return time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

	def get_time_now(self):
		"""
		Returns the current date and time.
		"""
		return datetime.now()