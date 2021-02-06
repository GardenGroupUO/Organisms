#!/usr/bin/python

EnergyProfileTXT_path = 'Population/EnergyProfile.txt'
up_to_name = 1
energies = []
restart_points = []
with open(EnergyProfileTXT_path,'r') as EnergyProfileTXT:
	for line in EnergyProfileTXT:
		if line.startswith('Genetic Algorithm Starts Here.'):
			continue
		if line.startswith('Restarting due to epoch.'):
			restart_points.append(clu_dir)
			continue
		if line.startswith('Finished prematurely as LES energy found.'):
			break
		clu_dir, gen, energy = line.rstrip().split()
		clu_dir = int(clu_dir); gen = int(gen); energy = float(energy)
		if not up_to_name == clu_dir:
			exit('Error')
		up_to_name += 1
		energies.append(energy)
