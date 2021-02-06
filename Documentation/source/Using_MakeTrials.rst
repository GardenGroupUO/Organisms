
.. _Using_MakeTrials:

*MakeTrials.py* - Creating Multiple, Repeated Genetic Algorithm Trials
######################################################################

Typically, it is common that one will not run just one genetic algorithm run, but multiple genetic algorithm runs with the same parameters. This can a pain to set up all the files to make the multiple runs and run them all. It can also be very hard to analyse all the data together, since there is just so much! Therefore, we have developed a set of scripts to make this experience less painful for the user.

In this article, we will look at how to use some of the tools that have been developed to create and run many genetic algorithm runs on slurm. Slurm (Slurm Workload Manager) is a Linux resource management system for running a computer cluster system. See `Slurm Workload Manager <https://slurm.schedmd.com/documentation.html>`_ for more information about slurm. 

In the next article (:ref:`Helpful Programs for Gathering data and Post-processing Data <HelpfulPrograms_GatherAndPostprocessingData>`) we describe a set of scripts to analyse the data from the multiple genetic algorithms.

What to make sure is done before running the MakeTrials.py program. 
*******************************************************************

If you installed the Organisms program using``pip3``, you do not need to do anything extra, you are all good to go. 

If you have manually added this program to your computer (such as cloning this program from Github), you will need to make sure that you have included the Subsidiary_Programs folder into your ``PATH`` and ``PYTHONPATH`` in your ``~/.bashrc`` file. To execute programs in Subsidiary_Programs, you must include the following in your ``~/.bashrc``:

.. code-block:: bash

	export PATH=<Path_to_Organisms_Program>/Subsidiary_Programs:$PATH
	export PYTHONPATH=<Path_to_Organisms_Program>/Subsidiary_Programs:$PYTHONPATH

See more about this in :ref:`Installation of the Genetic Algorithm <Installation_of_the_Genetic_Algorithm>`

How does MakeTrials.py work?
****************************

MakeTrials.py is a script which uses the ``MakeTrialsProgram`` class in ``SubsidiaryPrograms.MakeTrialsProgram`` (found in SubsidiaryPrograms/MakeTrialsProgram.py) to make all the files that one would need to make to perform a set of repeated the genetic algorithm upon a cluster system. This will create lots of the same genetic algorithm files (Run.py and RunMinimisation.py) and put them into folders called Trials. 

You can find another example of a ``Run.py`` file at `github.com/GardenGroupUO/Organisms <https://github.com/GardenGroupUO/Organisms>`_ under ``Examples\Playground``.

Setting up MakeTrials.py
************************

MakeTrials.py is designed to make all the trials desired for a specific cluster system. This is designed to be as customisable as possible. A typical MakeTrials.py script will look as follows:

.. literalinclude:: MakeTrials.py
	:language: python
	:caption: MakeTrials.py
	:name: MakeTrials.py
	:tab-width: 4
	:linenos:

We will now explain the components of this script. Many of the variable have been explained in :ref:`Run.py - Using the Genetic Algorithm <Using_Run>`. These are ``cluster_makeup``, ``surface_details``, ``pop_size``, ``generations``, ``no_offspring_per_generation``, ``creating_offspring_mode``, ``crossover_type``, ``mutation_types``, ``chance_of_mutation``, ``epoch_settings``, ``r_ij``, ``cell_length``, ``vacuum_to_add_length``, ``Minimisation_Function``, ``memory_operator_information``, ``predation_information``,  ``fitness_information``, ``ga_recording_information``, ``force_replace_pop_clusters_with_offspring``, ``user_initilised_population_folder``, ``rounding_criteria``, ``print_details``, ``no_of_cpus``, ``finish_algorithm_if_found_cluster_energy`` and ``total_length_of_running_time``.

Here, we will cover the meaning for variables ``dir_name``, ``NoOfTrials``, ``Condense_Single_Mention_Experiments``, ``making_files_for`` and ``JobArraysDetails``.

1) Details to create all the desired trials
===========================================

These include the details needed for this program to make the trials desired. These variables are:

	* **dir_name** (*str.*): This is the name of the folder to put the trials into.
	* **NoOfTrials** (*int.*): This is the number of trials you would like to create.
	* **Condense_Single_Mention_Experiments** (*bool.*): This program is designed to place the trials in a ordered system. If this is set to true, the trials will be put in a folder called XN_P_p_O_o, where XN is the cluster makeup, p is the size of the population, and o is the number of offspring make per generations. If this is set to False, the directory that will be made will be X/XN/Pop_p/Off_o, where X are the elements that make up the cluster, XN is the cluster makeup, p is the size of the population, and o is the number of offspring make per generations.
	* **making_files_for** (*str.*): This tells how the MakeTrials program will write files for performing multiple genetic algorithm trials. See :ref:`How files are created for running multiple genetic algorithm trials <Using_MakeTrials_making_files_for>` for more information about this.   
	* **no_of_packets_to_make** (*int*): If ``making_files_for = 'slurm_JobArrays_packets'``, then this tells the MakeTrials program how to split the **NoOfTrials** number of genetic algorithm trials into packets. See :ref:`How files are created for running multiple genetic algorithm trials <Using_MakeTrials_making_files_for>` for more information about this.   

An example of these parameters in MakeTrials.py is given below:

.. literalinclude:: MakeTrials.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 63
	:lines: 63-69

1.1) ``making_files_for``: How files are created for running multiple genetic algorithm trials
----------------------------------------------------------------------------------------------
.. _Using_MakeTrials_making_files_for:

This option is designed to write the ``submit.sl`` or ``mass_submit.sl`` scripts that you need for running multiple genetic algorithm trial jobs on slurm. There are three options for this setting. These options for ``JobArraysDetails['mode']`` are ``'individual'``, ``'slurm_JobArrays_full'``, and ``'slurm_JobArrays_packets'``.

If ``'individual'``, MakeTrials will create a slurm.sl file for each individual genetic algorithm trial. 

If ``'slurm_JobArrays_full'``, MakeTrials will create a mass_slurm.sl file will submit an array job that performs ``NoOfTrials`` genetic algorithm trials. An example of this shown below. 

.. literalinclude:: mass_submit_full.sl
	:language: bash
	:caption: mass_submit_full.sl
	:name: mass_submit_full.sl
	:tab-width: 4
	:linenos:

If ``'slurm_JobArrays_packets'``, MakeTrials will create a mass_slurm.sl file will submit an array job that performs ``NoOfTrials`` genetic algorithm trials. However, these will be run as ``no_of_packets_to_make`` number of packets that are running on slurm, where each packet is made up of :math:`\frac{\rm{NoOfTrials}}{\rm{no\_of\_packets\_to\_make}}` genetic algorithm trials that are run in series. Use the ``'slurm_JobArrays_packets'`` setting if you think each individual genetic algorithm trial will run for only a short amount of time (less than 5-10 minutes on average). The reason for using this setting rather than ``'slurm_JobArrays_full'`` is because running lots of short jobs on slurm can cause issues for the slurm controller that controls the queue on slurm. 

IMPORTANT: Make sure that the amount of time you have given for ``JobArraysDetails['time']`` is much greater than the maximum amount of time you think each trial will be completed in times ``no_of_packets_to_make``, i.e.

.. math::

	\rm{maximum\,amount\,of\,time\,to\,run\,one\,GA\,trial} \times \frac{\rm{NoOfTrials}}{\rm{no\_of\_packets\_to\_make}} << \rm{JobArraysDetails['time']}

If the below is not true, then it is recommended to use a partition on slurm that allows you to set :math:{\rm{JobArraysDetails['time']}} to as long as possible so that the above equation is true. If you cant do this, consider breaking up running all your GA trials with a greater value of ``no_of_packets_to_make`` (up to :math:{\rm{no\_of\_packets\_to\_make} = \frac{\rm{NoOfTrials}}{2}}). If you cant do this as well, lower your value of ``NoOfTrials`` and do all your trials bit by bit (for example, if performing 1,000,000 trials, first run trials 1-1000, then trials 1001-2000, then trials 2001-3000, so on ...). 

Avoid using ``'slurm_JobArrays_full'`` if possible as performing lots of small jobs on slurm can break slurm. If you cant avoid it, use ``'slurm_JobArrays_full'`` with caution. 

As a guideline, set ``JobArraysDetails['time']`` to as large a wall time as possible for the partition you are using on your slurm cluster. 

An example of this shown below.

.. literalinclude:: mass_submit_packets.sl
	:language: bash
	:caption: mass_submit_packets.sl
	:name: mass_submit_packets.sl
	:tab-width: 4
	:linenos:

2) Slurm Details
================

The ``JobArraysDetails`` dictionary contains all the information that will be needed to write the ``submit.sl`` or ``mass_submit.sl`` scripts that you need for running multiple genetic algorithm trial jobs on slurm. The parameters to be entered into the ``JobArraysDetails`` dictionary are:

	* **project** (*str.*): The name of the project to run this on.
	* **partition** (*str.*): The partition to run this on.
	* **time** (*str.*): The length of time to give these jobs. This is given in ‘HH:MM:SS’, where HH is the number of hours, MM is the number of minutes, and SS is the number of seconds to run the genetic algorithm for.
	* **nodes** (*int*): The number of nodes to use. Best to set this to 1. 
	* **ntasks_per_node** (*int*): The number of cpus to run these jobs across on a node. It is best to set this to the same value as ``no_of_cpus`` in the ``MakeTrials.py`` file. 
	* **mem** (*str.*): This is the memory that is used in total by the job.
	* **email** (*str.*): This is the email address to send slurm messages to about this job. If you do not want to give an email, write here either ``None`` or ``''``.
	* **python version** (*str.*): This give the submit script the version of python to load when submitting this job on slurm. The default is ``'Python/3.6.3-gimkl-2017a'``. However, if instead you want to use Python 3.7, you could write here ``JobArraysDetails['python version'] = 'Python/3.7.3-gimkl-2018b'``. In slurm write ``module avail python`` to find out what versions of python you have available on your computer cluster system. 

See `sbatch - Slurm Workload Manager - SchedMD <https://slurm.schedmd.com/sbatch.html>`_ and `The Slurm job scheduler <http://www.arc.ox.ac.uk/content/slurm-job-scheduler>`_ to learn more about these parameters in the submit.sl script for slurm.

An example of these parameters in MakeTrials.py is given below:

.. literalinclude:: MakeTrials.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 71
	:lines: 71-80

3) Time to Run the MakeTrials Program
=====================================

Now all there is to do is to run this program!

.. literalinclude:: MakeTrials.py
	:language: python
	:tab-width: 4
	:linenos:
	:lineno-start: 82
	:lines: 83-114

Can I make writing trials easily for many types of system.
**********************************************************

The answer is yes. This program has been designed to be as flexible as possible. For example, the following MakeTrials script will make 100 trials for various types of cluster systems, and for various population and offspring per generation sizes.

.. literalinclude:: MakeTrials_Multiple.py
	:language: python
	:caption: MakeTrials_Multiple.py
	:name: MakeTrials_Multiple.py
	:tab-width: 4
	:linenos: