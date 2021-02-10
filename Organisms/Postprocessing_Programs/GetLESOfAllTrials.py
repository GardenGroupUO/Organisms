#!/usr/bin/python
'''
HasCompletedUpToGeneration.py, Geoffrey Weal, 08/03/2019

This program will determine if your genetic algorithm trials has completed up to a certain generation. 

This program will also determine how many genetic algorithm trials have found th eputative global minimum from across all the trials, as well as the average number of minimisations required to obtain the putative global minimum up to the generation specified

If you want to get the most complete average number of generations required to obtain the putative global minimum, make sure you run all your genetic algorithm trials so that they have all found the true global minimum, then set the generation to search up to to infinity (you do not need to enter a generation, the default setting is infinity).

'''
import sys
from Organisms.Postprocessing_Programs.GetLESOfAllTrials_Main_v3 import GetLESOfAllTrials_Main

################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################

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

def get_int(given_input):
    given_input = str(given_input)
    given_input.lower()
    if not given_input.isdigit():
        print('Error. Your input must be an integer.')
    else:
        return int(given_input)

number_of_sys_argvs = len(sys.argv)

if number_of_sys_argvs == 1:
    max_generation_to_survey = get_input_int('What generation would you like to survey up to?',sys.maxsize)
    set_rounding = get_input_int('What rounding of the energy would you like to set?',12)
elif number_of_sys_argvs == 2:
    max_generation_to_survey = get_int(sys.argv[1])
    print('Generation to survey up to: '+str(max_generation_to_survey))
    set_rounding = get_input_int('What rounding of the energy would you like to set?',12)
elif number_of_sys_argvs == 3:
    max_generation_to_survey = get_int(sys.argv[1])
    print('Generation to survey up to: '+str(max_generation_to_survey))
    set_rounding = get_int(sys.argv[2])
    print('Rounding of the energy to set: '+str(set_rounding))

GetLESOfAllTrials_Main(max_generation_to_survey,set_rounding)