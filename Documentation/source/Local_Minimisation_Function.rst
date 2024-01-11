
.. _Local_Minimisation_Function:

*RunMinimisation.py* - Writing a Local Minimisation Function for the Genetic Algorithm
######################################################################################

In this article, we will look at how to write the local optimisation method for the genetic algorithm. 

.. contents::
    :depth: 2
    :local:

What is the Minimisation_Function
*********************************

The ``Minimisation_Function`` is a definition that tells the genetic algorithm how to perform a local optimisation. This is used by the genetic algorithm as a ``def`` (i.e. as a function). This means that, rather than a variable being passed into the algorithm, a function is passed into the algorithm. 

The implementation of the local minimisation process in this genetic algoritm program has been designed to be as free as possible, so that the user can use whatever local optimisation algorithm or program they want to use. In general, this algorithm will import a cluster in an ASE format from the genetic algorithm. The user can locally optimise it before sending it back to the genetic algorithm again in the ASE format.

Because of the flexibility, it is possible to use any type of calculator from ASE, ASAP, GWAP, LAMMPS, etc. It is even possible for the user to design this to use with non-python user-interface based local optimisers, such as VASP or Quantum Espresso! See at the bottom of this page, :ref:`How to write the Minimisation_Function for non-ASE Implemented Calculator <non_ASE_Implemented_Calculator>`.

In the following documentation we will describe how the ``Minimisation_Function`` method is designed in a **RunMinimisation.py** file, and how you can make your own. Examples of **RunMinimisation.py** files can be found in `github.com/GardenGroupUO/Organisms <https://github.com/GardenGroupUO/Organisms>`_ in the directory path ``Examples/Set_of_RunMinimisation_Files`` (this should be found in `github.com/GardenGroupUO/Organisms/tree/main/Examples/Set_of_RunMinimisation_Files <https://github.com/GardenGroupUO/Organisms/tree/main/Examples/Set_of_RunMinimisation_Files>`_). 

Where to write the Minimisation_Function
****************************************

The ``Minimisation_Function`` can be written into the Run.py file. However, as a personal preference and also to make the code cleaner to read, write and use, I put it into another python file. This file I have called **RunMinimisation.py**. This does not need to be the name of this file. For example, I have named this file **RunMinimisation_AuPd.py** when I wanted to keep a record that this minimisation python file contained the Gupta parameters and code for locally minimising a cluster using the Gupta potential for a cluster containing Au and Pd atoms. 

Furthermore, the def ``Minimisation_Function`` does not even need to be called ``Minimisation_Function``. It could be called ``TheGuptaFunction``, ``the_local_minimisation_function``, or ``The_Electric_Eel_Function``. Again, I have just always called it ``Minimisation_Function`` for simplicity and for ease when using different Run.py files with different Minimisation_Function codes. 

However, it is important that this code is referenced somehow in the Run.py program. The algorithm is imported into Run.py as follows (You can also see this in :ref:`Run.py - Using the Genetic Algorithm: Minimisation Scheme <Using_Run_Minimisation_Scheme>`):

.. code-block:: python

	# The RunMinimisation.py algorithm is one set by the user. It contain the def Minimisation_Function
	# That is used for local optimisations. This can be written in whatever way the user wants to perform
	# the local optimisations. This is meant to be as free as possible.
	from RunMinimisation import Minimisation_Function

where, in the above code, ``RunMinimisation`` is the name of the file the local minimisation code is found in (This file is called **RunMinimisation.py**), and ``Minimisation_Function`` is the name of the function that is found in the **RunMinimisation.py**. If you do it like this, make sure that your **RunMinimisation.py** file is in the same folder as your Run.py file. 


How to write the Minimisation_Function
**************************************

The ``Minimisation_Function`` must be written with the following requirements:

* **cluster** (*ase.Atoms*): This is the unoptimised version of the cluster.
* **collection** (*str.*): This indicates if the cluster is apart of which instance of Population or Offspring_pool.
* **cluster_name** (*int.*): This is the name of the cluster to be optimised. This should be the number of the cluster that was made during this genetic algorithm run.

NOTE: The **collection** and **cluster_name** variables do not need to be used in your ``RunMinimisation.py`` script if you are using an ASE or ASE implemented calculator and local optimisator. This information may be useful if you want the cluster to be locally optimised using an external program that can not be easily used with python (for example with VASP, see :ref:`How to write the Minimisation_Function for non-ASE Implemented Calculator <non_ASE_Implemented_Calculator>`).

returns: 

* **cluster** (*ase.Atoms*) - This is the optimised version of the cluster. 
* **converged** (*bool.*) - This boolean indicates if the local optimisation converged (``True`` for converged, ``False`` for did not converge).
* **Info** (*dict.*) - This sends information back to the genetic algorithm about how the local minimsation ran. 

An example of a RunMinimisation.py file for a Gupta potential involving only Cu atoms is given below:

.. literalinclude:: RunMinimisation.py
	:language: python
	:caption: RunMinimisation.py
	:name: RunMinimisation.py
	:tab-width: 4
	:linenos:

We will explain the components of this example below:

Importing external code
-----------------------

To begin, you will need to import all the external files that you will need so that you have the descriptor of the potential you want to use, and the local optimiser that you would like to use. In this example, the Gupta potential is used as the descriptor for the potential, while ``FIRE`` is the local optimiser that will be used to locally optimise the cluster.

.. literalinclude:: RunMinimisation.py
	:language: python
	:tab-width: 4
	:linenos: 
	:lineno-start: 16
	:lines: 16-19

Preparing the cluster 
---------------------

First, it is usually a good idea to tell ase if you want the calculator to calculate the cluster with periodic boundary conditions ``pbc`` or not. In the case of the Gupta potential, we will include the line ``cluster.pbc = False`` to make sure that there are no boundary conditions on upon the cluster, since we do not want this and the Gupta potential does not need this turned on. For your potential, you may want to include this, or not.

.. literalinclude:: RunMinimisation.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 22
	:lines: 22
	:dedent: 4

Preparing the Potential, and setting up the local optimiser.
------------------------------------------------------------

We would like to set up the parameters needed for the descriptor of the potential, attach the descriptor as a calculator to the ``cluster``, and set up the local optimiser. In this example, Gupta is called a calculator. It contains a description of the Gupta potential that can be used to calculate the energy of ``cluster``. We do this in the line ``cluster.set_calculator(Gupta(Gupta_parameters, cutoff=1000, debug=True))``. For more information on how this works, see `Tutorial on Using Calculators in ASE <https://wiki.fysik.dtu.dk/ase/ase/calculators/calculators.html>`_. 

The last line, ``dyn = FIRE(cluster)``, sets up the local optimiser, ``FIRE``, to be used to locally minimise the cluster ``cluster`` (see `Tutorial on Structure Optimization in ASE <https://wiki.fysik.dtu.dk/ase/ase/optimize.html>`_). 

See below for a example:

.. literalinclude:: RunMinimisation.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 24
	:lines: 24-28
	:dedent: 4

Executing the local optimiser
-----------------------------

We would like to now get the definition to run a local optimisation. This is done by performing ``dyn.run(fmax=0.01,steps=5000)``. However I have found that if something breaks for some reason during the optimisation, this can completely stop the genetic algorithm in its tracks, and cause it to finish with a fatal error. You may want this to happen so that you can address issues when they arise, but sometimes it is hard to continue to work when it keeps happening. If you would like, you can make sure the genetic algorithm does not fail entirely by adding a Error Handling block, as shown in the example below:

.. literalinclude:: RunMinimisation.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 29
	:lines: 29-39
	:dedent: 4

You can also see that I have placed an if statement to determine if the local optimsation actually converged. I have found that it is useful to include a way of noting if the optimisation was able to converge or not. See more about `How to perform a local optimisation in ASE here <https://wiki.fysik.dtu.dk/ase/ase/optimize.html>`_, or refer to the manual of the local optimiser you are using for more information on how to do this.

Writing the Info variable
-------------------------

I have found it useful for benchmarking in the past to give back to the genetic algorithm information on Force calls and times, and weither the optisation converged or not. For this we include it in the INFO.txt file for that optimisation as shown below. FEATURE IS CURRENTLY DISABLED.

.. literalinclude:: RunMinimisation.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 41
	:lines: 41-46
	:dedent: 4

Return the Optimised Cluster and Info
-------------------------------------

Remember to return the ``cluster`` and ``Info`` to the genetic algorithm so that it can use this information, as well as the optimiser cluster, to proceed to explore the potential energy surface of the cluster you wish to explore.

.. literalinclude:: RunMinimisation.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 48
	:lines: 48
	:dedent: 4


How to write the Minimisation_Function for a ASE Implemented Calculator
***********************************************************************

If the descriptor for the potential you would like to use is implemented in ASE, it is very easy to implement this into your Minimisation_Function definition. You can use the example of RunMinimisation.py above, where the only component you need to change is the set_calculator function used by Opt_cluster. This is the bit of the code above that looks like this:

.. code-block:: python

	Gupta_parameters = {'Cu': [10.960, 2.2780, 0.0855, 1.224, 2.556]}
	cluster.set_calculator(Gupta(Gupta_parameters, cutoff=1000, debug=True))

Instead of this, you can include all the parameters that you need for your potential before the set_calculator line. For example:

.. code-block:: python

	Potential_Parameters = ...
	cluster.set_calculator(Potential(Potential_Parameters))

Where ``Potential`` is the potential you would like to use, and ``Potential_Parameters`` are all the parameters that ``Potential`` needs to work. Please consult the manual of the potential you would like to use to learn how to use that potential.

.. _non_ASE_Implemented_Calculator:

How to write the Minimisation_Function for non-ASE Implemented Calculator
*************************************************************************

In the previous section of this page we have been performing a local optimisation using ASE implemented calculators. However, you may want to use a calculator to locally optimise your cluster. This may only be possible by allowing the program you wish to use to itself completely locally optimise the cluster. For example, VASP contains its own local optimisation functions since it is not implemented in ASE. This is no issue for us! We just need to be careful to implement the local optimisation using your own program, and make sure that the RunMinimisation.py file is constructed as follows:

Input into ``Minimisation_Function``:

* **cluster** (*ASE.Atoms*): This is the unoptimised version of the cluster.
* **collection** (*str.*): This indicates if the cluster is apart of the population or an offspring.
* **cluster_name** (*int.*): This is the name of the cluster to be optimised. This should be the number of the cluster that was made during this genetic algorithm run.

returns: 

* **cluster** (*ASE.Atoms*) - This is now the optimised version of the cluster. 
* **converged** (*bool.*) - This boolean indicates if the local optimisation converged (``True`` for converged, ``False`` for did not converge).
* **Info** (*dict.*) - This sends information back to the genetic algorithm about how the local minimsation ran. 

A general script for locally optimising however you want to is given below:

.. literalinclude:: RunMinimisation_General.py
	:language: python
	:caption: RunMinimisation_General.py
	:name: RunMinimisation_General.py
	:tab-width: 4
	:linenos:

For example, this is how you might want to set your RunMinimisation.py script for locally optimising using VASP.

.. literalinclude:: RunMinimisation_VASP.py
	:language: python
	:caption: RunMinimisation_VASP.py
	:name: RunMinimisation_VASP.py
	:tab-width: 4
	:linenos:





