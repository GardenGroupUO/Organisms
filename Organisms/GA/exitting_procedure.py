import atexit
from Organisms.GA.Lock import Lock_Remove

def exit_handler():
	print('Unlocking the genetic algorithm program before exitting program.')
	Lock_Remove()

def add_to_exitting_procedure():
	atexit.register(exit_handler)