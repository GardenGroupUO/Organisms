from ase import Atoms
from ase.io import read as ase_read
from ase.build import add_adsorbate
from ase.data import covalent_radii, vdw_radii, atomic_numbers
from ase.constraints import FixAtoms, FixedLine, FixInternals, ExternalForce
import numpy as np
from math import pi
from ase.calculators.emt import EMT
from ase.optimize import FIRE

class MyConstraint:
    """Constrain an atom to move along a given direction only."""
    def __init__(self, a, direction):
        self.a = a
        self.dir = direction / sqrt(np.dot(direction, direction))

    def adjust_positions(self, atoms, newpositions):
        step = newpositions[self.a] - atoms.positions[self.a]
        step = np.dot(step, self.dir)
        newpositions[self.a] = atoms.positions[self.a] + step * self.dir

    def adjust_forces(self, atoms, forces):
        forces[self.a] = self.dir * np.dot(forces[self.a], self.dir) + 10.0*direction

def get_xy_center(atoms):
	x_min = float(min(atoms.positions,key=lambda position: position[0])[0])
	x_max = float(max(atoms.positions,key=lambda position: position[0])[0])
	y_min = float(min(atoms.positions,key=lambda position: position[1])[1])
	y_max = float(max(atoms.positions,key=lambda position: position[1])[1])
	x_center = (x_max - x_min)/2.0
	y_center = (y_max - y_min)/2.0
	return np.array([x_center, y_center])

def get_distance(atom1,atom2):
	diff_x = atom1.x - atom2.x
	diff_y = atom1.y - atom2.y
	diff_z = atom1.z - atom2.z
	distance = (diff_x**2.0+diff_y**2.0+diff_z**2.0)**0.5
	return distance

class Surface:

	def __init__(self,surface_details):
		# Details about the surface
		if surface_details in [None,'none','None', {}]:
			self.surface = None
			self.place_cluster_where = None
		elif isinstance(surface_details['surface'], Atoms):
			self.surface = surface_details['surface']
		elif isinstance(surface_details['surface'], str):
			self.surface = ase_read(surface_details['surface'])
		else:
			exit('Error')
		if not self.surface == None:
			self.surface.center()
			self.place_cluster_where = surface_details['place_cluster_where']

	def adjust_z_axis(self, cluster):
		if self.surface == None:
			return
		'''
		surface_constraints = []
		for atom in self.surface:
			surface_constraints.append(MyConstraint(atom.index,(0,0,1)))
		'''
		surface_constraints = []
		#surface_constraints.append(ExternalForce(0, 0, 10))
		all_bonds = []
		all_angles = []
		all_dihedrals = []
		for index_1 in range(len(self.surface)):
			for index_2 in range(index_1+1,len(self.surface)):
				bonds_distance = get_distance(self.surface[index_1],self.surface[index_2])
				bond = [bonds_distance, [index_1,index_2]]
				all_bonds.append(bond)
				"""
				for index_3 in range(index_2+1,len(self.surface)): 
					angle_indices = [[index_1,index_2,index_3],[index_3,index_1,index_2],[index_2,index_3,index_1]]
					for angle_indice in angle_indices:
						angle = [self.surface.get_angle(*angle_indice) * pi / 180, angle_indice]
						all_angles.append(angle)
					'''
					for index_4 in range(index_3+1,len(self.surface)):  
						dihedral_indices = [[index_1,index_2,index_3,index_4],[index_1,index_2,index_3,index_4],[index_1,index_2,index_3,index_4]]
						for dihedral_indice in dihedral_indices:
							dihedral = [self.surface.get_dihedral(*dihedral_indice) * pi / 180, dihedral_indice]
							all_dihedrals.append(dihedral)
					'''
				"""
		surface_constraints.append(FixInternals(bonds=all_bonds, angles=all_angles, dihedrals=all_dihedrals))
		#self.surface.set_constraint(surface_constraints)

		c = FixAtoms(indices=range(len(self.surface),len(self.surface)+len(cluster)))
		cluster_constraints = [c]
		#cluster.set_constraint(cluster_constraints)

		for atom in self.surface:
			atom.z -= 40.0

		system = self.surface + cluster
		system.set_calculator(EMT())
		system.set_constraint(surface_constraints+cluster_constraints)
		dyn = FIRE(system)
		converged = False
		import pdb; pdb.set_trace()
		try:
			dyn.run(fmax=0.01,steps=5000)
			converged = dyn.converged()
			if not converged:
				import os
				name = os.path.basename(os.getcwd())
				errorMessage = 'The optimisation of cluster ' + name + ' did not optimise completely.'
				print(errorMessage, file=sys.stderr)
				print(errorMessage)
		except:
			print('Local Optimiser Failed for some reason.')
		import pdb; pdb.set_trace()



	def get_surface(self, cluster):
		if self.surface == None:
			return
		if self == None:
			return
		# find center of xy plane in 
		if self.place_cluster_where == None:
			cluster_xy_center = get_xy_center(cluster)
			surface_xy_center = get_xy_center(self.surface)
			xy_distance_diff = cluster_xy_center - surface_xy_center
			xy_distance_diff = np.append(xy_distance_diff,0.0)
			for atom in self.surface:
				atom.position += xy_distance_diff
		else:
			for index in range(len(self.surface)):
				self.surface[index].x = float(self.surface[index].x) + self.place_cluster_where[0]
				self.surface[index].y = float(self.surface[index].y) + self.place_cluster_where[1]

		self.adjust_z_axis(cluster)
			