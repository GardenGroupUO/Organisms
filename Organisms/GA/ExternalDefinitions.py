"""
ExternalDefinitions.py, 12/04/2017, Geoffrey R Weal

This python script is designed to hold subsidery definitions used by this Genetic Algorithm.

"""

from ase import Atom, Atoms
import copy, os
import collections

class atom_single_connection:
	"""
	This class is designed to record all the atoms an atom in a cluster is bonded/neighboured to, where a bond is
	defined as a atom-atom distance less than max_distance_between_atoms.
	:param atom: The dir of the atom in the cluster
	:type  atom: int
	"""
	def __init__(self,atom):
		self.atom = atom
		self.bonded_to = [] # The dir of the atoms that this self.atom is bonded to

def get_distance(atom1,atom2):
	xx = atom1[0] - atom2[0]
	yy = atom1[1] - atom2[1]
	zz = atom1[2] - atom2[2]
	return (xx*xx + yy*yy + zz*zz) ** 0.5

def Exploded(cluster, max_distance_between_atoms):
	"""
	This definition is designed to check to make sure a cluster has not exploded. This means that all the
	atoms in space are closely bound together as a nanoparticle rather than some atoms being
	disconnected from the majority of atoms in a cluster. This method works as follows:

	* Every atom is checked for neighbours/ other atoms it is bonded to in the cluster. The information of the neighbours of each atom are placed in a neighbour list
	* Write this later

	:param cluster: the cluster to check if all clusters are attached together.
	:type  cluster: ASE.Atoms
	:param max_distance_between_atoms: defines what the maximum length of a bond is in your cluster.
	:type  max_distance_between_atoms: float
	"""
	'''
	First the neighbours of all atoms in the cluster are recorded. These are all the atoms that have a bond length less than max_distance_between_atoms.
	'''
	# Initialise the list neighbours_list
	neighbours_list = []
	for ii in range(len(cluster)):
		neighbours_list.append(atom_single_connection(ii))
	# find and record the bonds for each atom in the cluster.
	cluster_positions = cluster.arrays['positions']
	for ii in range(len(neighbours_list)):
		for jj in range(ii+1,len(neighbours_list)): # from ii+1 to len(neighbours_list) as to prevent double recording of bonds.
			distance = get_distance(cluster_positions[neighbours_list[ii].atom],cluster_positions[neighbours_list[jj].atom]) # obtain the distance between two atoms
			# if distance < max_distance_between_atoms, the neighbours_list ii and jj are bonded together,
			# so record this in the instance of the class atom_single_connection for this atom
			if distance < max_distance_between_atoms:
				neighbours_list[ii].bonded_to.append(jj)
				neighbours_list[jj].bonded_to.append(ii)
	'''
	We now check to see that every atom is connect to a single entity (i.e. a cluster). This proceedure will
	make sure that the cluster is not in pieces.
	
	The algorithm works as follows:
	* Starting at atom 0, take a tree path through each bonding system to see if you can walk though to every atom in the cluster.
	* Get the neighbours of atom 0. these neighbours 
	* If this is not true, then the atom is in some way disconnected and so is not a true cluster.
	'''
	Cluster_paths = [0]
	atoms_not_reached = list(range(len(neighbours_list)))
	while not Cluster_paths == []:
		atom_to_explore = Cluster_paths.pop(0)
		if atom_to_explore in atoms_not_reached:
			atoms_not_reached.remove(atom_to_explore)
		Cluster_paths += neighbours_list[atom_to_explore].bonded_to
		while not neighbours_list[atom_to_explore].bonded_to == []:
			atoms_bonded_to = neighbours_list[atom_to_explore].bonded_to[0]
			neighbours_list[atoms_bonded_to].bonded_to.remove(atom_to_explore)
			neighbours_list[atom_to_explore].bonded_to.remove(atoms_bonded_to)

	if atoms_not_reached == []:
		return False
	else:
		return True

def InclusionRadiusOfCluster(cluster):
	"""
	Find the radius of a sphere that could completely enclose the cluster, with radius from the centre of mass
	to the most outer atom from the centre of mass.
	
	:param cluster: The cluster that the user would like to find the maximum radius from the centre of mass.
	:type  cluster: ASE.Atoms

	:returns: max(size): The radius of the cluster from the from the centre of mass to the most outer atom from the centre of mass (in Angstroms). This radius is for a sphere that will definitely enclose the cluster within.
	:rtype: float
	"""
	'''
	clus = copy.deepcopy(cluster)
	clus.center(vacuum=None, axis=(0, 1, 2), about=0.)
	size = []
	for atom in clus:
		dist = (atom.x*atom.x + atom.y*atom.y + atom.z*atom.z)**(1./2.)
		size.append(dist)
	'''
	max_size = -float('inf')
	for index1 in range(len(cluster)):
		for index2 in range(index1+1,len(cluster)):
			x_dist = cluster[index1].x - cluster[index2].x
			y_dist = cluster[index1].y - cluster[index2].y
			z_dist = cluster[index1].z - cluster[index2].z
			distance_between_atoms = (x_dist**2.0 + y_dist**2.0 + z_dist**2.0)**(0.5)
			if distance_between_atoms > max_size:
				max_size = distance_between_atoms
	return max_size/2.0

'''
def Rounding_Method(number,rounding_criteria):
	"""
	This definition will round the input number to the decimal place specified by rounding_criteria.
	The input number in the genetic algorithm is usually the energy of the cluster.

	:param number: The value that you would like to round (usually energy)
	:type  number: float
	:param rounding_criteria: The number of decimal places the value should be rounded to.
	:type  rounding_criteria: int
	
	"""
	round_by = (10**float(rounding_criteria))
	if rounding_criteria > 12:
		print('Error, the maximum decimal place rounding, to avoid numerical errors, is 12.')
		print('rounding_criteria: '+str(rounding_criteria))
		exit('Check this out. THis progra will finish without completing.')
	number = int(float(number)*round_by)/round_by
	return number
'''

def get_elemental_makeup(cluster):
	"""
	This gives a list which indicates the types of elements, and the number of those elements, in the cluster

	This method has been coped from the def get_elemental_makeup from class Cluster, in Cluster.py

	:returns: A list which indicates the types of elements, and the number of those elements, in the cluster
	:rtype: {str: int, ...} (old output was [[str.,int],...])
	"""
	elements = Counter(cluster.get_chemical_symbols())
	return elements
	'''
	if len(cluster) == 0:
		return [['',0]]
	elements = {}
	for atom in cluster:
		if atom.symbol not in elements:
			elements[atom.symbol] = 1
		else:
			elements[atom.symbol] += 1
	#elements = sorted([[element,number] for element,number in elements.iteritems()], key=lambda x:x[0], reverse=False)
	return elements
	'''

def isinstance_of_dict(dictionary,name_of_dictionary):
	if not isinstance(dictionary,dict):
		print('Error in def isinstance_of_dict/Difference_in_elements, in ExternalDefinitions.py')
		print('The input '+str(name_of_dictionary)+' is not a dictionary.')
		print(str(name_of_dictionary)+' = '+str(dictionary))
		print('Check this out.')
		import pdb; pdb.set_trace()
		exit('This program will finish without completing.')

def AtomInClusterPosition(atom,cluster):
	"""
	This definition will return true if their is an atom already at a particular position in the cluster.
	Prevent two atoms being in the exact same position which local optimisation techniques can not handle.

	Inputs:
		atom (ase.atom): The atom you want to add to the cluster, to check that atom will not be in the same position as any atom in the cluster.
		cluster (ase.atoms or GA.Cluster): The cluster that the atom is to be added to. 
	"""
	for atom_cluster in cluster:
		if atom.x == atom_cluster.x and atom.y == atom_cluster.y and atom.z == atom_cluster.z:
			return True
	return False

def is_position_already_occupied_by_an_atom_in_Cluster(atom_position,cluster,atom_indices_to_exclude_from_comparison=[]):
	"""
	This method determines if two atoms occupy the same position. 

	:param atom_position: The position of the atom, given as (x position, y position, z position). 
	:type  atom_position: (int, int, int)
	:param cluster: The cluster to investigate.
	:type  cluster: GA.Cluster
	:param atom_indices_to_exclude_from_comparison: list of the atom indices not to include in this analysis, THis should include the atom associated with the position list atom_position
	:type  atom_indices_to_exclude_from_comparison: list of int

	"""
	x_pos, y_pos, z_pos = atom_position
	atom_indices_to_check = [index for index in range(len(cluster)) if index not in atom_indices_to_exclude_from_comparison]
	for index in atom_indices_to_check:
		if x_pos == cluster[index].x and y_pos == cluster[index].y and z_pos == cluster[index].z:
			return True
	return False
