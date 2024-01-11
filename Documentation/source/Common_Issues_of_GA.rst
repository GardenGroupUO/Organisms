
.. _Common_Issues_of_GA:

Common Issues of the Genetic Algorithm and Ways to Solve Them
=============================================================

Randomly generated clusters all explode when creating the initial population
****************************************************************************

Here, the genetic algorithm keeps giving you the message ``Cluster exploded. Will obtain a new cluster``. Here, the genetic algorithm keeps creating a single cluster that continuously explodes over and over while you are initially setting up the initial population with randomly generated clusters. An exploded cluster means that the cluster does not form a single structure when it forms. Instead, the cluster locally minimises into two or more separate smaller clusters that are not attached to each other. This is not what we want, as we wont to make a single cluster with the specifications given in the ``cluster_makeup`` variable in the ``Run.py`` file

If this occurs, first check that your ``Minimisation`` method in your ``RunMinimisation.py`` is set up for a cluster with an element that is different to the elemental makeup of the cluster you have specified in the ``cluster_makeup`` variable in your ``Run.py`` file. The genetic algorithm proceeds but your clusters do not locally optimise because of this mismatch. Check your ``RunMinimisation.py`` and make sure that it includes the elements that you need to locally optimise, i.e. matches the ``cluster_makeup`` variable in your ``Run.py`` file.

If your ``RunMinimisation.py`` is correct and you still have this issue, this issue may be occurring because the the value that you have set for ``cell_length`` is too high. Look at systematically reducing this to a point that this doesnt happen. If you don't do this, this will likely not affect the rest of the genetic algorithm, it will just take longer than necessary to make the initial population. However, if you are using the ``random`` or ``random_XX`` mutation methods, this will cause issues during the genetic algorithm. If you are using either of these mutation methods, it is recommended that you try to set a value of ``cell_length`` where explosions are minimised. 

My cluster does not locally minimise properly of there is an error with ASAP
****************************************************************************

If your cluster is not locally minimising properly or you find there is an error with ASAP, it is likely that you have an incorrect setting in your ``RunMinimisation.py`` script. For example, you may be try to locally minimise a Cu cluster, but the calculator you are using in the ``RunMinimisation.py`` script is incorrectly set to give the potential of Au atoms only. Check your ``RunMinimisation.py`` script and then try running the genetic algorithm again. 

.. _ga_running_lock_explanation:

I have tried to run my genetic algorithm, but it won't run because it says that a file called ``ga_running.lock`` exists in the genetic algorithms directory
************************************************************************************************************************************************************

When the genetic algorithm begins, it will create a blank file called ``ga_running.lock``. This file is a lock that will prevent the user from running the genetic algorithm if it exists in the genetic algorithm's directory, i.e. preventing the user from running the genetic algorithm twice simutaneously, as this will cause major issues for your genetic algorithm if you do this by accident. This file should only exist while the genetic algorithm is running. 

This is to prevent the user from accidentally running the genetic algorithm while it is already running. However, if you had to stop the genetic algorithm without finishing it safely (see :ref:`Safely Finishing the Genetic Algorithm Midway<Safely_Finishing_the_GA_Midway>` to see what "safely" means), then this file will still be in the genetic algorithm's directory. If this is the case, and you are sure that the genetic algorithm is not running, remove the ``ga_running.lock`` file from the directory and try running the genetic algorithm again. 

The ase database website is not formatted correct/format is hard to use
***********************************************************************

This is a problem in most recent versions of ASE. Formatting does not seem to be an issue for any version of ASE version 3.19, but ASE database does not seem to be formatted properly for any version of ASE version 3.20. The current solution for this is to change the version of ase to 3.19. To do this, first uninstall ASE by typing ``pip3 uninstall ase`` in the terminal, then running ``pip3 install --user ase==3.19.3`` in the terminal. 

See :ref:`Using Databases with the Genetic Algorithm <Using_Databases_with_the_Genetic_Algorithm>` for more information on how databases work in ASE and for the genetic algorithm. 

I am having issues that some jobs are not submitted to slurm every so often when running ``Run_mass_submitSL_slurm.py`` and it is having to resubmit jobs
*********************************************************************************************************************************************************

Every so often I have found that slurm does not submit a job. This may be because too many jobs are being submitting consecutive in a short period of time, or because their is an internet issue or a slurm hang that only lasts for a few tens of seconds. 

``Run_mass_submitSL_slurm.py`` has been designed to wait for 10 seconds before attempting to resubmit the job to slurm. If ``Run_mass_submitSL_slurm.py`` has attempted to submit the current job to slurm a maximum of 20 times, then ``Run_mass_submitSL_slurm.py`` will exit and tell the user what jobs have not been submitted due to this issue. 

The amount of time that ``Run_mass_submitSL_slurm.py`` will wait before attempting to resubmit a job to slurm is given by the variable ``time_to_wait_before_next_submission_due_to_temp_submission_issue`` in ``Subsidiary_Programs/Run_mass_submitSL_slurm.py``, while the number of times that ``Run_mass_submitSL_slurm.py`` will attempt to resubmit a job to slurm before it will give up is given the variable ``number_of_consecutive_error_before_exitting`` in ``Subsidiary_Programs/Run_mass_submitSL_slurm.py``. 

See :ref:`Run_mass_submitSL_slurm.py - How to execute all Trials using the JobArray Slurm Job Submission Scheme <Run_mass_submitSL_slurm_py>` for more information about how ``Run_mass_submitSL_slurm.py`` is designed and works and the settings that you may need to change in ``Run_mass_submitSL_slurm.py`` so that it works for you in slurm. 

I found that when the fitness operator gave a ``ZeroDivisionError`` error when trying to obtain the ``CNA_fitness_contribution`` or the energy fitness value of ``rho_i``
**************************************************************************************************************************************************************************

An example of this type of error is given below for a ``ZeroDivisionError`` error for the ``CNA_fitness_contribution`` value.

.. code-block:: bash

	"/.../GA/Fitness_Operators/CNA_Fitness_Contribution.py", line 71, in get_CNA_fitness_parameter_normalised
	CNA_fitness_contribution = (CNA_most_similar_average - min_minimarity)/(max_similarity - min_minimarity) 
	ZeroDivisionError: float division by ZeroDivisionError: float division by zero

Here, either the population has no similarity span (or no energy span). In this example, this is because the cluster in the population with the highest similarity value has the same similarity as the cluster in the population with the lowest similarity value (i.e. ``max_similarity`` is equal to ``min_minimarity``). There has been an update that should prevent this from occur. However, if this problem does arise, the easiest way to potentially solve this problem is to lower your input value for ``rounding_criteria``

I can not run programs from ``Subsidiary_Programs``, ``Postprocessing_Programs``, or ``Helpful_Programs``, get the error when I run a program ``/usr/bin/env: python3: No such file or directory``
**************************************************************************************************************************************************************************************************

All programs that are used to pre- and post-processing Organsims data begins with the line

.. code-block:: bash

	#!/usr/bin/env python3

This will make sure that these programs are running in python3, rather than in python2. If you see the error:

``/usr/bin/env: python3: No such file or directory``

This means that either you have not installed python3 on your computer, or you have not loaded the python3 module in slurm.

If you are running a program in slurm, you load python by typing into the terminal

.. code-block:: bash

	module load python3_version

where ``python3_version`` is the version of python3 you want to use. To see what versions of python3 are available to you in slurm, type into the teriminal

.. code-block:: bash

	module avail python

This will give a list of versions of python3 you can use. Choose the one you would like to use and type this into the terminal as ``module load python3_version``, where ``python3_version`` is the name of the version of python3 you would like to use.

