
.. _Safely_Finishing_the_GA_Midway:

Safely Finishing the Genetic Algorithm Midway through the Algorithm
###################################################################

In some cases, if you are running the genetic algorithm, or have submitted the genetic algorithm trials through slurm, you may want to cancel the genetic algorithm from running before the genetic algorithm had completed. The algorithm is designed to be cancelled at any point during the algorithm and should be able to be restarted, but if possible it is recommended that this program is safely finished, meaning the algorithm completes the generation it is currently performing before finishing. 

This program can be finished safely by making a file called `finish` in the same directory that the `Run.py` is in. Nothing needs to be added to this finish file. If the algorithm finds this `finish` file it will finish once the current generation has completed. 

If you are running a mass number of genetic algorithms that you would like to safely finish, there is a program called ``make_finish_files.py`` that will add a ``finish`` file to any subdirectories from where you ran the ``make_finish_files.py`` program that also contain a ``Run.py`` file. 

To run this program, type ``make_finish_files.py`` into the terminal. This program will deposit a ``finish`` file in any subdirectory that contains a ``Run.py`` file. 

*Do you think that the genetic algorithm will not finish before your job times out on slurm or whatever computer cluster job scheduler cancels your genetic algorithm job?* Ultimately, this should not be an issue as the genetic algorithm has been designed to be cancelled unsafely. However, safely cancelling the genetic algorithm is perferred just in case there is a further bug in the program. Read up about the ``total_length_of_running_time`` parameter in :ref:`Other details of the Genetic algorithm<total_length_of_running_time>` to learn about how to tell the genetic algorithm to automatically safely finish after a certain period of time.  