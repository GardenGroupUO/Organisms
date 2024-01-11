
.. _HelpfulPrograms_GatherAndPostprocessingData:

Helpful Programs for Gathering data and Post-processing Data
############################################################

As well as including programs for creating and running mass numbers of genetic algorithm, we have also included scripts and programs to gather and process the data across all the set of repeated genetic algorithm runs. In this article, we will introduce all of the program that can be used to run these programs.  These programs can be run by typing the program you want to run into the terminal from whatever directory you are in. 

The scripts and programs that we will be mentioned here are:

.. contents::
    :depth: 1
    :local:

What to make sure is done before running any of these scripts. 
**************************************************************

If you installed Organisms through pip3
---------------------------------------

If you installed the Organisms program with ``pip3``, these scripts will be installed in your bin. You do not need to add anything into your ``~/.bashrc``. You are all good to go. 

If you performed a Manual installation
--------------------------------------

If you have manually added this program to your computer (such as cloning this program from Github), you will need to make sure that you have included the ``Postprocessing_Programs`` folder into your ``PATH`` in your ``~/.bashrc`` file. All of these program can be found in the ``Postprocessing_Programs`` folder. To execute these programs from the ``Postprocessing_Programs`` folder, you must include the following in your ``~/.bashrc``:

.. code-block:: bash

	export PATH_TO_GA="<Path_to_Organisms>" 

where ``<Path_to_Organisms>"`` is the path to get to the genetic algorithm program. Also include somewhere before this in your ``~/.bashrc``:

.. code-block:: bash

	export PATH="$PATH_TO_GA"/Organisms/Postprocessing_Programs:$PATH

See more about this in :ref:`Installation of the Genetic Algorithm <Installation_of_the_Genetic_Algorithm>`. 

``Did_Complete.py`` - Have all your genetic algorithm trials completed?
***********************************************************************

This program is the first program that you should use before continuing on with any analysis. It is a quick program that will scan through all the trials, and check to see if they have completed.

To use this program, you want to enter into into the terminal

.. code-block:: bash

	Did_Complete.py

in the directory that you ran your MakeTrials.py script from. You can also enter ``Did_Complete.py`` into the terminal within any folders, as long as at some point it will find the Trials in the subdirectories that you ran.

``Did_Find_LES.py`` - Did all your genetic algorithm trials find the global minimum?
************************************************************************************

This program is designed to determine which of the trials you can found the global minimum that you were searching for. To run this program, enter ``Did_Find_LES.py`` into the terminal at any directory you want. This program will go through all subdirectories in search for folders that start with ``Trial``, and look through the result to see if the global minimum you are looking for has been found for each trial run.

More specifically, this algorithm looks for any entries in the EnergyProfiles.txt files for each trial of clusters that are of a certain energy to a certain number of decimal places. 

This program will ask the user what the energy is of the cluster that the user wants to locate in each trial, the number of decimal places that the user wants to round the energy to, and the number of generations the user wants to means the genetic algorithm trials up to (If this is not given, the algorithm will look through every generation). 

Each set of trials is measured individually for different genetic algorithms in different folders. 

``GetLESOfAllTrials.py`` - Get information of generations and number of minimisations performed
***********************************************************************************************

This program is designed to obtain information about the generation and the number of minimisations performed to first obtain the lowest energy clusters each trial had found. This algorithm will also report the average number of generations and average number of minimisation performed across all the trials that had found the lowest of the lowest energy clusters those trials had found. For example, if 5 of 20 genetic algorithm trials found the a cluster with the same energy and this cluster was lower in energy than the lowest energy clusters found from the other 15 trials, then the average number of generations and minimisations is taken for those 5 that had found the lowest of the lowest energy clusters.

You can run this program by typing ``GetLESOfAllTrials.py`` in the terminal in any folder. This program will search through all subdirectories for folders that start with the name ``Trial``, and report on those genetic algorithm trials found in the same folder (being apart of the same set of genetic algorithm trials). The algorithm will ask for two pieces of information:

* The generation you would like to search up to (Default: The full genetic algorithm until the LES has been found or the genetic algorithm has successfully finished). 
* The number of decimal places to round the energy to (Default: 2 decimal places). 

You can also enter this in the terminal when you type in ``GetLESOfAllTrials.py``:

.. code-block:: bash

	GetLESOfAllTrials.py maximum_generation_to_sample_up_to

where the number of decimal places to run the genetic algorithm to is given as 2 decimal places (this is the default), or you can enter into the terminal

.. code-block:: bash

	GetLESOfAllTrials.py maximum_generation_to_sample_up_to number_of_decimal_places_to_round_the_energy_to

Each set of trials is measured individually for different genetic algorithms in different folders. This program should be run **after all genetic algorithm trials have successfully finished**. 

.. _Postprocessing_Database:

``Postprocessing_Database.py`` and ``Postprocessing_Many_Databases_Together.py`` - For breaking a large database into smaller chunks
************************************************************************************************************************************

If a database (such as the storage database in ``Recorded_Data/GA_Recording_Database.db``) is too big to process with ``ase db``, this program is designed to break up the database into smaller databases which can be better handled by ``ase db`` and your computer. This program will sort these clusters before placing them in the separate, potentially smaller databases. This program will also rotate the cluster so that the principle axis of inertia points along the z axis.

To run this program, first move into the ``Recorded_Data`` folder in the terminal, then run the ``Postprocessing_Database.py`` program in the terminal. There are two parameters that need to be entered. These are:

* **number_of_clusters_per_database** (*int*): This is the maximum number of clusters you would like in each database. 
* **sort_clusters_by** (*str.*): This tells the program how you would like clusters sorted in this(these) database(s). 

You can also enter this in the terminal when you type in ``Postprocessing_Database.py``:

.. code-block:: bash

	Postprocessing_Database.py number_of_clusters_per_database

where the number of decimal places to run the genetic algorithm to is given as 2 decimal places (this is the default), or you can enter into the terminal

.. code-block:: bash

	Postprocessing_Database.py number_of_clusters_per_database sort_clusters_by

.. _Postprocessing_Many_Databases_Together:

``Postprocessing_Many_Databases_Together.py`` - For compiling all databases from all your trials together and breaking them up into smaller chunks if needed
************************************************************************************************************************************************************

If you have performed many genetic algorithm trials and have created many ``Recorded_Data/GA_Recording_Database.db`` databases for your genetic algorithm trials, you can use the ``Postprocessing_Many_Databases_Together.py`` program to compile all the clusters you recorded across all your genetic algorithm trials together. 

**This is the recommeneded program to use if you want understand all the various geometries of a cluster.**

To run this program, first move into the folder that contains your ``Trials`` folders, then run the ``Postprocessing_Many_Databases_Together.py`` program in the terminal. There are two parameters that need to be entered. These are:

* **number_of_clusters_per_database** (*int*): This is the maximum number of clusters you would like in each database. 
* **sort_clusters_by** (*str.*): This tells the program how you would like clusters sorted in this(these) database(s). 

You can also enter this in the terminal when you type in ``Postprocessing_Many_Databases_Together.py``:

.. code-block:: bash

	Postprocessing_Database.py number_of_clusters_per_database

where the number of decimal places to run the genetic algorithm to is given as 2 decimal places (this is the default), or you can enter into the terminal

.. code-block:: bash

	Postprocessing_Database.py number_of_clusters_per_database sort_clusters_by

.. _database_viewer:

``database_viewer.py`` - Viewing GA databases with ASE database website viewer with metadata
********************************************************************************************

The databases that are created by the Organisms program has metadata that allows the clusters to be organised in the database by their energy. The metadata also contains information about all the variables included in the database for the users convenience. However, in recent versions of ASE the metadata is not included when using the website. ``database_viewer`` allows the metadata to be included in the ASE website viewer.

This program is run by the user moving into the ``Recorded_Data`` folder in the terminal and running the ``database_viewer.py`` program. There is one parameter that need to be entered. This is:

* **name_of_the_database** (*str.*): This is the name of the database that you want to view.

Enter this into the terminal when you type in ``database_viewer.py``:

.. code-block:: bash

	database_viewer.py name_of_the_database


.. _make_energy_vs_similarity_results:

``make_energy_vs_similarity_results.py`` - For analysing the genetic algorithm under-the-hood
*********************************************************************************************

It is often useful to understand how the genetic algorithm procedure during the global optimisation of a cluster. This is especially useful if you are wanting to analyse the efficiency of the genetic algorithm. We have created a program that can help to get under the hood of the Organisms program and understand what clusters the genetic algorithm was obtaining. This creates a series of energy vs similarity plots that act as a way of observing clusters created on the potential energy surface. See more information about the *make_energy_vs_similarity_results.py* program at :ref:`Information about using the make_energy_vs_similarity_results.py script <make_energy_vs_similarity_results_documentation>`. 


``remove_blank_arrayJobs.py`` - For removing blank ``arrayJob`` output and error files outside of ``Trials`` folders
********************************************************************************************************************

If you have been making lots of repeated trials using the ``MakeTrials.py`` script and all your runs have completed, you will find that you will have a lot of ``arrayJob`` files that are empty. This is because all the trials have completed and the data from the ``arrayJob`` output and error files has been moved into the respective Trial folder. This program is designed to remove these blank ``arrayJob`` files.

When you run this program, it will look into every subfolder for the folder that contains all the Trial folders. It will then look to see if the ``arrayJob`` files are blank or not. The blank ``arrayJob`` files will be removed. 

Note that it will not delete ``arrayJob`` files that are within trials folders. This is any folder that is named ``TrialX``, where ``X`` is an integer.



``remove_overall_arrayJobs.py`` - For removing all ``arrayJob`` output and error files outside of ``Trials`` folders
********************************************************************************************************************

This program will remove all ``arrayJob`` output and error files that are found alongside ``Trials`` folders. 

To run this program, go into the folder that your genetic algorithms have been run in and type ``remove_overall_arrayJobs.py`` into the terminal. This program will look into all the subdirectories for those folders that contain your ``Trials`` folders. It will then delete all the ``arrayJob`` output and error files that are alongside your ``Trials`` folders. 

Note that it will not delete ``arrayJob`` files that are within trials folders. This is any folder that is named ``TrialX``, where ``X`` is an integer.


``tar_trials_collectively.py`` - Tar all ``Trials`` folders (and other files and folders)
*****************************************************************************************

This program will recursively tar all subdirectories that include ``Trials`` folders. For example, if the folder called ``OffPerGenEquals16`` contains ``Trial1``, ``Trial2``, ``Trial3``, ``Trial4``, ``Trial5``, ``Run.py``, ``RunMinimisation.py``, ``mass_submit.sl``, this program will tar ``OffPerGenEquals16`` and everything in it into the tar file called ``OffPerGenEquals16.tar`` in the same place as where ``OffPerGenEquals16`` had originally been found. 

This program will also delete the Trials folders, since they have all been tarred up. Files and folder will not be deleted if you enter into the terminal:

.. code-block:: bash

	tar_trials_collectively.py False

``untar_trials_collectively.py`` - Untar all ``Trials`` folders (and other files and folders)
********************************************************************************************************************

This program will recursively untar all subdirectories that contain a tar file, and will untar the tar file in place. This is useful for untar tar files that were made using ``tar_trials_collectively.py``

This program will also delete the tar files in the process. Tar files will not be deleted if you enter into the terminal 

.. code-block:: bash

	untar_trials_collectively.py False














