'''
Cluster.py, 12/04/2017, Geoffrey R Weal

This class is specifically designed to hold cluster objects for the 
Genetic Algorithm program. This object will hold a reference to the 
Atoms class from ASE for the cluster, the energy of the cluster and 
the dir tag for the cluster

'''

from ase import Atoms
from copy import deepcopy
from ase.visualize import view
from collections import Counter
from numpy import array, zeros, sort
from time import time

from Organisms.GA.ExternalDefinitions import InclusionRadiusOfCluster

def import_surface(surface):
	"""
	This method is designed to import the surface into the genetic algorithm

	:param surface: This is the surface that the cluster is optimised upon. 
	:type  surface: str/ASE.Atoms.
	"""
	if isinstance(surface, test_Atoms):
		surface = surface
	elif isinstance(surface, str):
		surface = ase_read(surface)
	elif surface == None:
		surface = None
	else:
		exit('Error')
	for index in range(len(surface)):
		surface[index].type = 'surface'

	surface.centre()
	return surface

class Cluster(Atoms):
	'''
	This class is designed to clude all the information that the genetic algorithm needs to know from the chemical system.

	:param symbols: This can be a list of all the chemical symbols of atoms in the clusters, OR, the ASE.Atoms object that this object will be base on. For writing this as a list of element symbols, see See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information. Default: None
	:type  symbols: str (formula) or list of str., or ASE.Atoms
	:param positions: A list of all the (x,y,z) values for the cluster. See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information.  Default: None
	:type  positions: list of xyz-positions
	:param numbers: See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information. Default: None
	:type  numbers: list of int
	:param tags: See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information. Default: None
	:type  tags: list of int
	:param momenta: See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information. Default: None
	:type  momenta: list of xyz-momenta
	:param masses: See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information. Default: None
	:type  masses: list of float
	:param magmoms: See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information. Default: None
	:type  magmoms: list of float or list of xyz-values
	:param charges: See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information. Default: None
	:type  charges: list of float
	:param scaled_positions: See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information. Default: None
	:type  scaled_positions: list of scaled-positions
	:param cell: See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information. Default: None
	:type  cell: 3x3 matrix or length 3 or 6 vector
	:param pbc: See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information. Default: None
	:type  pbc: one or three bool
	:param celldisp: See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information. Default: None
	:type  celldisp: Vector
	:param constraint: See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information. Default: None
	:type  constraint: constraint object(s)
	:param calculator: See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information. Default: None
	:type  calculator: calculator object
	:param info: See https://wiki.fysik.dtu.dk/ase/ase/atoms.html?highlight=atoms#ase.Atoms for more information. Default: None
	:type  info: dict of key-value pairs
	:param surface: This is the surface that the cluster is modelled on. This is given either as a string or the ASE.Atoms object. Default: None
	:type  surface: ASE.Atoms/str.

	'''
	def __init__(self,symbols=None,positions=None,numbers=None,tags=None,momenta=None,masses=None,magmoms=None,charges=None,scaled_positions=None,cell=None,pbc=None,celldisp=None,constraint=None,calculator=None,info=None,surface=None):
		if isinstance(symbols,Atoms):
			positions = symbols.get_positions()
			numbers = symbols.get_atomic_numbers()
			tags = symbols.get_tags()
			momenta = symbols.get_momenta()
			masses = symbols.get_masses()
			magmoms = symbols.get_initial_magnetic_moments()
			charges = symbols.get_initial_charges()
			scaled_positions = None #symbols.get_scaled_positions()
			cell = symbols.get_cell()
			pbc = symbols.get_pbc()
			celldisp = symbols.get_celldisp()
			constraint = [c.copy() for c in symbols.constraints]
			calculator = symbols.get_calculator()
			info = deepcopy(symbols.info)
			symbols = None
		super().__init__(symbols,positions,numbers,tags,momenta,masses,magmoms,charges,scaled_positions,cell,pbc,celldisp,constraint,calculator,info)
		self.verified = False
		self.name = None

	def __str__(self):
		"""
		:returns: a label for this cluster, which is the dir of the cluster
		:rtype: str
		"""
		return 'Cluster_'+str(self.name)

	def __repr__(self):
		"""
		:returns: a label for this cluster, which is the dir of the cluster
		:rtype: str
		"""
		return str(self)

	def view(self):
		"""
		Allow the user to visually look at the cluster using the ASE gui. This is a debugging method.
		"""
		view(self)

	def verify_cluster(self,name,gen_made,vacuum_length,rounding_criteria):
		"""
		This method will verify that the cluster contains all the other information that it needs to run during the genetic algorithm, providing the name, generation made, and the energy of the cluster, as well as centering in a unit cell. 
		This method is performed after the cluster has been locally optimised. 

		:param name: The name that the cluster is referenced in this genetic algorithm program. This should be a integer that is based on when the cluster was made. 
		:type  name: int/str.
		:param gen_made: This is the generation when the cluster was created
		:type  gen_made: int
		:param vacuum_length: This is the amount of vacuum to give the cluster.
		:type  vacuum_length: float
		:param rounding_criteria: The number of decimal places that the cluster's energy is rounded to.
		:type  rounding_criteria: int

		"""
		self.verified = True
		self.name = name
		self.gen_made = gen_made
		self.sorted_by_Z = False
		if not len(self) == 0:
			#energy_start = time()
			self.energy = self.get_total_cluster_energy(rounding_criteria)
			#energy_end = time()
			#print(' '.join(['energy time = ',str(energy_end-energy_start)]))
			self.centre_cluster_at_centre_of_cell(vacuum_length)
		elif self.dir == -1:
			pass
		else:
			print('Error in Cluster, in Cluster.py')
			print('This cluster contains no atoms.')
			print("This probably shouldn't happen")
			print('Check this.')
			import pdb; pdb.set_trace()
			exit('This program will finish without completing.')

	def custom_verify_cluster(self,name,gen_made,cluster_energy,ever_in_population,excluded_because_violates_predation_operator,initial_population):
		"""
		This method allows you to custom verify the cluster. To be used when resuming the genetic algorithm. 

		:param name: The name that the cluster is referenced in this genetic algorithm program. This should be a integer that is based on when the cluster was made. 
		:type  name: int/str.
		:param gen_made: This is the generation when the cluster was created
		:type  gen_made: int
		:param ever_in_population: Was this cluster ever in the population. 
		:type  ever_in_population: bool.
		:param excluded_because_violates_predation_operator: Was the cluster removed from the offspring pool because it violated the predation operator
		:type  excluded_because_violates_predation_operator: bool.
		:param initial_population: Was the cluster apart of the initial population, either at rhe beginning of the population or after an epoch.
		:type  initial_population: bool.

		"""
		self.verified = True
		self.name = name
		self.gen_made = gen_made
		self.sorted_by_Z = False
		self.energy = cluster_energy
		self.ever_in_population = ever_in_population
		self.excluded_because_violates_predation_operator = excluded_because_violates_predation_operator
		self.initial_population = initial_population

	def sortZ(self):
		"""
		Sort the cluster from most positive to most negative value of z. This sorting by z axis is required to allow the algorithm to easily split itself into two sides of a dividing plane.

		"""
		if not self.sorted_by_Z:
			new_cluster = zeros((len(self),4))
			new_cluster.T[0] = self.get_atomic_numbers()
			new_cluster.T[1:] = self.get_positions().T #arrays['positions'].T
			new_cluster = array(sorted(new_cluster,key=lambda atom: atom[3],reverse=True))
			self.set_positions(new_cluster.T[1:].T)
			self.set_atomic_numbers(new_cluster.T[0].T)
			self.sorted_by_Z = True

	def get_total_cluster_energy(self,rounding_criteria=None):	
		'''
		Obtain the energy of the cluster to a predefined decimal place.
		
		:param rounding_criteria: The number of decimal places that the cluster's energy is rounded to.
		:type  rounding_criteria: int

		returns energy: This is the energy of the cluster
		rtype   energy: float
		'''
		energy = self.get_potential_energy()
		if not rounding_criteria == None:
			energy = round(energy,rounding_criteria)
		return energy

	def centre_cluster_at_centre_of_cell(self,vacuumAdd):
		"""
		This method will center the cluster in the middle of the cell. This method has been employed to make it easier to look at clusters that are made during the Organisms program. 

		Inputs:
			vacuumAdd (float): The amount of value to add around the cluster.
		"""
		lengthOfCell = 2.0*InclusionRadiusOfCluster(self) + vacuumAdd
		cell = [lengthOfCell,lengthOfCell,lengthOfCell]
		self.set_cell(cell)
		#start_time = time()
		self.center(vacuum=None, axis=(0, 1, 2), about=0.) # make a better center function?
		#end_time = time()
		#print('center time = '+str(end_time-start_time))

	def get_elemental_makeup(self):
		"""
		This gives a list which indicates the types of elements, and the number of those elements, in the cluster

		:returns: A list which indicates the types of elements, and the number of those elements, in the cluster
		:rtype: {str: int, ...} (old output was [[str.,int],...])
		"""
		return Counter(self.get_chemical_symbols())
		#self.chemical_makeup = Counter(self.get_chemical_symbols())
		#return self.chemical_makeup #Counter(self.get_chemical_symbols())

	def remove_calculator(self):
		"""
		This method will remove the calculator for this Cluster
		"""
		self.set_calculator(calc=None)

	def deepcopy(self):
		"""
		Will create a copy of the Cluster. This copy does not include a copy of the calculator as this has the potential to cause issues.
		"""
		#return self.copy()
		original_calculator = self.get_calculator()
		self.remove_calculator()
		new_Cluster = deepcopy(self)
		self.set_calculator(calc=original_calculator)
		return new_Cluster

	def deepcopy_skeleton(self):
		"""
		This will create a copy of the cluster that does not contain any atoms, but will contain all the other settings for this cluster.
		"""
		skeleton = self.deepcopy()
		for NOTUSED in range(len(skeleton)):
			del skeleton[-1]
		return skeleton