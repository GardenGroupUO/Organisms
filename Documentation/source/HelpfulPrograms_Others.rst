
.. _HelpfulPrograms_Others:

Other Helpful Programs for Gathering data and Post-processing Data
##################################################################

There are also a few other programs that have been designed that may be helpful for various reasons, but are not absolutely necessary for Postprocessing. In this article, we will introduce all these scripts, indicating what they do and how to use them. Some of these programs can be run by typing the program you want to run into the terminal from whatever directory you are in, but some of them you may need to copy to where you need to use them. 

The scripts and programs that we will be mentioned here are:

.. contents::
    :depth: 1
    :local:

What to make sure is done before running any of these scripts. 
**************************************************************

If you installed Organisms through pip3
---------------------------------------

If you installed the Organisms program with ``pip3``, these scripts will be installed in your bin. You do not need to add anything into your ``~/.bashrc``. You are all good to go. 

If you performed a Manual installation
--------------------------------------

If you have manually added this program to your computer (such as cloning this program from Github), you will need to make sure that you have included the ``Helpful_Programs`` folder into your ``PATH`` in your ``~/.bashrc`` file. All of these program can be found in the `Helpful_Programs` folder. To execute some of these programs from the ``Helpful_Programs`` folder, you must include the following in your ``~/.bashrc``:

.. code-block:: bash

	export PATH_TO_GA="<Path_to_Organisms>" 

where ``<Path_to_Organisms>"`` is the path to get to the genetic algorithm program. Also include somewhere before this in your ``~/.bashrc``:

.. code-block:: bash

	export PATH="$PATH_TO_GA"/Organisms/Helpful_Programs:$PATH

See more about this in :ref:`Installation of the Genetic Algorithm <Installation_of_the_Genetic_Algorithm>`. 

The ``delALL`` command
**********************

The ``delALL`` command will remove all the files that are created during a genetic algorithm. To use it, write the following line into your ``~/.bashrc``:

.. code-block:: bash

	alias delALL='rm -rf GA_Run_Details.txt epoch_data epoch_data.backup ga_running.lock Population Recorded_Data Initial_Population Saved_Points_In_GA_Run Memory_Operator_Data Diversity_Information __pycache__'

Note that ``delALL`` may give the error ``zsh: no matches found:`` if you are using ``zsh`` and one of the files or directories in the ``delALL`` line does not exist. To prevent this from happening and to get ``delALL`` to delete all the files or directories in this line of code despite of if they exists or not, add the following line to your ``~/.bashrc``:

.. code-block:: bash

	setopt +o nomatch

This solution was obtained from `stackexchange <https://unix.stackexchange.com/questions/310540/how-to-get-rid-of-no-match-found-when-running-rm>`_


