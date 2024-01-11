'''
Did_Find_LES.py, Geoffrey Weal, 08/03/2019

This program will determine which of your genetic algorithm trials have completed up to a certain generation. 
'''
import os, sys, subprocess

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
                if (generations is None and no_offspring_per_generation is None):
                    break
            if line.startswith('no_offspring_per_generation = '):
                no_offspring_per_generation = int(eval(line.replace('no_offspring_per_generation = ','')))
                if (generations is None and no_offspring_per_generation is None):
                    break
    if generations is None or no_offspring_per_generation is None:
        print('Error')
        print(generations)
        print(no_offspring_per_generation)
        import pdb; pdb.set_trace()
        exit('Error')
    return generations, no_offspring_per_generation

problem_trials = []
def Did_Trial_finish_successfully(filepath):
    # get decired generations and number of offspring per gerenation
    total_no_of_generation, no_offspring_per_generation = get_variables_from_run(filepath)
    # Read EnergyProfile.txt
    #with open(filepath+'/Population/EnergyProfile.txt','r') as EnergyProfileTXT:
    # --------------------------------------------------------------------------------------------------
    if not os.path.exists(filepath+'/Population/EnergyProfile.txt'):
        if os.path.exists(filepath+'/Population/current_population_details.txt'):
            with open(filepath+'/Population/current_population_details.txt','r') as current_population_detailsTXT:
                line = current_population_detailsTXT.readline()
                if line.startswith('GA Iteration: None'):
                    return False, 0 #None
                elif line.startswith('GA Iteration: 0'):
                    return False, 0
                else:
                    print('')
                    print('Error in def Did_Trial_finish_successfully, Did_Complete_Main.py')
                    print('')
                    print('Error occurred while examining: '+str(filepath))
                    print('')
                    print('There is no EnergyProfile.txt file, but current_population_details.txt says that the genetic algorithm has been running.')
                    print('Check to make sure that all files that the genetic algorithm should have made have been made.')
                    print('Especially the EnergyProfile.txt file')
                    print('See https://organisms.readthedocs.io/en/latest/Files_Made_During_the_Genetic_Algorithm.html to see what files are made and should be included as the Organisms program proceeds.')
                    print('')
                    print('This program will now finish without completing.')
                    problem_trials.append(filepath)
                    return False, -1
        else:
            print('')
            print('Error in def Did_Trial_finish_successfully, Did_Complete_Main.py')
            print('')
            print('Error occurred while examining: '+str(filepath))
            print('')
            print('Did not find a EnergyProfile.txt file, then could not find a current_population_details.txt file')
            print('If EnergyProfile.txt is not found, this may mean that the genetic algorithm was cancelled before the genetic algorithm made the population and was about to become.')
            print('For this reason, we then look to see if the current_population_details.txt to confirm there is no initial population.')
            print('This can not be verified, so best not to continue.')
            print('')
            print('What has likely happened is that the genetic algorithm has been cancelled just as it was about to begin.')
            print('The algorithm should be able to be resumed, but just in this case it is best to just start that genetic algorithm again from the beginning')
            print('')
            print('However, check to make sure that no files have been accidentally deleted.')
            print('See https://organisms.readthedocs.io/en/latest/Files_Made_During_the_Genetic_Algorithm.html to see what files are made and should be included as the Organisms program proceeds.')
            print('')
            print('This program will now finish without completing.')
            problem_trials.append(filepath)
            return False, -1
    # --------------------------------------------------------------------------------------------------
    last_lines_in_EnergyProfile = tail(filepath+'/Population/EnergyProfile.txt',no_offspring_per_generation) 
    all_cluster_gen_made = []
    finished_found_LES = False
    Restart_due_to_epoch = False
    for line in last_lines_in_EnergyProfile:
        if isinstance(line, bytes):
            line = line.decode()
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
            print(dirpath+'/'+dirname)
            print('Getting the following expection:')
            print()
            print('------------->')
            print(expection)
            print('------------->')
            print()
            print('Check this out and then repeat your program again')
            print('This program will finish here.')
            print('===================================================================')
            raise Exception(expection)
        if did_trial_finish_successfully:
            completed_Trials.append(trial_no)
        else:
            incomplete_Trials.append(trial_no)
            at_generation.append((dirname,current_gen))
        ###########
        sys.stdout.write("\r                                                                  ")
        sys.stdout.flush()
        sys.stdout.write("\rScanning Completion: "+str(round((float(index+1)/float(number_of_dirnames)*100.0),2))+" % (Checked "+str(dirname)+").")
        sys.stdout.flush()
        ###########
    completed_Trials.sort()
    incomplete_Trials.sort()
    at_generation.sort(key=lambda x:x[1])
    completed_successfully = True if len(incomplete_Trials) == 0 else False
    return completed_successfully, completed_Trials, incomplete_Trials, at_generation, problem_trials
