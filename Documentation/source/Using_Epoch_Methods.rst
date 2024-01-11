.. _Using_Epoch_Methods:

Using Epoch Methods
###################

An epoch method is designed to reset the population with a set of randomly generated clusters if the epoch method believes that the population has stagnated. 

In this article, we describe the types of epoch schemes that are available, as well as other settings that are avilable that allow the epoch method to do other things

.. contents::
    :depth: 2
    :local:

Types of Epoch Methods
======================

There are three types of Epoch methods available. These are no epoch method, the mean energy epoch method, and the same population epoch method. For no epoch method, set ``epoch_settings = {'epoch mode': None}``

Mean Energy Epoch Method
------------------------

This method is designed to reset the population is the mean energy of clusters in the population does not decrease after a generation. To use this method, set ``'epoch mode': 'mean energy'`` in your ``epoch_settings`` dictionary. 

To use this method, you need to also include the following setting in your ``epoch_settings`` dictionary. 

* 'mean energy difference': The mean energy must decrease by at this this amount after every generation to avoid an epoch.


Same Population Epoch Method
----------------------------

This method is designed to reset the population if no offspring replace any of the clusters in the population after so many generations. To use this method, set ``'epoch mode': 'same population'`` in your ``epoch_settings`` dictionary.

To use this method, you need to also include the following setting in your ``epoch_settings`` dictionary. 

* 'max repeat': This is the number of generations that the population can stay the same without being epoched. If the population does not change after this many generations, the population will be epoched. 

Other Settings
==============

There are other settings that you can set in the epoch method.

* **first epoch changes fitness operator to energy fitness operator** (*bool*): The epoch method is designed to reset the population with a set of randomly generated clusters once the population stagnates. However, there is another option. This other option works as follows: When the population stagnates for the first time, the population does not epoch but instead the fitness operator changes to the energy fitness operator. It is only once the population stagnates for a second time that the epoch method will reset the population. This method only works if you have not set the fitness operator to the energy fitness operator or if you have selected the structure + energy fitness operator but have set ``SCM_fitness_contribution`` to ``0.0``. (Default: ``False``) 

Epoch Method files
==================

The epoch method will make a file called ``epoch_data``, which contains all the information about the epoch for the current generation. There is also a file called ``epoch_data.backup`` which contains the epoch information about the last successful generation. The first line of these files is the generation that that epoch data is valid for. For the other lines, this information depends on the epoch method chosen.

Mean Energy Epoch Method
------------------------

The second line gives the mean energy of the population from the last successful generation. 

Same Population Epoch Method
----------------------------

The second line contains the list of the names of all the clusters in the last unique population. The third line indicates the recent number of generations that have had the same population.