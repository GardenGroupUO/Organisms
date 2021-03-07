.. _Using_Predation_Operators:

Using Predation Operators with the Genetic Algorithm
####################################################

The predation operator is designed to remove offspring, or even swap offspring in for particular clusters in the population, that are too similar to other offspring or clusters in the population in some way. This is to prevent duplicates from entering into the population and prevent it from loosing predation.


Types of Predation Operators Available and How to Use Them
**********************************************************

Several different predation operators have been implemented into this genetic algorithm. The predation operators that are available are:
	
	* **Off**: No predation operator will be performed.
	* **Energy Predation**: If two clusters have similar energies, one of those clusters will be removed.
	* **IDCM-based Predation**: This operator will determine if two clusters are structrally identical.
	* **SCM-based Predation**: This operator will determine if two clusters are structrally similar based on the structural comparison method, developed by the Garden group to improve the efficiency of global optimisation algorithms.

No Predation Operator
=====================

Yes, I know, why is "No Predation Operator" a predation operator. Its just a title. This option will not invoke any predation operator into your genetic algorithm run.

To use this, in your Run.py or MakeTrials.py script, set 

.. code-block:: python

	Diversity_Information = {'Predation Operator: 'Off'}

Energy Predation Operator
=========================

This predation operator is designed to prevent the population containing two clusters with the same energy.

There are two different implementation of this predation operator written into this program. These are the:

* **Simple Energy Predation Operator**
* **Comprehensive Energy Predation Operator**

This is set in the ``predation_information`` dictionary with the ``'mode'`` input. These are described below:

Simple Energy Predation Operator
--------------------------------

This predation operator is designed to prevent the population containing two clusters with the same energy to some decimal place. For example, if cluster 1 has an energy of -186.2537935 eV and cluster 2 has an energy of -186.2482194 eV, and you have set the energy predation operator is set to round energies to 2 d.p., then these two clusters will be considered the same energy, and one of these clusters will be removed from the genetic algorithm.

To use this in your Run.py or MakeTrials.py script, will want to add two setting in the ``predation_information`` variable is required:

* **mode** (*str.*): This variable should be set to ``'simple'``.
* **round_energy** (*int*): This is the decimal place to which energies will be compared to in the Energy Predation operator.

An example of how these settings are implimented into your Run.py or MakeTrials.py scripts is shown below:

.. code-block:: python

	Predation_Information = {'Predation Operator': 'Energy', 'mode': 'simple', 'round_energy': 2}

Comprehensive Energy Predation Operator
---------------------------------------

This energy predation operator allows you to specify the minimium energy difference between clusters in the population. All clusters in the population must have energies that differ by greater or equal to this minimium energy difference.

This operator works as follows:

* **Initialisation of Population**: Every cluster in the population must differ in energy by energy_difference. If two or more clusters have the same energy, one of these will be kept and the others removed. This will give vacant sites in the population for the genetic algorithm to repopulate with other clusters more suited to the comprehensive energy predation operator.
* **During the Genetic Algorithm**: After all the offspring are created, the offspring are:

	* compared to other offspring to see if they have an energy difference less than the minimum energy difference. The offspring that are removed will again depend either on the energy or the fitness value of the offspring.
	* compared to clusters in the population to see if they have an energy difference less than the minimum energy difference. Here, the offspring may be removed, or swapped with a cluster from the population. This will depend either on the energy or the fitness value of the clusters.

The clusters that are kept or removed will depend on the setting given for the variable ``'type_of_comprehensive_operator'``. This can be set to either ``'energy'``, or ``'fitness'``. 

* If ``type_of_comprehensive_operator = 'energy'``, clusters will be removed or replaced based on their energy. Clusters are more likely to be kept if they have a lower energy, and clusters with higher energies are more likely to be removed or replaced. 
* If ``type_of_comprehensive_operator = 'fitness'``, clusters will be removed or replaced based on their fitness value. Clusters are more likely to be kept if they have a higher fitness, and clusters with lower fitnesses are more likely to be removed or replaced. 

To use this predation operator in your Run.py or MakeTrials.py script, you will want to add three setting in the ``predation_information`` variable:

* **mode** (*str.*): This variable should be set to ``'comprehensive'``.
* **minimum_energy_diff** (*float*): This is the difference in energy that any two clusters in the population can be between each other (in eV). 
* **type_of_comprehensive_operator** (*str.*): This variable determines how clusters are kept and removed from the genetic algorithm. 

	* Set ``type_of_comprehensive_operator = 'energy'`` if you want clusters to be kept, replaced, or removed based on their energy, or 
	* Set ``type_of_comprehensive_operator = 'fitness'`` if you want clusters to be kept, replaced, or removed based on their fitness values.

An example of how these settings are implimented into your Run.py or MakeTrials.py scripts is shown below:

.. code-block:: python

	Predation_Information = {'Predation Operator': 'Energy', 'mode': 'comprehensive', 'minimum_energy_diff': 0.025, 'type_of_comprehensive_operator': 'energy'}

IDCM-based Predation Operator
=============================

The Interatomic Distance Comparison Method (IDCM) based predation operator is designed to remove clusters that are structurally identical to other clusters in the population or in the offspring set. The implementation of this predation operator will measure all the distances between every atom in a cluster to give a list of distances between atoms in the cluster. This list is sorted from shortest to longest distance. If all elements of both lists differ by < X %, then the clusters are considered structurally identical. This predation operator is based on the predation operator from `J. A. Vargas, F. Buendía, M. R. Beltrán, J. Phys. Chem. C, 2017, 121, 20, 10982-10991 <https://pubs.acs.org/doi/10.1021/acs.jpcc.6b12848>`_.

This operator works as follows:

* **Initialisation of Population**: Every cluster in the population must not be structurally identical to one another. If this is the case, the fitter cluster will be kept while the less fitter clusters will be removed. 
* **During the Genetic Algorithm**: After all the offspring are created, the offspring are:

	* compared to other offspring to see if they structurally identical to one another. The fittest offspring is kept and the other less fit offspring are removed. 
	* compared to cluster in the population to see if they structurally identical to one another. If the cluster in the population has the higher fitness, all the less fit offspring will be removed. If the offspring is the fitter cluster, it will be swapped into the population at the expense of the less fit cluster in the population. 

To use this predation operator in your Run.py or MakeTrials.py script, you will want to add three setting in the ``predation_information`` variable is required:

* **percentage_diff** (*float*): This is the value X % in the description above. If all elements of both lists differ by < ``'percentage_diff'`` %, then the clusters are considered structurally identical. 

An example of how these settings are implimented into your Run.py or MakeTrials.py scripts is shown below:

.. code-block:: python

	predation_information = {'Predation Operator': 'IDCM', 'percentage_diff': 5.0}

.. _SCM_Based_Predation_Operator:

SCM-Based Predation Operator
============================

The Structural Comparison Method (SCM) based predation operator is based on the structural comparison method (SCM), that is designed to identify if two clusters are structurally similar. Two clusters are classed in to one of three similarity classes: Class I (structurally identical or gemotrically similar), class II (structurally different, but are of the same structural motif) or class III (structurally different, and are of different motifs). See more about how the SCM works at :ref:`The Structural Comparison Method <The_Structural_Comparison_Method>`. This method works as follows:

This operator works as follows:

* **Initialisation of Population**: Every cluster in the population must not be structurally identical or geometrically similar to one another (of class I similarity). If this is the case, the fitter cluster will be kept while the less fitter clusters will be removed. 
* **During the Genetic Algorithm**: After all the offspring are created, the offspring are:

	* compared to other offspring to see if they structurally identical or geometrically similar to one another. The fittest offspring is kept and the other less fit offspring are removed. 
	* compared to cluster in the population to see if they structurally identical or geometrically similar to one another. If the cluster in the population has the higher fitness, all the less fit offspring will be removed. If the offspring is the fitter cluster, it will be swapped into the population at the expense of the less fit cluster in the population. 

There are two forms of the SCM that can be used in this implementation of the genetic algorithm. These are:

* **The Total Structural Comparison Method (T-SCM)**: This method will tally up the abundances of all the CNA signatures, across all the atoms in a cluster. The method will then compare the total abundances of two clusters using the Jaccard similarity index to get the structural similarity between these two clusters. 
* **The Atomic Structural Comparison Method (A-SCM)**: This method will compare the number of atoms that have an eual number of the same atomic CNA signatures between two clusters. The similarity between the clusters is based on the number of CNA equivalent atoms between the two clusters.

To use this predation operator in your Run.py or MakeTrials.py script, you will want to add three setting in the ``predation_information`` variable is required:

* **CNA scheme** (*str.*): This is the type of CNA scheme you would like to use, be it the The Total Structural Comparison Method (T-SCM) or the The Atomic Structural Comparison Method (A-SCM).

The CNA required the user to input a value of rCut, a cutoff value that specifies the maximum distance between atoms to be considered neighbours or "bonded". There are two ways that this can be specified in the ``predation_information`` variable. If you want to sample just one value of rCut, the variable you want to add is:

* **rCut** (*float*): This is a single cutoff value to be used by the SCM to get the similarity between two clusters. Given in Å.

If you want the similarity between two clusters to be sampled over a range of rCut values, use the following inputs:

* **rCut_low** (*float*): This is the minimum cutoff distance that the SCM will sample. Given in Å.
* **rCut_high** (*float*): This is the maximum cutoff distance that the SCM will sample. Given in Å.
* **rCut_resolution** (*float* or *int*): This specifies the cutoff distances that the SCM will sample. If this is given as a *float*, then this value describes the distance between the consecutive rCut values that will be sampled. E.g. if rCut_low = 2.1, rCut_high = 3.4, and rCut_resolution = 0.2, then the cutoff values that will be sampled are 2.1, 2.3, 2.5, 2.7, 2.9, 3.1 and 3.3. If this is given as a *int*, then this value will describe the number of rCut values that will be sampled. E.g. if rCut_low = 2.4, rCut_high = 3.4, and rCut_resolution = 101, then the cutoff values that will be sampled are 2.1, 2.11, 2.12, 2.13, 2.14, ...., 3.37, 3.38, 3.39, 3.4. 

You can also give the rCut settings in terms of the nearest neighbour distances relative to the lattice constant. In this case you must give the lattice_constant:

* **lattice_constant** (*float*): This is the lattice constant of your metal/element in the bulk. Given in Å.

If you want to sample the CNA at one value, give that single value in terms of nearest neighbour units:

* **single_nn_measurement** (float): This is a single nearest neighbour value to be used by the SCM to get the similarity between two clusters. The rCut value is then given as fnn_distance * single_nn_measurement. This value must be between 1.0 and 2.0. Given in nearest neighbour distance units. 

Note that fnn_distance is the first nearest neighbour distance, given as ``fnn_distance = lattice_constant / (2.0 ** 0.5)``. If you want the similarity between two clusters to be sampled over a range of rCut values, use the following inputs:

* **nn_low** (*float*): This is the minimum neasest neighbour distance that the SCM will sample. The minimum rCut value that will be sampled is then given as fnn_distance * single_nn_measurement. This value must be between 1.0 and 2.0. Given in nearest neighbour distance units. 
* **nn_high** (*float*): This is the maximum neasest neighbour distance that the SCM will sample. The maximum rCut value that will be sampled is then given as fnn_distance * single_nn_measurement. This value must be between 1.0 and 2.0. Given in nearest neighbour distance units. 
* **nn_resolution** (*int*): This specifies the number of rCut values you would like to sample. For example, if you set nn_low = 1.2, nn_high = 1.6, and nn_resolution = 41, then the cutoff values that will be sampled are 1.2, 1.21, 1.22, 1.23, ..., 1.58, 1.59, 1.60. 

An example of how these settings are implemented into your Run.py or MakeTrials.py scripts is shown below:

.. code-block:: python

	predation_information = {'Predation Operator': 'SCM', 'CNA scheme': 'T-SCM', 'rCut_high': 3.2, 'rCut_low': 2.9, 'rCut_resolution': 0.05}

If you want to perform your SCM predation operator on gold (with a lattice constant of 4.07 Å) sampling 78 points between the 1 + 1/3 n.n.d and 1 + 2/3 n.n.d (where n.n.d is the nearest neighbour distance), This is how you would enter this into your Run.py or MakeTrials.py script:

.. code-block:: python

	predation_information = {'Predation Operator': 'SCM', 'CNA scheme': 'T-SCM', 'lattice_constant': 4.07, 'nn_high': 1.0 + (2.0/3.0), 'n_low': 1.0 + (1.0/3.0), 'nn_resolution': 78}


Writing Your Own Predation Operators for the Genetic Algorithm
***************************************************************

It is possible to write your own predation operators to incorporate into this gentic algorithm program. How fun is that! (I am writing this while on a plane jetlagged, apologies for my enthusism). To do this, you will need to write a python script that starts with the following:

.. code-block:: python

	from Organisms.GA.Predation_Operators.Predation_Operator import Predation_Operator

	class Sample_Predation_Operator(Predation_Operator):
		def __init__(self,predation_information,population,print_details):
			super().__init__(predation_information,population,print_details)

		def check_initial_population(self,return_report=False):
			# algorithm to check the initial population
			if return_report:
				return clusters_to_remove, report
			else:
				return clusters_to_remove

		def assess_for_violations(self,offspring_pool,force_replace_pop_clusters_with_offspring):
			# algorithm to check for violations between clusters in the population and the offspring
			return offspring_to_remove, force_replacement

In this Sample_Predation_operator, you will want to enter the following for each definition. 

* ``__init__(self,predation_information,population)``: This is the initialisation function. 

	* ``predation_information`` (*dict.*): contains all the information that the predation operator needs. 
	* ``population`` (*Organisms.GA.Population*): is the population that the predation operator will focus on monitoring.
	* ``print_details`` (*bool.*): This indicates if the user wants the algorithm to print out the details of what the predation operator is doing during the genetic algorithm.
* ``check_initial_population(self,return_report=False)``: This definition is responsible for making sure that the initialised population obeys the predation operator. 

	* ``return_report`` (*bool.*): indicates if a report on the clusters that were removed is needed.
	* ``clusters_to_remove`` (*list*): indicated which clusters to remove from the population. This is given as a list in the form: ``[index position of cluster in the population, the name of the cluster]``.
	* ``report`` (*dict.*): This indicates what clusters have violated the predation operator, and the clusters in he population that it is similar to. This is given as a dictionary in the form: ``{name of cluster to remove: [names of all the other cluster that this cluster is similar to (i.e. why this cluster violates the predation operator)]}``
* ``assess_for_violations(self,offspring_pool,force_replace_pop_clusters_with_offspring)``: This definition is designed to determine which offspring (and the clusters in the population) violate the predation operator during a generation. It will not remove or change any clusters in the offspring or population, but instead will record which offspring violate the predation operator. It will also recommend if it is beneficial to force replace a cluster in the population with a higher fitness offspring.

	* ``offspring_pool`` (*Organisms.GA.Offspring_Pool*): The offspring to check against the population for violations against this predation operator
	* ``offspring_to_remove`` (*list*): This gives a list of all the offspring to be removed from the offspring_pool due to violating the predation operator. This is a list with the form: ``[name of offspring to be remove, index of the offspring in the offspring_pool to be remove]``
	* ``force_replace_pop_clusters_with_offspring`` (*bool*): This will tell the genetic algorithm whether to swap clusters in the population with offspring if the predation operator indicates they are the same but the predation operator has a better fitness value than the cluster in the population. 
	* ``force_replacement`` (*list*): This gives a list of clusters in the offspring that, while violating the predation operator, have a higher fitness than their counterpart cluster in the population. Therefore, it is recommended to replace the cluster in the population with the offspring. This is a list with the form: ``(name of cluster in the population to remove, name of offspring to replace with)``