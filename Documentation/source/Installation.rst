
.. _Installation:

Installation: Setting Up the Organisms Program and Pre-Requisites Packages
##########################################################################

In this article, we will look at how to install the genetic algorithm and all requisites for this program.

.. contents::
    :depth: 2
    :local:

Pre-requisites
==============

Python 3 and ``pip3``
---------------------

This program is designed to work with **Python 3**. While this program has been designed to work with Python 3.6, it should work with any version of Python 3 that is the same or later than 3.6.

To find out if you have Python 3 on your computer and what version you have, type into the terminal

.. code-block:: bash

	python3 --version

If you have Python 3 on your computer, you will get the version of python you have on your computer. E.g.

.. code-block:: bash

	geoffreyweal@Geoffreys-Mini Documentation % python3 --version
	Python 3.6.3

If you have Python 3, you may have ``pip3`` installed on your computer as well. ``pip3`` is a python package installation tool that is recommended by Python for installing Python packages. To see if you have ``pip3`` installed, type into the terminal

.. code-block:: bash

	pip3 list

If you get back a list of python packages install on your computer, you have ``pip3`` installed. E.g.

.. code-block:: bash

	geoffreyweal@Geoffreys-Mini Documentation % pip3 list
	Package                       Version
	----------------------------- ---------
	alabaster                     0.7.12
	asap3                         3.11.10
	ase                           3.20.1
	Babel                         2.8.0
	certifi                       2020.6.20
	chardet                       3.0.4
	click                         7.1.2
	cycler                        0.10.0
	docutils                      0.16
	Flask                         1.1.2
	idna                          2.10
	imagesize                     1.2.0
	itsdangerous                  1.1.0
	Jinja2                        2.11.2
	kiwisolver                    1.2.0
	MarkupSafe                    1.1.1
	matplotlib                    3.3.1
	numpy                         1.19.1
	packaging                     20.4
	Pillow                        7.2.0
	pip                           20.2.4
	Pygments                      2.7.1
	pyparsing                     2.4.7
	python-dateutil               2.8.1
	pytz                          2020.1
	requests                      2.24.0
	scipy                         1.5.2
	setuptools                    41.2.0
	six                           1.15.0
	snowballstemmer               2.0.0
	Sphinx                        3.2.1
	sphinx-pyreverse              0.0.13
	sphinx-rtd-theme              0.5.0
	sphinx-tabs                   1.3.0
	sphinxcontrib-applehelp       1.0.2
	sphinxcontrib-devhelp         1.0.2
	sphinxcontrib-htmlhelp        1.0.3
	sphinxcontrib-jsmath          1.0.1
	sphinxcontrib-plantuml        0.18.1
	sphinxcontrib-qthelp          1.0.3
	sphinxcontrib-serializinghtml 1.1.4
	sphinxcontrib-websupport      1.2.4
	urllib3                       1.25.10
	Werkzeug                      1.0.1
	wheel                         0.33.1
	xlrd                          1.2.0

If you do not see this, you probably do not have ``pip3`` installed on your computer. If this is the case, check out `PIP Installation <https://pip.pypa.io/en/stable/installing/>`_

.. note::

	In most cases, ``pip`` and ``pip3`` are synonymous for the Python Installation Package for Python 3. **However in some cases,** ``pip`` **will be directed to the Python Installation Package for Python 2 rather than Python 3.** To check this, run in the terminal:

	.. code-block:: bash

		pip --version

	If the output indicates you this Python Installation Package is for Python 2 and not Python 3, only install packages using the ``pip3`` name. 

	For the rest of this documentation, ``pip`` will be used, however if your computer's ``pip``  refers to Python 2 and not Python 3, use ``pip3``  instead of ``pip``. 


Atomic Simulation Environment
-----------------------------

This genetic algorithm uses the atomic simulation environment (ASE) for two purposes. The description of a cluster that has been designed for this algorithm is based on that given by ASE's Atoms class. This allows the genetic algorithm to take advantage of the features of ASE, such as the wide range of calculators that can be used to calculate the energy of the cluster, and the local optimisers available to optimise offspring created during the genetic algorithm. Furthermore, ASE also offers useful tools for viewing, manipulating, reading and saving clusters and chemcial systems easily. Read more about `ASE here <https://wiki.fysik.dtu.dk/ase/>`_. For this genetic algorithm, it is recommended that you **install a version of ase that is 3.19.1 or greater**.

The installation of ASE can be found on the `ASE installation page <https://wiki.fysik.dtu.dk/ase/install.html>`_, however from experience if you are using ASE for the first time, it is best to install ASE using pip, the package manager that is an extension of python to keep all your program easily managed and easy to import into your python. 

To install ASE using pip, perform the following in your terminal.

.. code-block:: bash

	pip3 install --upgrade --user ase

Installing using ``pip3`` ensures that ASE is being installed to be used by Python 3, and not Python 2. Installing ASE like this will also install all the requisite program needed for ASE. This installation includes the use of features such as viewing the xyz files of structure and looking at ase databases through a website. These should be already assessible, which you can test by entering into the terminal:

.. code-block:: bash

	ase gui

This should show a gui with nothing in it, as shown below.

.. figure:: Images/ase_gui_blank.png
   :align: center
   :figwidth: 50%
   :alt: ase_gui_blank

   This is a blank ase gui screen that you would see if enter ``ase gui`` into the terminal.

However, in the case that this does not work, we need to manually add a path to your ``~/.bashrc`` so you can use the ASE features externally outside python. First enter the following into the terminal:

.. code-block:: bash

	pip3 show ase

This will give a bunch of information, including the location of ase on your computer. For example, when I do this I get:

.. code-block:: bash

	Geoffreys-Mini:~ geoffreyweal$ pip show ase
	Name: ase
	Version: 3.20.1
	Summary: Atomic Simulation Environment
	Home-page: https://wiki.fysik.dtu.dk/ase
	Author: None
	Author-email: None
	License: LGPLv2.1+
	Location: /Users/geoffreyweal/Library/Python/3.6/lib/python/site-packages
	Requires: matplotlib, scipy, numpy
	Required-by: 

In the 'Location' line, if you remove the 'lib/python/site-packages' bit and replace it with 'bin'. The example below is for Python 3.6. 

.. code-block:: bash

	/Users/geoffreyweal/Library/Python/3.6/bin

This is the location of these useful ASE tools. You want to put this as a path in your ``~/.bashrc`` as below:

.. code-block:: bash

	############################################################
	# For ASE
	export PATH=/Users/geoffreyweal/Library/Python/3.6/bin:$PATH
	############################################################

Packaging
---------

The packaging program is also used in this program to check the versions of ASE that you are using for compatibility issues. Easiest way to install packaging is though pip. Type the following into the terminal:

.. code-block:: bash

	pip3 install --upgrade --user packaging

As Soon As Possible (ASAP)
--------------------------

As Soon As Possible (ASAP) is not a pre-requisite of this program, however it is a great source of empirical potentials that can be used to calculate the energies of clusters and chemical systems with ASE and with this program. It is required however if you want to use either the ``SCM-based predation operator`` or the ``structure + energy fitness operator`` (click here for more information on the :ref:`SCM-based predation operator <SCM_Based_Predation_Operator>` and the :ref:`structure + energy fitness operator <make_energy_vs_similarity_results>`). You can read more about it at `ASAP <https://wiki.fysik.dtu.dk/asap/>`_. You can find out how to install it at `ASAP Installation <https://wiki.fysik.dtu.dk/asap/Installation>`_, however I have found the best way to use it simply is using pip. To install using pip, perform the following in the terminal. 

.. code-block:: bash

	pip3 install --upgrade --user asap3==3.11.10

Where we install asap3 version 3.11.10. Generally, this program takes a bit of time to install. **NOTE: We require that you use asap3 version 3.11.10. This is because we have noticed a (core dump) issue that seems to occur during the genetic algorithm. Unfortunately, this error appears at seemingly random times so we don't know what the problem is, but it seems to be resolved if you use this version of asap3**

.. _Installation_of_the_Genetic_Algorithm:

Setting up Organisms
====================

There are two ways to install Organisms on your system. These ways are described below:

Install Organisms through ``pip3``
----------------------------------

To install the Organisms program using ``pip3``, perform the following in your terminal.

.. code-block:: bash

	pip3 install --upgrade --user Organisms

You should be able to access the genetic algorithm as well as run the scripts and commands described in :ref:`Helpful Programs to Create and Run the Genetic Algorithm <HelpfulPrograms_CreatingAndRunningGA>`, :ref:`Helpful Programs for Gathering data and Post-processing Data <HelpfulPrograms_GatherAndPostprocessingData>`, and :ref:`Other Helpful Programs for Gathering data and Post-processing Data <HelpfulPrograms_Others>` in the terminal.

The website for Organisms on ``pip3`` can be found by clicking the button below:

.. image:: https://img.shields.io/pypi/v/Organisms
   :target: https://pypi.org/project/Organisms/
   :alt: PyPI

Install Organisms through ``conda``
-----------------------------------

You can also install Organisms through ``conda``, however I am not as versed on this as using ``pip3``. See `docs.conda.io <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.html>`_ to see more information about this. Once you have installed anaconda on your computer, I believe you install the Organisms program using ``conda`` by performing the following in your terminal.

.. code-block:: bash

	conda install ase
	conda install asap3
	conda install organisms

The website for Organisms on ``conda`` can be found by clicking the button below:

.. image:: https://img.shields.io/conda/v/gardengroupuo/organisms
   :target: https://anaconda.org/GardenGroupUO/organisms
   :alt: Conda

Manual installation
-------------------

First, download Organisms to your computer. You can do this by cloning a version of this from Github, or obtaining a version of the program from the authors. If you are obtaining this program via Github, you want to ``cd`` to the directory that you want to place this program in on the terminal, and then clone the program from Github through the terminal as well. It is recommended that you install a release version of Organisms on your computer as these release versions are tested to make sure they are (hopefully) running as they should be prior to them being released. 

.. code-block:: bash
	
	cd PATH/TO/WHERE_YOU_WANT_Organisms_TO_LIVE_ON_YOUR_COMPUTER
	git clone https://github.com/GardenGroupUO/Organisms --branch 3.2.7.1

.. Next, add a python path to it in your  ``.bashrc`` to indicate its location. First you want to ``cd`` into the newly cloned ``Organisms`` folder and then enter into the terminal ``pwd``

.. #code-block bash

	cd Organisms
	pwd

You can find out what releases are available by entering into the terminal:

.. code-block:: bash

	git ls-remote --tags --exit-code --refs https://github.com/GardenGroupUO/Organisms.git

.. note::

	If you would like to use the most recent version of Organisms that is still under testing, you can do this by doing the following in the terminal: 

	.. code-block:: bash
		
		cd PATH/TO/WHERE_YOU_WANT_Organisms_TO_LIVE_ON_YOUR_COMPUTER
		git clone https://github.com/GardenGroupUO/Organisms

Next, you need to change permissions to use this program by using ``chmod``. In the terminal write:

.. code-block:: bash

	chmod -R 777 Organisms

Next, add a python path to it in your  ``.bashrc`` to indicate its location. Do this by entering into the terminal where you cloned the Organisms program into ``pwd``

.. code-block:: bash

	pwd

This will give you the path to the Organisms program. You want to enter the result from ``pwd`` into the ``.bashrc`` file. This is done as shown below:

.. code-block:: bash

	export PATH_TO_GA="<Path_to_Organisms>" 
	export PYTHONPATH="$PATH_TO_GA":$PYTHONPATH

where ``"<path_to_Organisms>"`` is the directory path that you place Organisms (Enter in here the result you got from the ``pwd`` command). Once you have run ``source ~/.bashrc``, the genetic algorithm should be all ready to go!

Organisms contains many parts to it. You will see that there are six folders. These are ``GA``, ``Subsidiary_Programs``, ``Postprocessing_Programs``, ``Helpful_Programs``, ``Examples`` and ``Documentation``. 

The genetic algorithm is completely contained in the folder ``GA``. If everything is working as it should, and you do not want to modify the genetic algorithm program, you shouldnt need to access it. 

The folder called ``Examples`` contains all the files that one would want to used to use the genetic algorithm. This includes examples of the basic run code for the genetic algorithm, the ``Run.py`` and ``RunMinimisation.py`` files (in the Playground folder), as well as the files that can be used to create, execute, and coagulate data from multiple runs of the genetic algorithm (in the CreateSets folder). 

This genetic algorithm contains many programs that can help you create and run the genetic algorithm (in ``Subsidiary_Programs``), for postprocessing the data from your genetic algorithm(s) (``Postprocessing_Programs``), and other helpful programs for determining how the algorithm has run or for learning other things about your genetic algorithm runs (``Helpful_Programs``). To execute any of these programs contained within either the ``Subsidiary_Programs``, ``Postprocessing_Programs``, or ``Helpful_Programs`` folders, include the following in your ``~/.bashrc``:

.. code-block:: bash

	export PATH="$PATH_TO_GA"/Organisms/Subsidiary_Programs:$PATH
	export PATH="$PATH_TO_GA"/Organisms/Postprocessing_Programs:$PATH
	export PATH="$PATH_TO_GA"/Organisms/Helpful_Programs:$PATH

See :ref:`Helpful Programs to Create and Run the Genetic Algorithm <HelpfulPrograms_CreatingAndRunningGA>`, :ref:`How Organisms Works <How_Organisms_Works>` for more information about the programs that are available in the ``Subsidiary_Programs`` and ``Postprocessing_Programs`` folders respectively. You can also see :ref:`Other Helpful Programs for Gathering data and Post-processing Data <HelpfulPrograms_Others>` for information on how to use the scripts found in the ``Helpful_Programs`` folder.

Other Useful things to know before you start
````````````````````````````````````````````

* You may use ``squeue`` to figure out what jobs are running in slurm. For monitoring what genetic algorithm jobs are running, I have found the following alias useful. Include the following in your ``~/.bashrc`` (see :ref:`How to execute all Trials using the JobArray Slurm Job Submission Scheme <Run_mass_submitSL_slurm_py>` for what is going on in the below line)

.. code-block:: bash

	alias qme='squeue -o "%.20i %.9P %.5Q %.50j %.8u %.8T %.10M %.11l %.6D %.4C %.6b %.20S %.20R %.8q" -u $USER --sort=+i'

* If you are just testing out the Organisms program, sometimes you may want to delete all of the files that the genetic algorithm created and start again to make sure everything is working. An easy way to remove all the files that Organisms created is by adding the following alias to your ``~/.bashrc``

.. code-block:: bash

	alias delALL='rm -rf GA_Run_Details.txt epoch_data epoch_data.backup ga_running.lock Population Recorded_Data Initial_Population Saved_Points_In_GA_Run Memory_Operator_Data Diversity_Information __pycache__'

Note that ``delALL`` may give the error ``zsh: no matches found:`` if you are using ``zsh`` and one of the files or directories in the ``delALL`` line does not exist. To prevent this from happening and to get ``delALL`` to delete all the files or directories in this line of code despite of if they exists or not, add the following line to your ``~/.bashrc``:

.. code-block:: bash

	setopt +o nomatch

This solution was obtained from `stackexchange <https://unix.stackexchange.com/questions/310540/how-to-get-rid-of-no-match-found-when-running-rm>`_

Summary of what you want in the ``~/.bashrc`` for the Organisms program if you manually installed the Organisms
```````````````````````````````````````````````````````````````````````````````````````````````````````````````

You want to have the following in your ``~/.bashrc``:

.. code-block:: bash

	#########################################################
	# Paths and Pythonpaths for the genetic algorithm

	export PATH_TO_GA="<Path_to_Organisms>" 
	export PYTHONPATH="$PATH_TO_GA":$PYTHONPATH

	export PATH="$PATH_TO_GA"/Organisms/Subsidiary_Programs:$PATH
	export PATH="$PATH_TO_GA"/Organisms/Postprocessing_Programs:$PATH
	export PATH="$PATH_TO_GA"/Organisms/Helpful_Programs:$PATH

	alias qme='squeue -o "%.20i %.9P %.5Q %.50j %.8u %.8T %.10M %.11l %.6D %.4C %.6b %.20S %.20R %.8q" -u $USER --sort=+i'

	alias delALL='rm -rf GA_Run_Details.txt epoch_data epoch_data.backup ga_running.lock Population Recorded_Data Initial_Population Saved_Points_In_GA_Run Memory_Operator_Data Diversity_Information __pycache__'
	setopt +o nomatch # if you are using zsh and getting the "zsh: no matches found:" error

	#########################################################

