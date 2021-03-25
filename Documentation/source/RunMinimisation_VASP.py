import os, time
from ase.io import write as ase_write
from ase.io import read as ase_read
from shutil import copyfile
from subprocess import Popen

def Minimisation_Function(cluster,collection,cluster_name):
	#######################################################################################
	cluster.pbc = True # make sure that the periodic boundry conditions are set off
	#######################################################################################
	# Perform the local optimisation method on the cluster.
	original_path = os.getcwd()
	offspring_name = str(cluster_name)
	clusters_to_make_name = 'clusters_for_VASP'
	if not os.path.exists(clusters_to_make_name):
		os.makedir(clusters_to_make_name)
	copyfile('VASP_Files/INCAR',clusters_to_make_name+'/'+offspring_name+'/INCAR')
	copyfile('VASP_Files/POTCAR',clusters_to_make_name+'/'+offspring_name+'/POTCAR')
	copyfile('VASP_Files/KPOINTS',clusters_to_make_name+'/'+offspring_name+'/KPOINTS')
	os.chdir(clusters_to_make_name+'/'+offspring_name)
	ase_write(cluster,'POSCAR','vasp')
	startTime = time.time();
	try:
		Popen(['srun','vasp'])
	except Exception:
		pass
	endTime = time.time()
	cluster = ase_read('OUTCAR')
	os.chdir(original_path)
	####################################################################################################################
	# Write information about the algorithm
	Info = {}
	Info["INFO.txt"] = ''
	#Info["INFO.txt"] += ("No of Force Calls: " + str(dyn.get_number_of_steps()) + '\n')
	Info["INFO.txt"] += ("Time (s): " + str(endTime - startTime) + '\n')
	#Info["INFO.txt"] += ("Cluster converged?: " + str(dyn.converged()) + '\n')
	####################################################################################################################
	return cluster, converged, Info