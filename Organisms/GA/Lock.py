import os

lock_name = 'ga_running.lock'

def Lock_Check():
	if os.path.exists(lock_name):
		print('------------------------------------------------------------------------')
		print('Issue with Running the Genetic Algorithm.')
		print('The genetic algorithm has found the file "'+lock_name+'" before running the genetic algorithm.')
		print('This means that the user has tried to run this program while the genetic algorithm is already running.')
		print('')
		print('Check that you are not already running this program. If you are not currently running this program, remove the "'+lock_name+'" from the directory and continue.')
		print('')
		print('If you had to stop this program without safely closing it, or if the genetic algorithm was stopped while it was running, this "'+lock_name+'" file will have remained.')
		print('If this is the case for you, it is ok remove "'+lock_name+'" and continue to run the genetic algorithm by typing "Python Run.py" in the terminal like you had just done.')
		print('When you run "Python Run.py" in the terminal, the genetic algorithm will resume from where is was, from the last generation that has completed successfully.')
		print('')
		print('-> Note that you can get rid of all the run files in subfolders if you run "remove_lock_files.py" script in the terminal. See manual for more information about the "remove_lock_files.py" script.')
		print('')
		print('The genetic algorithm will exit without having begun.')
		exit('------------------------------------------------------------------------')

def Lock_Set():
	if os.path.exists(lock_name):
		print('Issue with '+lock_name+'. Check programming of Lock.py')
		exit('The genetic algorithm will exit without having begun.')
	with open(lock_name,'w') as lock_file:
		lock_file.write('\n')

def Lock_Check_and_Set():
	Lock_Check()
	Lock_Set()

def Lock_Remove():
	if not os.path.exists(lock_name): 
		print('------------------------------------------------------------------------')
		print('Something weird had happened. The genetic algorithm is wanting to remove the lock file, but '+lock_name+' does not exist in the directory.')
		print('This is fine, but just note something weird has happened and may pay to figure out what happened.')
		print('Continuing the genetic algorithm, as the genetic algorithm will be finishing up')
		print('------------------------------------------------------------------------')
	else:
		os.remove(lock_name)