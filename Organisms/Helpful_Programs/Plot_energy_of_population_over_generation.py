#!/usr/bin/python

EnergyProfileTXT_path = 'Population/Population_history.txt'
recorded_current_population_no = 1
all_energies = []
restart_generations = []
restart_generations_plot_marker = []
no_of_restarts = 0
with open(EnergyProfileTXT_path,'r') as EnergyProfileTXT:
	for NOUSED in range(5):
		EnergyProfileTXT.readline()
	counter = 0
	for line in EnergyProfileTXT:
		if '#-----------------------------------------------------------------------------' in line:
			continue
		elif 'Reset population as reached epoch' in line:
			print('Population Restarted')
			restart_generations.append(current_generation_no)
			restart_generations_plot_marker.append(current_generation_no+no_of_restarts+0.5)
			no_of_restarts += 1
			continue
		if counter == 0:
			current_generation_no = int(line.replace('GA Iteration:',''))
			print('Generation: '+str(current_generation_no))
			if current_generation_no == recorded_current_population_no:
				exit('Error')
			recorded_current_population_no += 1
		elif counter == 1:
			line.replace('Clusters in Pool:\t','').split()
		elif counter == 2:
			energies = tuple(float(energy) for energy in line.replace('Energies of Clusters:\t','').split())
			all_energies.append(energies)
			counter = -1
		counter += 1

plot_names = []
plot_energies = []
for index in range(len(all_energies)):
	energies = all_energies[index]
	plot_names += [index+1]*len(energies)
	plot_energies += energies

# Make plot.
import matplotlib.pyplot as plt
plt.scatter(plot_names, plot_energies, s=2, c='b', alpha=0.5)
plt.xlabel('Generation')
plt.ylabel('Energy')
plt.tight_layout()
plt.savefig('energy_of_population_over_generation.png')