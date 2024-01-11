
.. _Files_Made_During_the_Genetic_Algorithm:

Files Made During the Genetic Algorithm
=======================================

There are a number of files and folders that are created as the Organisms program runs. Some of these will always be created, some of these are created depending on if certain settings are given in your ``Run.py`` script. 

Files and Folders that are Always Made
--------------------------------------

The following files and folders will always be created and modified as your genetic algorithm runs. These files and folders are:

* ``GA_Run_Details.txt``: This file contains data about how the algorithm ran. Currently is just set up to measure the amount of time each generation took. This is the time including epoching if epoching occurs. If an epoch occurs, the amount of time required to perform an the epoch will also be given. 
* ``Population``: This is a folder that contains all the information required about the population. In it includes:

	- ``EnergyProfile.txt``: This contains the energies of each cluster that was created and the generation it was created in. Cluster in this file also include offspring that were not included in the population. 
	- ``Population_history.txt``: This contains the information of the clusters that are in the population after each generation, as well as the energies of those clusters and the generations when clusters were originally accepted into the population. 
	- ``current_population_details.txt``: This is a file that contains the information about all the clusters in the current population, as well as the energy of the cluster and the generation that the clusters was accepted into the population. This file has the same format as the ``Population_history.txt``. The reason that this file is created is because it makes resuming Organisms midway through a genetic algorithm easy (in regards to programming) and quick. 
	- ``Population.db``: This is a ASE database file that contains all the clusters that are in the current population. 

backups of these files are also created during the genetic algorithm before starting a new generation. These are deleted when a generation has finished. Backup files end with ``.backup``.

Files and Folders made when Epoching
------------------------------------

The files that are made if you include epoching in your genetic algorithm are:

* ``epoch_data``: This file contains all the information needed if one wants to resume a genetic algorithm where epoching is involved. 

You may also see a ``epoch_data.backup`` file. This contains epoching information about the previous generation. 

See :ref:`Using_Epoch_Methods` for more information about Epoching and files created during genetic algorithms involving epochs.

Files and Folders made when Recording Clusters Created during a Genetic Algorithm
---------------------------------------------------------------------------------

The files that are made if you include recording created clusters in your genetic algorithm are:

* ``Recorded_Data/GA_Recording_Database.db``: This database include all the clusters that were created and saved during the genetic algorithm. 

See :ref:`Recording_Clusters_From_The_Genetic_Algorithm` for more information about recording clusters created during the genetic algorithm and the files created during this process.