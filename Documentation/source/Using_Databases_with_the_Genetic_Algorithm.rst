
.. _Using_Databases_with_the_Genetic_Algorithm:

Using Databases with the Genetic Algorithm
==========================================

The genetic algorithm has been designed to create database files that are designed to hold data about the clusters that are created during the genetic algorithm. See `Databases in ASE <https://wiki.fysik.dtu.dk/ase/ase/db/db.html>`__ for information about how databases generally work in ASE. 

There are a few databases that can be created during the genetic algorithm. First is the ``Population\Population.db`` database. This database is created to store clusters that are in the current population. This database is required by the genetic algorithm in case the user needs to resume the genetic algorithm. The user can also create the ``Recorded_Data/GA_Recording_Database.db`` database which is designed to save clusters that were created during the genetic algorithm. See :ref:`Recording Clusters From The Genetic Algorithm <Recording_Clusters_From_The_Genetic_Algorithm>` for more information on how to record clusters during the genetic algorithm. 

ASE allows the user to view the database in a number of ways. See `ase db <https://wiki.fysik.dtu.dk/ase/ase/db/db.html#ase-db>`_ to see how to use this. One of these ways is using the database website viewer, which allows the user to view the clusters in the database in a very nice graphical user interface. To use this, write into the terminal ``ase db -w name_of_database.db`` and open up the website ``http://0.0.0.0:5000/``. This works as it should in ASE version ``3.19.1``, ``3.19.2`` and ```3.19.3``, but it does not work in ASE versions ``3.20.0`` or ``3.20.1`` as of 21/11/2020. Need to check version ``3.21.1``. If you would like the formatting to be optimised for working with the genetic algorithm, the current solution is to change the version of ase to 3.19. To do this, first uninstall ASE by typing ``pip3 uninstall ase`` in the terminal, then running ``pip3 install --user ase==3.19.3`` in the terminal. 

You can also make a custom format for the ASE database website. To do this you will want to run the following command in the terminal ``ase db -w name_of_database.d -M meta.py``. The ``meta.py`` file is a python file that can be used to custom format the ASE database website. The ``meta.py`` file is designed to give the database title, give definitions for all the variables given to the database, and the format of the database website. The ``meta.py`` file contains the following variables:

* **title** (*str.*): This is the title of the database
* **default_columns** (*dict.*): This contains information about each variable in the database
* **key_descriptions** (*list of str.*): This is a list that specifies the order variable given in the database.

An example is a meta.py file is given in ``Helpful_Programs`` and an example is also given below

.. literalinclude:: meta.py
	:language: python
	:caption: meta.py
	:name: meta.py
	:tab-width: 4
	:linenos:

The format for the database as specified in this example is: ``name    cluster_energy    id``. 

The following variables are included in the database:

* **name** (*int*): Name of the cluster.
* **gen_made** (*int*): The generation the cluster was created.
* **cluster_energy** (energy units, *float*): Potential energy of the cluster.
* **ever_in_population** (*bool*): This variable indicates if the cluster was ever in the population. If an offspring was made and was not ever accepted into the population, this variable will be False. If the cluster had been in the population for even one generation, this variable will be True.
* **excluded_because_violates_predation_operator** (*bool*): This variable will determine if a cluster was excluded from the population because it violated the predation operator.
* **initial_population** (*bool*): This variable will indicate if the cluster was apart of a newly created population.
* **removed_by_memory_operator** (*bool*): This variable will indicate if a cluster is removed because it resembles a cluster in the memory operator.
