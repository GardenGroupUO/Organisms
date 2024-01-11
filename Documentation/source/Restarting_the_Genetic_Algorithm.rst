.. _Restarting_the_Genetic_Algorithm:

Restarting the Genetic Algorithm
################################

The algorithm has been designed to record all the relavant information required to restart the algorithm from the last previously successful generation. The genetic algorithm by default records all the data it needs to disk, however, making files for backing up can be turned off or change to record only after so many generations if desired. If you do need to restart the genetic algorithm, you only need to run your ``Run.py`` file by running ``python3 Run.py`` in the terminal. You do not need to change any files and it is **recommended you do not change any genetic algorithm files** (unless the genetic algorithm does not restart properly, which in that case you may want to play around with files for debugging reasons. However, if the genetic algorithm is working properly you should not need to do this). The genetic algorithm will change or update any files that it needs to. Just sit back and let the python program do all the work for you. 

Requirements for Restarting the Genetic Algorithm
=================================================

To be able to restart this genetic algorithm, the algorithm will write the following files to disk after each generation: 

* ``epoch_data`` - This contains information that is needed to know about epoching. This file is formatted differently for each epoch method. It is not created if you do not choose to epoch during your genetic algorithm. See :ref:`Using Epoch Methods <Using_Epoch_Methods>` for more information about this file.
* ``Population/Population.db`` - This is a ASE database that contains all the structural and energy information about clusters in the population. Always required. See :ref:`Recording Clusters From The Genetic Algorithm <Recording_Clusters_From_The_Genetic_Algorithm>` for more information about recording clusters created during the genetic algorithm. 
* ``Population/current_population_details.txt`` - This contain information about the current generation, and the names and energies of the clusters in the population at that generation. Always required. 
* ``Population/EnergyProfile.txt`` - This file contains all the information of the clusters that were created at any point during the genetic algorithm, whether they were placed into the population or if they were excluded because they violated the predation operator. Always required. 
* ``Population/Population_history.txt`` - This file contains all the information about the population after every generation. Always required. 
* ``Recorded_Data/GA_Recording_Database.db`` - This contains the clusters that were created during a genetic algorithm. This file will only be created if the user wants to record clusters created during the genetic algorithm. See :ref:`Recording Clusters From The Genetic Algorithm <Recording_Clusters_From_The_Genetic_Algorithm>` for more information about recording clusters created during the genetic algorithm. 

These four to six files are required (depending on your epoch and recording clusters settings) and must have been created at the same generation for the genetic algorithm to proceed. The algorithm will not proceed is any of these files is missing or any information about these files causes issues and confusions for the genetic algorithm. 

Also, backups of the ``Population/Population.db``, ``Population/current_population_details.txt``, and the ``epoch_data`` files are created before beginning a generation. This means that is anything goes wrong that these backup files are available for the genetic algorithm to use. Generally, this genetic algorithm will first look for these backup files and get information from them, since it is know that these files should contain all the required information and should not be corrupted. The non-backup files are generally created at different points during the generation, so can be corrupt or contain information that is inconsist with each other if the algorithm was abruptly cancelled during a generation. However, if a generation finished successfully without any issues, these backup files are removed after every generation. In these cases there will be no backup files, and the genetic algorith will look for the non-backup files. 

Files that are updated when restarting the genetic algorithm
============================================================

There are three other files that are updated by the genetic algorithm if they contain information about clusters obtained from an unsuccessful generation. These are:

* ``Population/EnergyProfile.txt`` - This file contains all the information of the clusters that were created at any point during the genetic algorithm, whether they were placed into the population or if they were excluded because they violated the predation operator
* ``Population/Population_history.txt`` - This file contains all the information about the population after every generation. 
* ``Recorded_Data/GA_Recording_Database.db`` - This contains the clusters that were created during a gentic algorithm. See :ref:`Recording Clusters From The Genetic Algorithm <Recording_Clusters_From_The_Genetic_Algorithm>` for more information about recording clusters created during the genetic algorithm. 

The ``GA_Recording_Database.db`` is not backed-up after every generation. This is because this file can get quite large and would continuously increase the computational time for performing each generation. For this reason, this file is not continuously backed-up. There are rarely problems with this database file. 
