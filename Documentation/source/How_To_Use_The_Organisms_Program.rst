
.. _How_To_Use_The_Organisms_Program:

How To Use The Organisms Program
================================

This program uses an input python file that contains all the information needed to run the Organisms program. This is called the **Run.py** file. You can read more about how to construct this file in :ref:`Run.py - Using the Organisms program <Using_Run>`. Executing the Run.py file will perform the genetic algorithm for a cluster of your choosing. The genetic algorithm can also be run on a cluster on a surface if required. An example of the Run.py file can be found in Examples/Playground

However, it is likely that one genetic algorithm run may not be enough to confidently obtain the global minimum structure. This is because the genetic algorithm, or any global optimisation algorithm, is not guaranteed to locate the global minimum structure, and therefore the global minimum may not be found the first time the genetic algorithm is used. For this reason, this program comes a few extra scripts to make and simutaneously run multiple genetic algorithms easier, including setting up files to be used with the slurm job schedule manager. The Examples/CreateSets folder contains a file called **MakeTrials.py** that will create many repeated trials, using the same genetic algorithm parameters. You can use this program to create and organise your directory to run multiple genetic algorithm runs. Read more about this feature at :ref:`MakeTrials.py - Creating Multiple, Repeated Genetic Algorithm Trials <Using_MakeTrials>`. 

There are two further pages that contain information that is useful for working with this program. 

* :ref:`Helpful Programs to Create and Run the Genetic Algorithm <HelpfulPrograms_CreatingAndRunningGA>` contains information about all the programs that can be used to create other files, such as randomly generated clusters, and run them on mass with as minimal work required by the user as possible. Note again that information on how to use make a number of repeated trials on mass can be found in :ref:`MakeTrials.py - Creating Multiple, Repeated Genetic Algorithm Trials <Using_MakeTrials>`. 
* :ref:`Helpful Programs for Gathering and Post-processing Data <HelpfulPrograms_GatherAndPostprocessingData>` contains information about programs designed for processing all the trials together, such as programs to check that all the trials had completed, determining the generations and number of minimisations required to obtain the lowest energy cluster each trial could find, the average number of generations and average number of minimisations required to obtain the lowest energy cluster from any of the trials performed, and more post-processing programs. 
