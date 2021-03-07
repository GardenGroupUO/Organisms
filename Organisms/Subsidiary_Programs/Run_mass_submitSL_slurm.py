#!/usr/bin/python
'''
Geoffrey Weal, Run_mass_submitSL_slurm.py, 10/02/2021

This program is designed to submit all sl files called mass_submit.sl to slurm

'''
print('###########################################################################')
print('###########################################################################')
print('Run_mass_submitSl_slurm.py')
print('###########################################################################')
print('This program is designed to submit all your mass_submit.sl scripts appropriately to slurm.')
print('###########################################################################')
print('###########################################################################')

import os, time, sys
import subprocess

# ------------------------------------------------------
# These variables can be changed by the user.
Max_jobs_in_queue_at_any_one_time = 10000
time_to_wait_before_next_submission = 20.0
time_to_wait_max_queue = 60.0

time_to_wait_before_next_submission_due_to_temp_submission_issue = 10.0
number_of_consecutive_error_before_exitting = 20
# ------------------------------------------------------

if len(sys.argv) > 1:
    wait_between_submissions = str(sys.argv[1]).lower()
    if wait_between_submissions in ['t','true']:
        wait_between_submissions = True
    elif wait_between_submissions in ['f','false']:
        wait_between_submissions = False
    else:
        print('If you pass this program an argument, it must be either: ')
        print('    t, true, True: will wait 1 minute between submitting jobs')
        print('    f, false. False: will not wait between submitting jobs')
        print('If no argument is entered, the default is given as True')
        exit('This program will exit without running')
else:
    wait_between_submissions = True

if wait_between_submissions == True:
    print('This program will wait one minute between submitting jobs.')
else:
    print('This program will not wait between submitting jobs.')
path = os.getcwd()

def countdown(t):
    print('Will wait for ' + str(float(t)/60.0) + ' minutes, then will resume Pan submissions.\n')
    while t:
        mins, secs = divmod(t, 60)
        timeformat = str(mins) + ':' + str(secs)
        #timeformat = '{:02d}:{:02d}'.format(mins, secs)
        sys.stdout.write("\r                                                                                   ")
        sys.stdout.flush()
        sys.stdout.write("\rCountdown: " + str(timeformat))
        sys.stdout.flush()
        time.sleep(1)
        t -= 1
    print('Resuming Pan Submissions.\n')

def myrun(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_lines = [line for line in iter(proc.stdout.readline,'')]
    #import pdb; pdb.set_trace()
    #proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #stdout_lines = [line for line in io.TextIOWrapper(proc.stdout, encoding="utf-8")]
    """from http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html"""
    '''
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = []
    while True:
        line = p.stdout.readline()
        stdout.append(line)
        if line == '' and p.poll() != None:
            break
    '''
    return ''.join(stdout_lines)

###########################################################################################
###########################################################################################
###########################################################################################

def get_number_to_trials_that_will_be_submitted_by_mass_submitSL(dirpath):
    path_to_mass_submitSL = dirpath+'/mass_submit.sl'
    with open(path_to_mass_submitSL,'r') as mass_submitSL:
        for line in mass_submitSL:
            if '#SBATCH --array=' in line:
                trials = line.replace('#SBATCH --array=','')
                no_of_trials_that_will_be_submitted = 0
                worked_successfully = True
                trial_limits_commands = trials.rstrip().split(',')
                for trial_limits in trial_limits_commands:
                    if trial_limits.count('-') == 1:
                        trial_limits = trial_limits.split('-')
                        if len(trial_limits) == 2 and trial_limits[0].isdigit() and trial_limits[1].isdigit():
                            no_of_trials_that_will_be_submitted =+ int(trial_limits[1]) - int(trial_limits[0]) + 1
                        else:
                            worked_successfully = False
                            break
                    elif trial_limits.isdigit():
                        no_of_trials_that_will_be_submitted += 1
                    else:
                        worked_successfully = False
                        break
                if worked_successfully:
                    return no_of_trials_that_will_be_submitted
                else:
                    print('========================================================')
                    print('Error in submitting: '+str(path_to_mass_submitSL))
                    print('One of the clusters in the array to be submitted is not a integer or is entered incorrectly.')
                    print()
                    print(line)
                    print()
                    print('Check this line in your submit.sl script')
                    print('This program will now exit')
                    exit ('========================================================')         
    print('Error in def get_number_to_trials_that_will_be_submitted_by_mass_submitSL, in Run_mass_submitSl_slurm.py script, found in the folder SubsidiaryPrograms in this GA program.')
    print('The mass_submit.sl script found in '+str(dirpath)+' does not have the line that starts with "#SBATCH --array=" in the script.')
    print('Just check this script to make sure everything is all good.')
    import pdb; pdb.set_trace()
    print('This program will finish')
    exit()

command = "squeue -r -u $USER"
def check_max_jobs_in_queue_after_next_submission(dirpath):
    while True:
        text = myrun(command)
        nlines = len(text.splitlines())-1
        if not (nlines == -1):
            break
        else:
            print('Could not get the number of jobs in the slurm queue. Retrying to get this value.')
    number_of_trials_to_be_submitted = get_number_to_trials_that_will_be_submitted_by_mass_submitSL(dirpath)
    if nlines > Max_jobs_in_queue_at_any_one_time - number_of_trials_to_be_submitted:
        return True, nlines
    else:
        return False, nlines

###########################################################################################
###########################################################################################
###########################################################################################

# Check to make sure the array line in all mass_submit.sl scripts is there and that none of the mass_submission script submit more than Max_jobs_in_queue_at_any_one_time
# into the queue. 
print('-----------------------------------------------')
print('Checking to make sure that the array line in all mass_submit.sl scripts is there and that none of the mass_submission script submit more than Max_jobs_in_queue_at_any_one_time into the queue.')
for (dirpath, dirnames, filenames) in os.walk(path):
    dirnames.sort()
    if 'mass_submit.sl' in filenames:
        no_of_trials_that_will_be_submitted = get_number_to_trials_that_will_be_submitted_by_mass_submitSL(dirpath)
        if no_of_trials_that_will_be_submitted > Max_jobs_in_queue_at_any_one_time:
            print('Issue: The number of Trials that you want to submit is greater the number of trials you are allowed to submit at any one time.')
            print('Number of jobs that will be submitted by '+str(dirpath)+'/mass_submit.sl: '+str(no_of_trials_that_will_be_submitted))
            print('Maximum number of trials that can be submitted into slurm: '+str(Max_jobs_in_queue_at_any_one_time))
            print('Consider doing either:')
            print('    1) Using the scripts Create_submitSL_slurm.py and Run_submitSL_slurm.py to run your jobs. This will submit your jobs individually and has better control over submitting this large number of trials within slurm without causing issues with slurm.')
            print('    2) Contact your slurm technical support about increasing the maximum number of jobs that can be found in the queue at any one time.')
            print('This program will exit without doing anything.')
            exit()
        dirnames[:] = []
        filenames[:] = []
print('All clear to submit your mass_submit.sl scripts.')
print('-----------------------------------------------')
print('*****************************************************************************')
print('*****************************************************************************')
print('Submitting mass_submit.sl scripts to slurm.')

# Time to submit all the GA scripts! Lets get this stuff going!
submitting_command = "sbatch mass_submit.sl"
for (dirpath, dirnames, filenames) in os.walk(path):
    dirnames.sort()
    if 'mass_submit.sl' in filenames:
        # determine if it is the right time to submit jobs
        print('*****************************************************************************')
        while True:
            reached_max_jobs, number_in_queue = check_max_jobs_in_queue_after_next_submission(dirpath)
            if reached_max_jobs:
                print('-----------------------------------------------------------------------------')
                print('You can not have any more jobs in the queue before submitting the mass_sub. Will wait a bit of time for some of them to complete')
                print('Number of Jobs in the queue = '+str(number_in_queue))
                countdown(time_to_wait_before_next_submission)
                print('-----------------------------------------------------------------------------')
            else:
                print('The number of jobs in the queue currently is: '+str(number_in_queue))
                break
        # submit the jobs
        os.chdir(dirpath)
        name = dirpath.replace(path, '').split('/', -1)[1:]
        name = "_".join(str(x) for x in name)
        print("Submitting " + str(name) + " to slurm.")
        error_counter = 0
        while True:
            if error_counter == number_of_consecutive_error_before_exitting:
                break
            else:
                proc = subprocess.Popen(submitting_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if not proc.wait() == 0:
                    error_counter += 1
                    if error_counter == number_of_consecutive_error_before_exitting:
                        print('----------------------------------------------')
                        print('Error in submitting submit script to slurm.')
                        print('I got '+str(number_of_consecutive_error_before_exitting)+" consecutive errors. Something must not be working right somewhere. I'm going to stop here just in case something is not working.")
                        print('')
                        print('The following mass_submit.sl scripts WERE NOT SUBMITTED TO SLURM')
                        print('')
                    else:
                        stdout, stderr = proc.communicate()
                        print('----------------------------------------------')
                        print('Error in submitting submit script to slurm. This error was:')
                        print(stderr)
                        print('Number of consecutive errors: '+str(error_counter))
                        print('Run_mass_submitSL_slurm.py will retry submitting this job to slurm after '+str(time_to_wait_before_next_submission_due_to_temp_submission_issue)+' seconds of wait time')
                        print('----------------------------------------------')
                        countdown(time_to_wait_before_next_submission_due_to_temp_submission_issue)
                else:
                    break
        if error_counter == number_of_consecutive_error_before_exitting:
            print(dirpath)
        elif not wait_between_submissions:
            pass # do not wait any time before proceeding to the next submission.
        else:
            reached_max_jobs, number_in_queue = check_max_jobs_in_queue_after_next_submission(dirpath)
            print('The number of jobs in the queue after submitting job is currently is: '+str(number_in_queue))
            print('Will wait for '+str(time_to_wait_max_queue)+' to give time between consecutive submissions')
            countdown(time_to_wait_max_queue)
            print('*****************************************************************************')
        dirnames[:] = []
        filenames[:] = []

if error_counter == number_of_consecutive_error_before_exitting:
    print('----------------------------------------------')
    print()
    print('"Run_mass_submitSL_slurm.py" will finish WITHOUT HAVING SUBMITTED ALL JOBS.')
    print()
    print('*****************************************************************************')
    print('NOT ALL mass_submit.sl SCRIPTS WERE SUBMITTED SUCCESSFULLY.')
    print('*****************************************************************************') 
else:
    print('*****************************************************************************')
    print('*****************************************************************************')
    print('*****************************************************************************')
    print('All mass_submit.sl scripts have been submitted to slurm successfully.')
    print('*****************************************************************************')
    print('*****************************************************************************')
    print('*****************************************************************************')