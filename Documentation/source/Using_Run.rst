
.. _Using_Run:

*Run.py* - Running the Genetic Algorithm
########################################

In this article, we will look at how to run the genetic algorithm. This program is run though the **Run.py** script, which includes all the information on what cluster to globally optimise and the genetic algorithm settings to use. You can find other examples of ``Run.py`` files at `github.com/GardenGroupUO/Organisms <https://github.com/GardenGroupUO/Organisms>`_ under ``Examples\Playground`` and ``Examples\Example_Run_Files``. Also, you can try out this program by running an example script through a Jupyter notebook. See :ref:`Examples_of_Running_GA` to get access to examples of running Organisms through this Jupyter notebook!

.. contents::
    :depth: 2
    :local:

Running the Genetic Algorithm Program
*************************************

We will explain how the Run.py code works by running though the example shown below:

.. literalinclude:: Run.py
	:language: python
	:caption: Run.py
	:name: Run.py
	:tab-width: 4
	:linenos:

Lets go through each part of the Run.py file one by one to understand how to use it. 

1) The elemental makeup of the cluster
======================================

The first part of Run.py specifies the type of cluster you will be testing. Here, the makeup of the cluster is described using a dictionary in the format, {element: number of that element in the cluster, ...}. An example of this is shown below:

.. literalinclude:: Run.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 3
	:lines: 3-4

2) Details if the cluster lies on a surface
===========================================

This feature allows the user to include a surface to place a cluster upon. This feature is still being developed and does not currently work.

.. literalinclude:: Run.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 6
	:lines: 6-7

3) The main details of the genetic algorithm
============================================

Here, the components of the genetic algorithm are described below:

* **pop_size** (*int*): The number of clusters in the population.
* **generations** (*int*): The number of generations that will be carried out by the genetic algorithm.
* **no_offspring_per_generation** (*int*): The number of offspring generated per generation.

It is recommended that for a particular test case that one try a few variations for pop_size and no_offspring_per_generation. From the literature, an pop_size = 30 or 40 and no_offspring_per_generation set to ``0.8*pop_size`` is common. 

An example of these parameters in Run.py is given below:

.. literalinclude:: Run.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 9
	:lines: 9-12

4) Details concerning the Mating and Mutation Proceedure
========================================================

The following set of parameters are focused on settings that involve the Mating and Mutation Procedures of the genetic algorithm. These are processes that affect how new offspring are created during the genetic algorithm. There are four sets of parameters involving the Mating and Mutation Procedures. Firstly, below is a parameter that affects both the Mating and Mutation Procedures:

* **creating_offspring_mode** (*str.*): This indicates how you want these procedures to work when making an offspring. There are two options:
		
		* ``"Either_Mating_and_Mutation"`` - the genetic algorithm will perform **either** a mating or mutation proceedure to obtain the offspring.
		* ``"Both_Mating_and_Mutation"`` - the genetic algorithm will perform **both** a mating and mutation proceedure to obtain the offspring. Here, the mating scheme will always occur, however there is only a chance that the mutation scheme will occur.

* **crossover_type** (*str.*): The mating method will use the spatial information of two parent clusters to create a new cluster from the two of them. This variable determines which mating proceedure the genetic algorithm will perform. 

		* ``"CAS_weighted"``: *Deavon and Ho Weighted Cut and Splice Method* - The cut and splice method, weighted by fitness of parents.
		* ``"CAS_half"``:     *Deavon and Ho Half Cut and Splice Method*     - The cut and splice method, where poth parents are in half (recommended from experience).
		* ``"CAS_random"``:   *Deavon and Ho Random Cut and Splice Method*   - The cut and splice method, where one parent is cut a random percent x%, while the other parent is cut by (100-x)%. The value of x changes each time it is used to a random number between 0% and 100% (recommended for LJ98 clusters).
		* ``"CAS_custom_XX"``:  *Deavon and Ho Custom Cut and Splice Method*   - The cut and splice method, where one parent cut a set percent XX% and the other parent is cut by (100-XX)%. Here, XX is a value that is set by the user. To use this, set crossType = CAS_custom_XX, where XX is a float of your choice between 0 and 100.

* **mutation_types** (*[[str.,float],...]*): The mutation method will change the structure of a cluster to give a new cluster as a result. The type of mutation method the user would like to use. This can one of the following:	

	* ``"random"``: This will completely erase the previous cluster and generated a new cluster, where atoms have been placed randomly within the cluster
	* ``"random_XX"``: This will randomly place XX percent of the atoms in the cluster to new positions in the cluster. (Make this more clear what is going on later)
	* ``"move"``: This will move all the atoms in the cluster from their original positions by a maximum default distance equal to r_ij*0.5 Å.
	* ``"move_XX"``: This will move all the atoms in the cluster from their original positions by a maximum distance XX Å.
	* ``"homotop"``: This will swap the positions of two atoms that are of a different element. This mutation method can not be used for monometallic clusters.

	It is possible for more than one mutation method to be used. For this reason, the format for mutTypes is [[Type of Mutation,chance of mutation],...]. Here, all the chances of mutations should add up to 1.0. For example, "mutTypes = [[random, 0.45], [move, 0.225], [random_33.33, 0.325]]" is acceptable as all the chances of mutations add up to 1.0 (0.45 + 0.225 + 0.325 = 1.0).

* **chance_of_mutation** (*float*): The chance that a mutation will occur. How the genetic algorithm uses this variable depends on the input for creating_offspring_mode. If:

		* ``creating_offspring_mode = "Either_Mating_and_Mutation"`` - chance_of_mutation is the chance that a mutation will occur rather than a mating scheme.
		* ``creating_offspring_mode = "Both_Mating_and_Mutation"`` - chance_of_mutation is the chance that a mutation will occur. The mating scheme will always occur when ``creating_offspring_mode = "Both_Mating_and_Mutation"``.

An example of these parameters used in the Run.py file is given below:

.. literalinclude:: Run.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 14
	:lines: 14-18

5) Epoch Settings
=================

It is possible to include a epoch in this version of the genetic algorithm. An epoch is a feature that allows the population to be reset with new, randomly generated clusters. See :ref:`Using Epoch Methods <Using_Epoch_Methods>` for more information on epoch methods, including the various types of epoches and settings. 

An example of the epoch parameters used in the Run.py file is given below:

.. literalinclude:: Run.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 20
	:lines: 20-21

6) Other Details
================

There are three other variables which are important to include in your Run.py file. These are:

* **r_ij** (*float*): This is the maximum bond distance that we would expect in this cluster. This parameter is used when clusters are created using either or both the mating or mutation schemes. This parameter is used to determine if a cluster has stayed in one piece after the local minimisation, as it is possible for the cluster to break into multiple pieces. This should be a reasonable distance, but not excessively large. For example, for Au, which has a FCC lattice constant of 4.078 Å. Therefore it has a first nearest neighbour of 2.884 Å and a second nearest neighbour of 4.078 Å. Therefore r_ij should be set to some value between 2.884 Å and 4.078 Å. For example, r_ij = 3.5 Å or r_ij = 4.0 Å would probably be appropriate, however I have been able to get away with r_ij = 3.0 Å. ``r_ij`` is given in Å.
* **cell_length** (*float*): If you are wanting to create randomly generated clusters, either at the start of the genetic algorithm or using the 'random' mutation method, then you will want to specify the length of the box that you want to add atoms to. boxtoplaceinlength is the length of this box. Don't make this too big, or else it is likely atoms will be too far apart and a cluster will be broken into multiple pieces. ``cell_length`` is given in Å.
* **vacuum_to_add_length** (*float*): The length of vacuum added around the cluster. This variable is only used to aesthetics reasons. How the genetic algorithm records clusters for databases is to take the *locally optimised* cluster and measure its radius. A new cell is then created with cell length that is twice the radius of the cluster. The cluster is then placed in this new cell, and a vacumm of ``vacuum_to_add_length`` is then added to this new cell. The reason for taking the radius of the cluster to make a cell is so that no matter if and how you rotate the cluster for post processing, you can be assurred that the cluster will always have a vacuum of at least ``vacuum_to_add_length`` Å. This is important especially if you reoptimise the cluster with periodic potential such as VASP where it is vital that a minimum vacuum is given to prevent reoptimisation issues from occurring. ``vacuum_to_add_length`` is given in Å.

An example of these parameters used in the Run.py file is given below:

.. literalinclude:: Run.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 23
	:lines: 23-26

.. _Using_Run_Minimisation_Scheme:

7) Minimisation Scheme
======================

This component of Run.py focuses on the function/method that the genetic algorithm uses for performing local minimisations. This is used by the genetic algorithm as a def type (i.e. as a function). This means that, rather than a variable being passed into the algorithm, a function is passed into the algorithm. 

One can write this function into the Run.py file, however it is usually easier and nicer to view this function in a different python file. I typically call this something like RunMinimisation.py, and the function in this file is called Minimisation_Function. Minimisation_Function will contain the algorithm for performing a local optimisation. 

Because of the flexibility, it is possible to use any type of calculator from ASE, ASAP, GWAP, LAMMPS, etc. It is even possible for the user to design this to use with non-python user-interface based local optimisers, such as VASP or Quantum Espresso! 

To see an example of how to write Minimisation_Function, see :ref:`Writing a Local Minimisation Function for the Genetic Algorithm <Local_Minimisation_Function>`.

The algorithm is imported into Run.py as follows:

.. literalinclude:: Run.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 28
	:lines: 28-31

8) The Memory Operator
======================

This operator is designed to prevent clusters from being in the population that resemble any cluster in this memory operator in some way. This operator uses the SCM to determine how structurally similar cluster are. See :ref:`Using the Memory Operator <Using_the_Memory_Operator>` for more information on how to use the memory operator. An example of how the memory operator is written in the Run.py file is shown below.

.. literalinclude:: Run.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 33
	:lines: 33-34

9) Predation Operators
======================

This component of Run.py specifies all the information concerning the predation operator. You can see more about how the predation operators works at :ref:`Using Predation Operators with the Genetic Algorithm <Using_Predation_Operators>`.

In terms of the Run.py file, there is only one variable that we need to deal with, predation_information. This variable is a dictionary type, {}, which holds all the information that would been needed for the predation operator that the user wishes to use. For example:

.. code-block:: python

	predation_information = {'Predation_Switch': 'SCM', 'SCM Scheme': 'T-SCM', 'rCut_high': 3.2, 'rCut_low': 2.9, 'rCut_resolution': 0.05}

There are a variety of predation operators that are inbuilt currently into the genetic algorithm. You can find out more about what they do, and how to use them in your Run.py file, at :ref:`Using Predation Operators with the Genetic Algorithm <Using_Predation_Operators>`.

Below are some other examples of the inputs required for the other types of predation operators available. **Please see** :ref:`Using Predation Operators with the Genetic Algorithm <Using_Predation_Operators>` **before using these predation operators**.

.. literalinclude:: Run.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 36
	:lines: 36-42

10) Fitness Operators
=====================

This component of Run.py specified all the information required by the fitness operators. You can find more information about how the fitness operators works at :ref:`Using Fitness Operators with the Genetic Algorithm <Using_Fitness_Operators>`.

In the Run.py file, all the setting for the fitness operator are contained in the dictionary called fitness_information. For example:

.. code-block:: python

	fitness_information = {'Fitness Operator': 'Energy', 'fitness_function': energy_fitness_function}

There are a variety of fitness scheme available to be used in this implementation of the genetic algorithm. You can find all the information about all the available fitness schemes in :ref:`Using Fitness Operators with the Genetic Algorithm <Using_Fitness_Operators>`.

An example of how the fitness scheme is written in the Run.py file is shown below. **Please see** :ref:`Using Fitness Operators with the Genetic Algorithm <Using_Fitness_Operators>` **before using these fitness operators**. 

.. literalinclude:: Run.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 44
	:lines: 44-50

11) Recording Clusters from the Genetic Algorithm
=================================================

This input in the Run.py file indicates how the user would like to record clusters that are created during the genetic algorithm. The information is contained in the dictionary called ga_recording_information. There are six parameters that the user can set. These are:

* ga_recording_scheme
* limit_number_of_clusters_recorded
* limit_energy_height_of_clusters_recorded
* exclude_recording_cluster_screened_by_diversity_scheme
* saving_points_of_GA
* record_initial_population

Not all of these parameters need to be entered. If the user does not enter in any of these parameters, the genetic algorithm will not keep a record of the clusters that were obtained. 

More information on how to record clusters made during the genetic algorithm can be found at :ref:`Recording Clusters From The Genetic Algorithm <Recording_Clusters_From_The_Genetic_Algorithm>`.

An example of the ``'ga_recording_information'`` variable in the Run.py file is shown below. **Please see** :ref:`Recording Clusters From The Genetic Algorithm <Recording_Clusters_From_The_Genetic_Algorithm>` **before using this feature to record clusters obtained during the genetic algorithm**. 

.. literalinclude:: Run.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 52
	:lines: 52-59

.. _Other_details_of_the_Genetic_algorithm:

12) Other details of the Genetic algorithm
===========================================

These last set of parameters are important, but there is no good appropriate place to put them in the Run.py file. These last parameters are:

* **force_replace_pop_clusters_with_offspring** (*bool*): In the genetic algorithm, the predation operator may find that the an offspring is "identical" to a cluster in the population, but that offspring is more fit than the cluster in the population. In this case, the genetic algorithm can replace the less fit cluster in the population with the "identical" more fit offspring. Set this variable to ``True`` if you want this to happen. Set this variable to ``False`` if you don't want this to happen. Default: ``True``. 
* **user_initilised_population_folder** (*str.*): This is the name, or the path to, the folder holding the initalised population that you would like to use instead of the program creating a set of randomly generated clusters. If you do not have, or do not want to use, an initialised population, set this to ``None`` or ``''``.
* **rounding_criteria** (*int*): This is the round that will be enforced on the value of the cluster energy. Default: ``2``
* **print_details** (*bool*): Will print the details of the genetic algotithm, like a verbose. 
* **no_of_cpus** (*int*): This is the number of cpus that you would like the algorithm to run on. These extra cores will be used to create the offspring as well as used by the predation and fitness operators if beneficial to use extra cores for the chosen operators.
* **finish_algorithm_if_found_cluster_energy** (*dict.*): This parameter will stop the algorithm if the desired global minimum is found. This parameter is to be used if the user would like to test the performance of the algorithm and knows beforehand what the energy of the global minimum is. This parameter is set as a dictionary as two parameters. **'cluster energy'** is a float that states the energy of the global minimum. **'round'** is an interger that you want to set to the same rounding that you gave for the 'cluster energy' input. This will round the energy of clusters made, and compare this energy to your 'cluster energy' input. An example of this for Au38 using Cleri Gupta parameters are ``finish_algorithm_if_found_cluster_energy = {'cluster energy': -130.54, 'round': 2}``. If you are not testing the performance of the algorithm, or dont know the global minimum of the cluster you are testing, set ``finish_algorithm_if_found_cluster_energy = None``. Default: ``None``

.. _total_length_of_running_time:

* **total_length_of_running_time** (*int*): This is the maximum amount of time (in hours) that the algorithm is allow to run for. This variable is useful if you are running on a remote computer system like slurm that finishes once a certain time limit is reached. To prevent the algorithm from being incorrectly cancelled when running, set this value to a time limit less than your maximum time limit on slurm. I have been setting this to the slurm job time minus 2 hours. For example, if the genetic algorithm is submitted to slurm for 72 hours, set ``total_length_of_running_time=70.0``. While this algorithm is designed to be able to be restarted even if the program is cancelled during a generation, it is best to prevent any issues from occurring by using this variable to cancel the algorithm safety so that there are absolutely no issues when restarting the genetic algorithm. Is ``None`` is given, no time limit will be set. Default: ``None``

An example of how they are written in the Run.py file are show below:

.. literalinclude:: Run.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 61
	:lines: 61-68

The Genetic Algorithm!
======================

You have got to the end of all the parameter setting stuff! Now on to the fun stuff! The next part of the Run.py file tells the genetic algorithm to run. This is written as follows in the Run.py:

.. literalinclude:: Run.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 71
	:lines: 71-96