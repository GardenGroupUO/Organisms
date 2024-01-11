#!/usr/bin/env python3
'''
Did_Find_LES.py, Geoffrey Weal, 08/03/2019

This program will determine which of your genetic algorithm trials have completed up to a certain generation. 
'''
import os
from Organisms.Postprocessing_Programs.Did_Complete_Main import has_all_trials_finished

path = os.getcwd()

def did_Trial_finish_successfully(filepath):
    with open(filepath,'r') as DETAILS_FILE:
        for line in DETAILS_FILE:
            if line.startswith("The Genetic Algorithm finished successfully."):
                return True
    return False

number_of_trials = []
Overall_Trials_to_check = {}

all_problem_trials = []

for dirpath, dirnames, filenames in os.walk(path):
    dirnames.sort()
    if any([(dirname.startswith('Trial') and dirname.replace('Trial','').isdigit()) for dirname in dirnames]):
        completed_successfully, completed_Trials, incomplete_Trials, at_generation, problem_trials = has_all_trials_finished(dirpath, dirnames)
        toString = ''
        toString += '******************************************************************************\n'
        toString += '******************************************************************************\n'
        toString += 'This set of genetic algorithm trials finished '+('SUCCESSFULLY' if completed_successfully else 'UNSUCCESSFULLY')+'.\n'
        toString += '\n'
        toString += '# Successful Trials: '+str(len(completed_Trials))+';\t# Unsuccessful Trials: '+str(len(incomplete_Trials))+';\tTotal # of Trials: '+str(len(completed_Trials)+len(incomplete_Trials))+'\n'
        number_of_trials.append((dirpath,len(completed_Trials),len(incomplete_Trials)))
        toString += '\n'
        toString += 'The following Trials in '+str(dirpath)+' completed or did not complete.\n'
        toString += 'Completed Trials: '+str(completed_Trials)+'\n'
        toString += 'Incomplete Trials: '+str(incomplete_Trials)+'\n'
        toString += 'There were '+str(len(incomplete_Trials))+' incomplete trials.\n'
        if not at_generation == []:
            toString += 'The current generation of the incomplete trials:\n'
            for trial_gen in at_generation:
                toString += str(trial_gen[0])+': Gen '+str(trial_gen[1])+'\n'
        toString += '******************************************************************************\n'
        toString += '******************************************************************************\n'
        print(toString)
        with open(dirpath+'/TrialsCompletionDetails.txt','w') as TrialsCompletionDetailsTXT:
            TrialsCompletionDetailsTXT.write(toString)
        dirnames[:] = []
        filenames[:] = []
        if not completed_successfully:
            Overall_Trials_to_check[dirpath] = incomplete_Trials
        all_problem_trials += problem_trials

print('########################################################################')
print('########################################################################')
number_of_trials.sort()
print('Number of Trials that were performed for each set of trials:')
for dirpath, no_of_successful, no_of_unsuccessful in number_of_trials:
    print(dirpath+': '+str(no_of_successful+no_of_unsuccessful)+'\t(successful: '+str(no_of_successful)+'; unsuccessful: '+str(no_of_unsuccessful)+')')
print('########################################################################')
print('########################################################################')
print('Details of Trials that did not complete:')
if len(Overall_Trials_to_check) == 0:
    print('ALL Trials completed SUCCESSFULLY')
else:
    for dirpath, incomplete_Trials in Overall_Trials_to_check.items():
        print('path: '+str(dirpath)+'; Trials to Repeat: '+str(incomplete_Trials))
print('########################################################################')
print('########################################################################')
if not len(all_problem_trials) == 0:
    print('There were also a few problem trials that this Did_Complete.py program had errors with. These should be checked out as something may be wrong with the trial itself and may just need to be reset.')
    print('This could be for example a file was accidentally deleted')
    print('These problem trials are:')
    print('')
    for problem_trial in all_problem_trials:
        print(str(problem_trial))
    print('')
    print('########################################################################')
    print('########################################################################')
