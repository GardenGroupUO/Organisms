import os
import subprocess
from shutil import copytree, move

def tail(f, n, offset=0):
	"""
	This method will read the last lines from a text file

	:param f: This is the file path to the path you want to read the end of
	:type  f: str.
	:param n: This is the last lines to read from the document.
	:type  n: int
	:param offset: This is an offset number of line that should at least have been read, but this can be kept as 0 and given in n. For the user to decide. 
	:type  offset: int

	returns lines: These are the line to be read from the end of the document
	rtype   lines: list of str.
	"""
	proc = subprocess.Popen(['tail', '-n', str(n + offset), f], stdout=subprocess.PIPE)
	lines = proc.stdout.readlines()
	return lines

def remove_end_lines_from_text(file, number_of_lines_to_remove):
	"""
	This method removes the last number of lines from the document. 

	For more information, see: https://superuser.com/questions/127786/efficiently-remove-the-last-two-lines-of-an-extremely-large-text-file
	
	:param file: This is the file path to the path you want to read the end of
	:type  file: str.
	:param number_of_lines_to_remove: This is the number of lines to remove from the document.
	:type  number_of_lines_to_remove: int

	"""
	count = 0
	with open(file,'r+b', buffering=0) as f:
		f.seek(0, os.SEEK_END)
		end = f.tell()
		while f.tell() > 0:
			f.seek(-1, os.SEEK_CUR)
			print(f.tell())
			char = f.read(1)
			if char != b'\n' and f.tell() == end:
				print("No change: file does not end with a newline")
				exit(1)
			if char == b'\n':
				count += 1
			if count == number_of_lines_to_remove + 1:
				f.truncate()
				print("Removed " + str(number_of_lines_to_remove) + " lines from end of file")
				return
			f.seek(-1, os.SEEK_CUR)
	if count < number_of_lines_to_remove + 1:
		print("No change: requested removal would leave empty file")
		exit(3)
		
class EnergyProfile:
	"""
	This class is designed to record the energies of the clusters during the genetic algorithm.

	:param collection: This is the specific collection of the genetic algorithm this class will be recording for.
	:type  collection: Organisms.GA.Collection
	:param end_name: Include a suffix to the EnergyProfile.txt filename
	:type  end_name: str.
	"""
	def __init__(self,collection,end_name=None):
		self.path = collection.name
		if end_name == None:
			self.EnergyProfileTXT_path = self.path+"/EnergyProfile.txt"
		else:
			self.EnergyProfileTXT_path = self.path+"/EnergyProfile_"+str(end_name)+".txt"
		self.create()

	def create(self):
		"""
		This definition will create the folders and text files for 
		"""
		if not os.path.exists(self.path):
			os.makedirs(self.path)

	def GA_Starts(self):
		"""
		This will write the energies of the collection into the recording EnergyProfile text file.
		"""
		return

	def add_epoch_note(self):
		"""
		Add a note to the energyprofile to say that an epoch event occurred at this point
		"""
		self.open('a')
		self.energyProfile.write('Restarting due to epoch.\n')
		self.close()

	def add_epoch_note_due_to_population_energy_convergence(self):
		"""
		Add a note to the energyprofile to say that an epoch event occurred at this point due to the energies in the cluster having converged. 
		"""
		self.open('a')
		self.energyProfile.write('Restarting due to epoch. The population has energetically converged.\n')
		self.close()

	def add_found_LES_note(self):
		"""
		Add a note to the energyprofile to say that the LES was located, such that your genetic algorithm will now finish. 
		"""
		self.open('a')
		self.energyProfile.write('Finished prematurely as LES energy found.\n')
		self.close()

	def is_LES_note_in_EnergyProfile(self):
		"""
		Look through the EnergyProfile if it exists for a note saying that the LES had be found.

		:returns True if the EnergyProfile states the LES has been found, otherwise return False.
		:rtype bool.
		"""
		if not os.path.exists(self.EnergyProfileTXT_path):
			return False
		self.open('r')
		for line in self.energyProfile:
			if 'Finished prematurely as LES energy found.' in line:
				return True
		return False

	def add_collection(self,collection,generation_number):
		"""
		This will add information about the collection to the EenrgyProfile.txt

		Inputs:
			collection (Organisms.GA.collection): This is the collection to be added to the EnergyProfile.txt, should be an Offspring_Pool.
			generation_number (int): This is the current generation number of the running Organisms program.
		"""
		self.open('a')
		for cluster in collection:
			self.add_to(cluster,generation_number)
		self.close()

	def add_to(self,cluster,generation_number):
		"""
		This definition will add the information of a cluster. Designed to be used when offspring are created.

		Inputs:
			cluster (Organisms.GA.Cluster): This is the cluster to write information about in the EnergyProfile.txt
			generation_number (int): This is the current generation number of the running Organisms program.
		"""
		self.energyProfile.write("{0}\t{1}\t{2}\n".format(cluster.name, generation_number, cluster.energy))
		
	def open(self,read_type):
		"""
		This will open the EnergyProfile text file that is being recorded to.

		This is designed to be a private definition

		Inputs:
			read_type (str.): This is the way to open the file, either read ('r''), write ('w'), or append ('a').

		"""
		self.energyProfile = open(self.EnergyProfileTXT_path, str(read_type))

	def close(self):
		"""
		This will close the EnergyProfile text file that is being recorded to.

		This is designed to be a private definition
		"""
		self.energyProfile.close()

	def check(self, resume_from_generation, no_offspring_per_generation):
		"""
		Check the EnergyProfile to make sure it is all good to go. As well as if the LES has been located by the genetic algorthm, and to remove any information from the end of the EnergyProfile document that attains to future generations that the algorithm did not complete successfully.

		:param resume_from_generation: The generation that the algorithm is resuming from
		:type  resume_from_generation: int
		:param no_offspring_per_generation: The number of offspring generated per generation. 
		:type  no_offspring_per_generation: int

		"""	
		while True:
			counter = 0
			last_lines_in_EnergyProfile = tail(self.path+'/EnergyProfile.txt',no_offspring_per_generation)[::-1]
			for line in last_lines_in_EnergyProfile:
				if type(line) is bytes:
					line = line.decode()
				if line.startswith('Restarting due to epoch.'):
					counter += 1
					continue
				line = line.split()
				generation = int(line[1])
				if generation > resume_from_generation:
					counter += 1
				elif generation == resume_from_generation:
					break
				elif generation < resume_from_generation:
					print('Error in def check, in class EnergyProfile, in EnergyProfile.py')
					print('The last generation in the '+str(self.EnergyProfileTXT_path)+' is less than the resumed generation.')
					print('Check the EnergyProfile file for this GA run before continuing. There may be an issue here')
					print('Last generation in the EnergyProfile file: '+str(generation))
					print('Generation to resume from: '+str(resume_from_generation))
					import pdb; pdb.set_trace()
					exit('The genetic algorithm will finished without starting.')
			if counter > 0:
				print('Removing the last '+str(counter)+' from '+str(self.path+'/EnergyProfile.txt'))
				remove_end_lines_from_text(self.path+'/EnergyProfile.txt', counter)
			else:
				break
		last_lines_in_EnergyProfile = tail(self.path+'/EnergyProfile.txt',no_offspring_per_generation)
		all_cluster_gen_made = []
		for line in last_lines_in_EnergyProfile:
			line = line.split()
			generation = int(line[1])
			all_cluster_gen_made.append(generation)
		if not (len(set(all_cluster_gen_made)) == 1):
			print('Error in def check, in class EnergyProfile, in EnergyProfile.py')
			print('The last generation in the '+str(self.EnergyProfileTXT_path)+' is not the resumed generation.')
			print('Check the EnergyProfile file for this GA run before continuing. There may be an issue here')
			print('Generations of clusters in proposed population'+str(all_cluster_gen_made))
			print('Generation to resume from: '+str(resume_from_generation))
			import pdb; pdb.set_trace()
			exit('The genetic algorithm will finished without starting.')
		all_cluster_gen_made = all_cluster_gen_made[0]
		if all_cluster_gen_made == resume_from_generation:
			return
		else:
			print('Error in def check, in class EnergyProfile, in EnergyProfile.py')
			print('The last generation in the '+str(self.EnergyProfileTXT_path)+' is less than the resumed generation.')
			print('Check the EnergyProfile file for this GA run before continuing. There may be an issue here')
			print('Last generation in the EnergyProfile file: '+str(all_cluster_gen_made))
			print('Generation to resume from: '+str(resume_from_generation))
			import pdb; pdb.set_trace()
			exit('The genetic algorithm will finished without starting.')

	def get_current_generation_and_last_cluster_generated_from_EnergyProfile(self):
		"""
		Get the number of the last generation and the name of the last cluster that was recorded in the EnergyProfile

		:returns The last recorded generation, and the name of the last recorded cluster.
		:rtype   int, int

		"""
		last_lines_in_EnergyProfile = tail(self.path+'/EnergyProfile.txt',1)
		#import pdb; pdb.set_trace()
		#line = last_lines_in_EnergyProfile.readline()
		#line = line.rstrip().split()
		line = last_lines_in_EnergyProfile[0].rstrip().split()
		name       = int(line[0])
		generation = int(line[1])
		return generation, name
