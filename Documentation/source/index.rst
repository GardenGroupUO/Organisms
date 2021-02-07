.. The Genetic Algorithm for Research and Development on Nanoclusters (Organisms) documentation master file, created by
   sphinx-quickstart on Mon Oct  1 08:10:30 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similatity (Organisms) documentation!
########################################################################################################################################

.. raw:: html
    :file: Images/pypi_python_version.svg
.. raw:: html
    :file: Images/pypi_version.svg
.. raw:: html
    :file: Images/github_licence.svg

This documentation is designed to guide the user to use the GOtago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similatity (Organisms) program. This algorithm is designed to explore the potential energy surface of a cluster system, using the genetic algorithm, and to local the putative globally lowest energetic cluster. It was designed for obtaining low energy structures of clusters that could be catalytically interesting. The algorithm was designed by Dr Anna Garden and the Garden group at the University of Otago, Dunedin, New Zealand. See for more information about what the group does at `blogs.otago.ac.nz/annagarden <https://blogs.otago.ac.nz/annagarden/>`_. The Github page for this program can be found at `github.com/GardenGroupUO/Organisms <https://github.com/GardenGroupUO/Organisms>`_.

.. sectionauthor:: Dr. Anna Garden <anna.garden@otago.ac.nz>
.. sectionauthor:: Geoffrey Weal <geoffrey.weal@gmail.com>

.. tabs::

   .. tab:: Genetic Algorithm

      The genetic algorithm uses the ideas of Darwin's theory of evolution to locate the global minimum.

   .. tab:: Operators

      This implementation of the genetic algorithm includes various predation, fitness and epoch operators. Also included is the SCM-based predation operator and a ''structure + energy'' fitness operator.

   .. tab:: SCM-based predation operator

      The SCM-based predation operator compares the structures of clusters together and excludes clusters from the population that are too similar to each other. 

   .. tab:: ''Structure + energy'' fitness operator

      The ''structure + energy'' fitness operator is designed to include a portion of structural diversity into the fitness value as well as energy. The goal of this fitness operator is to guide the genetic algorithm around to unexplored areas of a cluster's potential energy surface. 

   .. tab:: Recording clusters in databases

      With the use of Atomic Simulation Environment, this algorithm has been designed so that you can record all the clusters you make, or just the important ones such as the lowest energy clusters that you make

Table of Contents
=================

.. toctree::
   :maxdepth: 2
   
   How_Organisms_Works
   Installation
   How_To_Use_The_Organisms_Program
   Using_Run
   Local_Minimisation_Function
   Examples_of_Running_GA
   Using_MakeTrials
   Safely_Finishing_the_GA_Midway
   Restarting_the_Genetic_Algorithm
   Common_Issues_of_GA
   HelpfulPrograms_CreatingAndRunningGA
   HelpfulPrograms_GatherAndPostprocessingData
   HelpfulPrograms_Others
   Initialising_a_New_Population
   Using_Predation_Operators_with_the_Genetic_Algorithm
   Using_Fitness_Operators_with_the_Genetic_Algorithm
   The_Structural_Comparison_Method
   Using_the_Memory_Operator
   Using_Epoch_Methods
   Recording_Clusters_From_The_Genetic_Algorithm
   Using_Databases_with_the_Genetic_Algorithm
   Adding_Surfaces
   GA_Files
   genindex
   py-modindex

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`