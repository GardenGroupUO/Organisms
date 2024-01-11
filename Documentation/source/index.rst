.. The Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similarity (Organisms) documentation master file, created by
   sphinx-quickstart on Mon Oct  1 08:10:30 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similatity (Organisms) documentation!
########################################################################################################################################

.. image:: https://img.shields.io/badge/Citation-click%20here-green.svg
   :target: https://dx.doi.org/10.1021/acs.jcim.0c01128
   :alt: Citation
   

.. image:: https://img.shields.io/pypi/pyversions/Organisms
   :target: https://docs.python.org/3/
   :alt: Python Version


.. image:: https://img.shields.io/github/v/release/GardenGroupUO/Organisms
   :target: https://github.com/GardenGroupUO/Organisms
   :alt: GitHub release (latest by date)


.. image:: https://img.shields.io/pypi/v/Organisms
   :target: https://pypi.org/project/Organisms/
   :alt: PyPI


.. image:: https://img.shields.io/conda/v/gardengroupuo/organisms
   :target: https://anaconda.org/GardenGroupUO/organisms
   :alt: Conda


.. image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/GardenGroupUO/Organisms/blob/main/Notebooks/Organisms_Jupyter_Example.ipynb#scrollTo=objective-alliance
   :alt: Colab


.. image:: https://img.shields.io/github/license/GardenGroupUO/Organisms
   :target: https://www.gnu.org/licenses/agpl-3.0.en.html
   :alt: Licence


.. image:: https://img.shields.io/lgtm/grade/python/github/GardenGroupUO/Organisms
   :target: https://lgtm.com/projects/g/GardenGroupUO/Organisms/context:python
   :alt: LGTM Grade

.. sectionauthor:: Geoffrey Weal <geoffrey.weal@gmail.com>
.. sectionauthor:: Dr. Anna Garden <anna.garden@otago.ac.nz>

Group page: https://blogs.otago.ac.nz/annagarden/

Page to cite with work from: Development of a Structural Comparison Method to Promote Exploration of the Potential Energy Surface in the Global Optimisation of Nanoclusters, Geoffrey R. Weal, Samantha M. McIntyre, and Anna L. Garden, *J. Chem. Inf. Model.*, **2021**, *61* (4), 1732-1744 `DOI: 10.1021/acs.jcim.0c01128 <https://dx.doi.org/10.1021/acs.jcim.0c01128>`_.

What is this Documentation about?
=================================

This documentation is designed to guide the user to use the Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similatity (Organisms) program. 


What is Organisms
=================

The Otago Research Genetic Algorithm for Nanoclusters, Including Structural Methods and Similarity (Organisms) program is designed to perform a genetic algorithm global optimisation for nanoclusters. It has been designed with inspiration from the Birmingham Cluster Genetic Algorithm and the Birmingham Parallel Genetic Algorithm from the Roy Johnston Group 
(see ``J. B. A. Davis, A. Shayeghi, S. L. Horswell, R. L. Johnston, Nanoscale, 2015,7, 14032`` (`https://doi.org/10.1039/C5NR03774C <https://doi.org/10.1039/C5NR03774C>`_ or `link to Davis pdf here <https://pubs.rsc.org/en/content/articlepdf/2015/nr/c5nr03774c>`_) 
and 
``R. L. Johnston, Dalton Trans., 2003, 4193–4207`` (`https://doi.org/10.1039/B305686D <https://doi.org/10.1039/B305686D>`_ or `link to Johnston pdf here <http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.124.6813&rep=rep1&type=pdf>`_). 

This algorithm is designed to explore the potential energy surface of a cluster system, using the genetic algorithm, and to local the putative globally lowest energetic cluster. It was designed for obtaining low energy structures of clusters that could be catalytically interesting. The algorithm was designed by Dr Anna Garden and the Garden group at the University of Otago, Dunedin, New Zealand. See for more information about what the group does at `blogs.otago.ac.nz/annagarden <https://blogs.otago.ac.nz/annagarden/>`_. The Github page for this program can be found at `github.com/GardenGroupUO/Organisms <https://github.com/GardenGroupUO/Organisms>`_. 

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

Try Organisms before you Clone/Pip/Conda (on Binder/Jupter Notebooks)!
======================================================================

If you are new to the Organisms program, it is recommended try it out by running Organisms live on our interactive Jupyter+Google Colabs page before you download it. On Google Colabs, you can play around with the Organisms program on the web. You do not need to install anything to try Organisms out on Google Colabs. 

**Click the Google Colabs button below to try Organisms out on the web!**

.. image:: https://colab.research.google.com/assets/colab-badge.svg
   :target: https://colab.research.google.com/github/GardenGroupUO/Organisms/blob/main/Notebooks/Organisms_Jupyter_Example.ipynb#scrollTo=objective-alliance
   :alt: Colab


Installation
============

It is recommended to read the installation page before using the Organisms program. See :ref:`Installation: Setting Up the Organisms Program and Pre-Requisites Packages <Installation>` for more information. Note that you can install Organisms through ``pip3`` and ``conda``. 


Table of Contents
=================

.. toctree::
   :maxdepth: 2
   
   How_Organisms_Works
   Installation
   How_To_Use_The_Organisms_Program
   Using_Run
   Files_Made_During_the_Genetic_Algorithm
   Examples_of_Running_GA
   Local_Minimisation_Function
   Using_MakeTrials
   Safely_Finishing_the_GA_Midway
   Restarting_the_Genetic_Algorithm
   Common_Issues_of_GA
   HelpfulPrograms_CreatingAndRunningGA
   HelpfulPrograms_GatherAndPostprocessingData
   make_energy_vs_similarity_results_documentation
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