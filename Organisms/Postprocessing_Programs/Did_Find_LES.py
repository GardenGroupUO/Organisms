#!/usr/bin/python
'''
Did_Find_LES.py, Geoffrey Weal, 08/03/2019

This program Will determine which of your genetic algorithm trials have found the cluster with the energy given to a certain decimal place.
'''
import os, sys
from Organisms.Postprocessing_Programs.Did_Find_LES_Main import has_all_trials_found_LES

path = os.getcwd()

# ---------------------------------------------------------------------- #
import re
def get_input_energy_float(input_message):
    while True:
        get_input = str(raw_input(str(input_message)+' [No default]?: '))
        if re.match(r'^-?\d+(?:\.\d+)?$', get_input) is None:
            print('Error. Your input must be an float.')
        try:
            return float(get_input)
        except:
            print('Error. Your input must be an integer.')

def get_input_int(input_message,default_input):
    if not isinstance(default_input,int):
        print('Error in get_input_int of Coagulate_EnergyProfiles.py')
        print('The default_input must be an int')
        print('default_input: '+str(default_input))
        print('Check this out')
        import pdb; pdb.set_trace()
        exit()
    while True:
        get_input = str(raw_input(str(input_message)+' ['+str(default_input)+']?: '))
        get_input.lower()
        if get_input == '':
            get_input = str(default_input)
        if not get_input.isdigit():
            print('Error. Your input must be an integer.')
        else:
            return int(get_input)

energy_LES = get_input_energy_float('What is the energy of the LES?')
set_rounding = get_input_int('What rounding of the energy would you like to set?',12)
max_generation_to_survey = get_input_int('What generation would you like to survey up to?',sys.maxsize)

# ---------------------------------------------------------------------- #

has_all_trials_found_LES(energy_LES, max_generation_to_survey, set_rounding)