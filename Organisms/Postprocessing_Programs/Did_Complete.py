#!/usr/bin/python
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

Overall_Trials_to_check = {}

for dirpath, dirnames, filenames in os.walk(path):
    dirnames.sort()
    if any([(dirname.startswith('Trial') and dirname.replace('Trial','').isdigit()) for dirname in dirnames]):
        completed_successfully, completed_Trials, incomplete_Trials, at_generation = has_all_trials_finished(dirpath, dirnames)
        toString = ''
        toString += '******************************************************************************\n'
        toString += '******************************************************************************\n'
        toString += 'This set of genetic algorithm trials finished '+('SUCCESSFULLY' if completed_successfully else 'UNSUCCESSFULLY')+'.\n'
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

print('########################################################################')
print('########################################################################')
print('Details of Trials that did not complete:')
if len(Overall_Trials_to_check) == 0:
    print('ALL Trials completed SUCCESSFULLY')
else:
    for dirpath, incomplete_Trials in Overall_Trials_to_check.iteritems():
        print('path: '+str(dirpath)+'; Trials to Repeat: '+str(incomplete_Trials))
print('########################################################################')
print('########################################################################')
