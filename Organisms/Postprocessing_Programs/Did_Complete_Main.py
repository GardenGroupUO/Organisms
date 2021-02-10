'''
Did_Find_LES.py, Geoffrey Weal, 08/03/2019

This program will determine which of your genetic algorithm trials have completed up to a certain generation. 
'''
import os, sys
import subprocess

def tail(f, n, offset=0):
    proc = subprocess.Popen(['tail', '-n', str(n + offset), f], stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()
    return lines

def get_variables_from_run(filepath):
    with open(filepath+'/Run.py','r') as RunPY:
        generations = None; no_offspring_per_generation = None;
        for line in RunPY:
            if line.startswith('generations = '):
                generations = int(eval(line.replace('generations = ','')))
                if (generations == None and no_offspring_per_generation == None):
                    break
            if line.startswith('no_offspring_per_generation = '):
                no_offspring_per_generation = int(eval(line.replace('no_offspring_per_generation = ','')))
                if (generations == None and no_offspring_per_generation == None):
                    break
    if generations == None or no_offspring_per_generation == None:
        print('Error')
        print(generations)
        print(no_offspring_per_generation)
        import pdb; pdb.set_trace()
        exit('Error')
    return generations, no_offspring_per_generation

def Did_Trial_finish_successfully(filepath):
    # get decired generations and number of offspring per gerenation
    total_no_of_generation, no_offspring_per_generation = get_variables_from_run(filepath)
    # Read EnergyProfile.txt
    #with open(filepath+'/Population/EnergyProfile.txt','r') as EnergyProfileTXT:
    last_lines_in_EnergyProfile = tail(filepath+'/Population/EnergyProfile.txt',no_offspring_per_generation) 
    all_cluster_gen_made = []
    finished_found_LES = False
    Restart_due_to_epoch = False
    for line in last_lines_in_EnergyProfile:
        if line.startswith('Finished prematurely as LES energy found.'):
            finished_found_LES = True
        elif line.startswith('Restarting due to epoch.'):
            Restart_due_to_epoch = True
        else:
            line = line.split()
            generation = int(line[1])
            all_cluster_gen_made.append(generation)
    if finished_found_LES:
        return True, all_cluster_gen_made[0]
    if Restart_due_to_epoch:
        return False, all_cluster_gen_made[0]
    if not (len(set(all_cluster_gen_made)) == 1):
        print('1')
        import pdb; pdb.set_trace()
        exit('Error')
    all_cluster_gen_made = all_cluster_gen_made[0]
    if all_cluster_gen_made < total_no_of_generation:
        return False, all_cluster_gen_made
    elif all_cluster_gen_made == total_no_of_generation:
        return True, all_cluster_gen_made
    else:
        #print('2')
        #import pdb; pdb.set_trace()
        #exit('Error')
        print('Note, you have performed more than enough generations for: '+str(filepath))
        return True, all_cluster_gen_made

def has_all_trials_finished(dirpath, dirnames):

    completed_Trials = []
    incomplete_Trials = []
    at_generation = []
    dirnames = [dirname for dirname in dirnames if dirname.startswith('Trial')]
    dirnames.sort(key=lambda dirname: int(dirname.replace('Trial','')))
    number_of_dirnames = len(dirnames)
    for index in range(number_of_dirnames):
        dirname = dirnames[index]
        trial_no = int(dirname.replace('Trial',''))
        try:
            did_trial_finish_successfully, current_gen = Did_Trial_finish_successfully(dirpath+'/'+dirname)
        except Exception as expection:
            print('===================================================================')
            print('Error in def has_all_trials_finished in Did_Complete_Main.py')
            print('Something weird is happening with Trial '+str(trial_no))
            print('Getting the following expection:')
            print()
            print('------------->')
            print(expection)
            print('------------->')
            print()
            print('Check this out and then repeat your program again')
            print('This program will finish here.')
            exit ('===================================================================')
        if did_trial_finish_successfully:
            completed_Trials.append(trial_no)
        else:
            incomplete_Trials.append(trial_no)
            at_generation.append((dirname,current_gen))
        ###########
        sys.stdout.write("\r                                                                  ")
        sys.stdout.flush()
        sys.stdout.write("\rScanning Completion: "+str(float(index+1)/float(number_of_dirnames)*100.0)+" % (Checked "+str(dirname)+").")
        sys.stdout.flush()
        ###########
    completed_Trials.sort()
    incomplete_Trials.sort()
    at_generation.sort(key=lambda x:x[1])
    completed_successfully = True if len(incomplete_Trials) == 0 else False
    return completed_successfully, completed_Trials, incomplete_Trials, at_generation
