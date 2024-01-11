.. _Using_Fitness_Operators:

Using Fitness Operators with the Genetic Algorithm
##################################################

The fitness operator is designed to assign the fitness values to each cluster created during the genetic algorithm. This allows one to invoke different ways for the genetic algorithm to explore the potential energy surface for a particuar cluster. The fitness is used for the following reasons:

* To determine the likelihood of clusters being mated together during the crossover proceedure (during the offspring creation process). 
* To determine which clusters are removed during the predation process.
* To determine which clusters survive during the natural selection process. 

Types of Fitness Operators Available and How to Use Them
********************************************************

Two types of fitness operators have been implemented into this genetic algorithm. The fitness operators that are available are:
	
* :ref:`Energy_Fitness_Operator_intext`: Here, the fitness of a cluster is determined by its energy as well as the energy of the lowest energetic and highest energetic cluster in the population and offspring pool.
* :ref:`Structure_plus_Energy_Fitness_Operator`: In this operator, the fitness of a cluster is obtained from the energy of the cluster (obtained using the **Energy** fitness operator) as well as from the similarity of the cluster, as obtained using the structural comparison method (SCM). 

.. _Energy_Fitness_Operator_intext:

Energy Fitness Operator
=======================

This operator gives each cluster a fitness value by taking the energy of the cluster, and the energy of the highest and lowest energtic clusters in the current population and offspring pool. The only input require are the settings for the ``'fitness_function'``, which will be explained in :ref:`Fitness Functions <Fitness_Functions>`. An example of how these settings are implimented into your Run.py or MakeTrials.py scripts is shown below:

.. code-block:: python

	energy_fitness_function = {'function': 'exponential', 'alpha': 3.0}
	fitness_information = {'Fitness Operator': 'Energy', 'fitness_function': energy_fitness_function}

.. _Structure_plus_Energy_Fitness_Operator:

Structure + Energy Fitness Operator
===================================

This operator works by taking the energy of the cluster (as well as the energy of the highest and lowest energtic clusters in the current population and offspring pool) and the representative similarity of the cluster, and converting these into a fitness value for the cluster. Read more about how the SCM works at the section on :ref:`The Structural Comparison Method <The_Structural_Comparison_Method>`.

The representative similaity is obtained as follows: Every cluster in the population and in the offspring pool will have an associated average similarity associated to them. For each cluster, all the of the average similarities that cluster has with every other cluster are placed in a list, and the maximum average similarity from the list is taken as that clusters representative similaity.

The input parameters required for this fitness operator are:

* **SCM scheme** (*str.*): This is the type of SCM scheme you would like to use. This can be either Total Comparison Structural Comparison Method (T-SCM) or the Atom-by-Atom Comparison Structural Comparison Method (A-SCM). Read more about this at the :ref:`SCM Based Predation Operator <SCM_Based_Predation_Operator>`.
* **SCM_fitness_contribution** (*float*): This is the relative contribution of the SCM fitness value to the overall value. The energetic fitness contribution is 1 - ``'SCM_fitness_contribution'``. 
* **Take from the collection of a clusters similarities** (*str.*): This determines how you want to process all the siilarities that are associated with a cluster in the population and offspring. This can be set to either ``'Maximum'`` or ``'Average'``. See :ref:`Take from the collection of a cluster's similarities <Take_from_the_collection_of_a_clusters_similarities>` for more information. Default: ``'Maximum'``. 
* **normalise_similarities** (*bool*): This will tell the SCM + Energy Fitness Operator whether to normalise the similarity or not. Normalising the similarities means taking the structural similarity, subtracting it from the minimum similarity of clusters in the population , and dividing it by the maximum similarity minus minimum similarity of clusters in the population. True means to normalise, False means do not normalise the similarities. See :ref:`Normalise Similarities <Normalise_Similarities>` for more information. Default: False. 
* **Dynamic Mode** (*bool.*): This will set the operator into dynamic mode. See more about this at :ref:`Dynamic Mode <Dynamic_Mode>`.
* **energy_fitness_function** (*Organisms.GA.Fitness_Scripts.Fitness_Function*): This describes how the fitness is obtained for the energetic fitness value. More about fitness functions can be read at :ref:`Fitness Functions <Fitness_Functions>`.
* **SCM_fitness_function** (*Organisms.GA.Fitness_Scripts.Fitness_Function*): This describes how the fitness is obtained for the SCM-based fitness value. More about fitness functions can be read at :ref:`Fitness Functions <Fitness_Functions>`.

If you are using the SCM Based Diversity operator as well, you can also include the following inputs:

* **Use Predation Information** (*bool.*): If this is set to ``True``, the Structure + Energy fitness operator will use the same rCut parameters as the SCM-based predation operator. Do not include this in the ``predation_information``, or set this to ``False``, if you want to use different values of rCut for the SCM + Energy fitness operator or are not using the SCM-based Predation Operator. default: False

If you need to set the rCut values, you can enter this in two ways.  If you want to sample just one value of rCut, the variable you want to add is:

* **rCut** (*float*): This is a single cutoff value to be used by the SCM to get the similarity between two clusters. Given in Å.

If you want the similarity between two clusters to be sampled over a range of rCut values, use the following inputs:

* **rCut_low** (*float*): This is the minimum cutoff distance that the SCM will sample. Given in Å.
* **rCut_high** (*float*): This is the maximum cutoff distance that the SCM will sample. Given in Å.
* **rCut_resolution** (*float*): This specifies the cutoff distances that the SCM will sample. If this is given as a float, then this value describes the distance between the consecutive rCut values that will be sampled. E.g. if rCut_low = 2.1, rCut_high = 3.4, and rCut_resolution = 0.2, then the cutoff values that will be sampled are 2.1, 2.3, 2.5, 2.7, 2.9, 3.1 and 3.3. If this is given as a int, then this value will describe the number of rCut values that will be sampled. E.g. if rCut_low = 2.4, rCut_high = 3.4, and rCut_resolution = 101, then the cutoff values that will be sampled are 2.1, 2.11, 2.12, 2.13, 2.14, ...., 3.37, 3.38, 3.39, 3.4. 

You can also give the rCut settings in terms of the **nearest neighbour distances relative to the lattice constant**. In this case you must give the lattice_constant:

* **lattice_constant** (*float*): This is the lattice constant of your metal/element in the bulk. Given in Å.

If you want to sample the CNA at one value, give that single value in terms of nearest neighbour units:

* **single_nn_measurement** (float): This is a single nearest neighbour value to be used by the SCM to get the similarity between two clusters. The rCut value is then given as fnn_distance * single_nn_measurement. This value must be between 1.0 and 2.0. Given in nearest neighbour distance units. 

Note that fnn_distance is the first nearest neighbour distance, given as ``fnn_distance = lattice_constant / (2.0 ** 0.5)``. If you want the similarity between two clusters to be sampled over a range of rCut values, use the following inputs:

* **nn_low** (*float*): This is the minimum neasest neighbour distance that the SCM will sample. The minimum rCut value that will be sampled is then given as fnn_distance * single_nn_measurement. This value must be between 1.0 and 2.0. Given in nearest neighbour distance units. 
* **nn_high** (*float*): This is the maximum neasest neighbour distance that the SCM will sample. The maximum rCut value that will be sampled is then given as fnn_distance * single_nn_measurement. This value must be between 1.0 and 2.0. Given in nearest neighbour distance units. 
* **nn_resolution** (*int*): This specifies the number of rCut values you would like to sample. For example, if you set nn_low = 1.2, nn_high = 1.6, and nn_resolution = 41, then the cutoff values that will be sampled are 1.2, 1.21, 1.22, 1.23, ..., 1.58, 1.59, 1.60. 


Three examples of how these settings are implimented into your Run.py or MakeTrials.py scripts are shown below. First, if you have not used the SCM-based predation operator, or you are using the SCM-based predation operator but sampling different values of rCut, an example of ``fitness_information`` is given below.

.. code-block:: python

	fitness_information = {'Fitness Operator': 'Structure + Energy', 'CNA scheme': 'T-SCM', 'rCut_high': 3.2, 'rCut_low': 2.9, 'rCut_resolution': 0.05, 'SCM_fitness_contribution': 0.5, 'normalise_similarities': False, 'Dynamic Mode': False, 'energy_fitness_function': energy_fitness_function, 'SCM_fitness_function': SCM_fitness_function}

If you want to perform your SCM fitness operator on gold (with a lattice constant of 4.07 Å) sampling 78 points between the 1 + 1/3 n.n.d and 1 + 2/3 n.n.d (where n.n.d is the nearest neighbour distance), This is how you would enter this into your Run.py or MakeTrials.py script:

.. code-block:: python

	fitness_information = {'Fitness Operator': 'Structure + Energy', 'CNA scheme': 'T-SCM', lattice_constant: 4.07, 'nn_high': 1.0 + (2.0/3.0), 'n_low': 1.0 + (1.0/3.0), 'nn_resolution': 78, 'SCM_fitness_contribution': 0.5, 'normalise_similarities': False, 'Dynamic Mode': False, 'energy_fitness_function': energy_fitness_function, 'SCM_fitness_function': SCM_fitness_function}

If you are using the SCM-based predation operator and sampling the same values of rCut, you can set ``Use Predation Information = True`` and negate writing in the same values for rCut. An example is given below:

.. code-block:: python

	fitness_information = {'Fitness Operator': 'Structure + Energy', 'CNA scheme': 'T-SCM', 'Use Predation Information': True, 'SCM_fitness_contribution': 0.5, 'normalise_similarities': False, 'Dynamic Mode': False, 'energy_fitness_function': energy_fitness_function, 'SCM_fitness_function': SCM_fitness_function}

.. _Take_from_the_collection_of_a_clusters_similarities:

Take from the collection of a cluster's similarities
----------------------------------------------------

When obtaining the value of :math:`\sigma_{SCM}(x)` for cluster :math:`x`, you take the collection of all :math:`\sigma` values between cluster :math:`x` and every other cluster in the population and offspring, and you perform some sort of mathematical operation upon this collection of :math:`\sigma` values to obtain :math:`\sigma_{SCM}(x)`. There are two settings for this: 

If you set ``'Take from the collection of a clusters similarities'`` in the ``fitness_information`` dictionary to ``'Maximum'``, then you will take the maximum value of :math:`\sigma_{xy}` between the :math:`x`:superscript:`th` cluster and every other cluster in the population (including offspring)

:math:`\sigma_{SCM}(x) = \max\{\sigma_{xy} | y = 1, ..., n_{total}, y \neq x\}` 

where :math:`n_{total}` is the total number of clusters in the population (including offspring). ``'Maximum'`` is the default setting for this setting in the ``fitness_information`` dictionary.

If you set ``'Take from the collection of a clusters similarities'`` in the ``fitness_information`` dictionary to ``'Average'``, then you will take the mean value of :math:`\sigma_{xy}` between the :math:`x`:superscript:`th` cluster and every other cluster in the population (including offspring)

:math:`\sigma_{SCM}(x) = \textrm{mean}\{\sigma_{xy} | y = 1, ..., n_{total}\}` 

where :math:`n_{total}` is the total number of clusters in the population (including offspring). 

.. _Normalise_Similarities:

Normalise Similarities
----------------------

The similarity obtained from the SCM is used to obtain the structural fitness values for the clusters in the population. To do this, the algorithm obtains the :math:`\rho_{SCM}(x)` for the :math:`x`:superscript:`th` cluster in the population, which is the translated into the structural fitness value, :math:`f_{SCM}(x)` for the :math:`x`:superscript:`th` cluster. The value of :math:`\rho_{SCM}(x)` can be obtained in two ways. 

First, the unnormalised similarity can be used, where the :math:`x`:superscript:`th` cluster's similarity is divided by 100 to give the similarity as a decimal, which is between 0 and 1. 

:math:`\rho_{SCM}(x) = \frac{\sigma_{SCM}(x)}{100}` 

Second, the similarity can be normalised. Here, the maximum and minimum similarities of all cluster in the population, including offspring, are obtained (referred to as :math:`\sigma_{SCM,max}` and :math:`\sigma_{SCM,min}`). :math:`\rho_{SCM}(x)` for the :math:`x`:superscript:`th` cluster is then obtained as below

:math:`\rho_{SCM}(x) = \frac{\sigma_{SCM}(x) - \sigma_{SCM,min}}{\sigma_{SCM,max} - \sigma_{SCM,min}}` 

.. _Dynamic_Mode:

Dynamic Mode
------------

To be developed. 

.. _Fitness_Functions:

Fitness Functions
=================

In this implementation of the genetic algorithm, there are a few different functions that one can use to convert an energy or a similarity value into a fitness value. You can find more information about these fitness functions in `R. L. Johnston, Dalton Trans., 2003, 4193-4207 <https://pubs-rsc-org.ezproxy.otago.ac.nz/en/content/articlelanding/2003/dt/b305686d#!divAbstract>`_

Exponential Function
--------------------

This will use a exponential function to obtain the fitness value. 

:math:`f(i) = e^{-\alpha\rho(i)}` 

The input required is the value of :math:`\alpha` 

An example of the input for this function is shown below.

.. code-block:: python

	energy_fitness_function = {'function': 'exponential', 'alpha': 3.0}

Hyperbolic Tangent Function
---------------------------

This will use a hyperbolic tangent function to obtain the fitness value. 

:math:`f(i) = \frac{1}{2}[1 - \tanh(2\rho(i) - 1)]` 

An example of the input for this function is shown below.

.. code-block:: python

	energy_fitness_function = {'function': 'tanh'}

Linear Function
---------------

This will use a linear function to obtain the fitness value. 

:math:`f(i) = \rm{gradient} \times rho(i) + \rm{constant}` 

The input required is the value of :math:`\rm{gradient}` and :math:`\rm{constant}` 

An example of the input for this function is shown below.

.. code-block:: python

	energy_fitness_function = {'function': 'linear', 'gradient': 0.5, 'constant': 0.5}

Direct Function
---------------

This will use a direct function to obtain the fitness value. 

:math:`f(i) = \rho(i)` 

An example of the input for this function is shown below.

.. code-block:: python

	energy_fitness_function = {'function': 'direct'}

Writing Your Own Fitness operators for the Genetic Algorithm
*************************************************************

It is possible to write your own fitness operators to incorporate into this gentic algorithm program. To do this, you will need to write a python script that has the following:

.. code-block:: python

	from Organisms.GA.Fitness_Operators.Fitness_Operator import Fitness_Operator
	from Organisms.GA.Fitness_Operators.Fitness_Function import Fitness_Function

	class Sample_Fitness_Operator(Fitness_Operator):

		def __init__(self, fitness_information, predation_operator, population, print_details):

		def assign_initial_population_fitnesses(self):
			
		def assign_resumed_population_fitnesses(self, resume_from_generation): 
			
		def assign_all_fitnesses_before_assess_against_predation_operator(self, all_offspring_pools, current_generation_no):
			
		def assign_all_fitnesses_after_assess_against_predation_operator(self, all_offspring_pools, current_generation_no, offspring_to_remove):

		def assign_all_fitnesses_after_natural_selection(self, current_generation_no):
		
In this Sample_Fitness_Operator, you will want to enter the following for each definition.

* ``__init__(self, fitness_information, predation_operator, population, print_details)``: This is the initialisation function.

	* ``fitness_information`` (*dict.*): Contains all the information that the fitness operator needs.
	* ``predation_operator`` (*Organisms.GA.Predation_Operators.Predation_Operator*): This is the predation operator that is being used in the genetic algorithm.
	* ``population`` (*Organisms.GA.Population*): Is the population that the predation operator will focus on monitoring.
	* ``print_details`` (*bool.*): This indicates if the user wants the algorithm to print out the details of what the predation operator is doing during the genetic algorithm.

* ``assign_initial_population_fitnesses(self)``: This assigns the fitnesses to the clusters in the initial population.

* ``assign_resumed_population_fitnesses(self, resume_from_generation)``: This assigns the fitnesses to the clusters in the population that has been resumed.

	* ``resume_from_generation`` (*int*): The number of the generation that the genetic algorithm is being resumed from.

* ``assign_all_fitnesses_before_assess_against_predation_operator(self, all_offspring_pools, current_generation_no)``: This will assign fitness to the clusters in the population and the offspring before the predation operator has been performed for this generation. 

	* ``all_offspring_pools`` (*Organisms.GA.Offspring_Pool* or a *list of Organisms.GA.Offspring_Pool*): The offspring_pool
	* ``current_generation_no`` (*int*): The current generation.

* ``assign_all_fitnesses_after_assess_against_predation_operator(self, all_offspring_pools, current_generation_no, offspring_to_remove)``: This will assign fitness to the clusters in the population and the offspring after the predation operator has been performed for this generation. 

	* ``all_offspring_pools`` (*Organisms.GA.Offspring_Pool* or a *list of Organisms.GA.Offspring_Pool*): The offspring_pool
	* ``current_generation_no`` (*int*): The current generation.
	* ``offspring_to_remove`` (*list of ints*): This is a list of the names of the clusters that will be removed. This is currently not needed, but kept as a input variable just in case it is needed in the future. 

* ``assign_all_fitnesses_after_natural_selection(self, current_generation_no)``: This will assign all the fitnesses to all clusters in the population after performing the natural selection process

	* ``current_generation_no`` (*int*): The current generation.