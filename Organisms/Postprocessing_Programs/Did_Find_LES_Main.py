'''
Did_Find_LES_Main.py, Geoffrey Weal, 08/03/2019

This program Will determine which of your genetic algorithm trials have found the cluster with the energy given to a certain decimal place.
'''
import os, sys
import numpy as np
import scipy.stats

def Rounding_Method(number,rounding_criteria):
    """
    This definition will round the input number to the decimal place specified by rounding_criteria.
    The input number in the genetic algorithm is usually the energy of the cluster.

    :param number: The value that you would like to round (usually energy)
    :type  number: float
    :param rounding_criteria: The number of decimal places the value should be rounded to.
    :type  rounding_criteria: int
    
    """
    if rounding_criteria > 12:
        print('Error, the maximum decimal place rounding, to avoid numerical errors, is 12')
        print('rounding_criteria: '+str(rounding_criteria))
        exit('Check this out')
    number = round(number,rounding_criteria)
    return number

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    ci = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, ci

class has_all_trials_found_LES:

    def __init__(self,energy_LES, max_generation_to_survey, set_rounding):
        self.energy_LES = Rounding_Method(float(energy_LES),set_rounding)
        self.max_generation_to_survey = max_generation_to_survey
        self.set_rounding = set_rounding
        self.run()
        self.print_those_that_all_trials_did_not_all_find_LES()

    def print_those_that_all_trials_did_not_all_find_LES(self):
        results_all_found_LES = []
        results_not_all_found_LES = []
        for dirpath, all_number_of_true_trials, all_total_no_of_trials in self.results:
            if all_number_of_true_trials == all_total_no_of_trials:
                results_all_found_LES.append((dirpath, all_number_of_true_trials, all_total_no_of_trials))
            else:
                results_not_all_found_LES.append((dirpath, all_number_of_true_trials, all_total_no_of_trials))
        print('# ------------------------------------------------------------------ #')
        if not results_all_found_LES == []:
            print('Jobs that all trials found the LES')
            for dirpath, all_number_of_true_trials, all_total_no_of_trials in results_all_found_LES: 
                print(str(dirpath)+' ('+str(all_number_of_true_trials)+' out of '+str(all_total_no_of_trials)+')')
        else:
            print('No Jobs were completed that all trials found the LES')
        print('# ------------------------------------------------------------------ #')
        if not results_not_all_found_LES == []:
            print('Jobs that NOT all trials found the LES')
            for dirpath, all_number_of_true_trials, all_total_no_of_trials in results_not_all_found_LES: 
                print(str(dirpath)+' ('+str(all_number_of_true_trials)+' out of '+str(all_total_no_of_trials)+')')
        else:
            print('For all Jobs, all trials found the LES')
        print('# ------------------------------------------------------------------ #')

    def run(self):
        path = os.getcwd()
        Overall_Trials_to_check = {}
        self.results = []
        for dirpath, dirnames, filenames in os.walk(path):
            dirnames.sort()
            if any([(dirname.startswith('Trial') and dirname.replace('Trial','').isdigit()) for dirname in dirnames]):
                print('Getting LES data for '+str(dirpath))
                LES_Details = self.get_found_LES_Details(dirpath, dirnames, self.energy_LES, self.max_generation_to_survey, self.set_rounding)
                toString = ''
                toString += '******************************************************************************\n'
                toString += '******************************************************************************\n'
                toString += 'This is the information of the LES of these genetic algorithm trials.\n'
                toString += 'Trial\tfound LES\tdir\tGen.\n'
                for LES_of_a_Trial in LES_Details:
                    LES_Trial, found_LES, LES_clu_dir, LES_gen = LES_of_a_Trial
                    toString += str(LES_Trial)+'\t'+str(found_LES)+'\t'+str(LES_clu_dir)+'\t'+str(LES_gen)+'\n'
                toString += '******************************************************************************\n'
                toString += '******************************************************************************\n'
                toString += 'Overall Details'+'\n'
                number_of_true_trials = [x for x in LES_Details if x[1] == True]
                number_of_true_trials = len(number_of_true_trials)
                total_no_of_trials = len(LES_Details)
                toString += 'Number of trials that located the LES: '+str(number_of_true_trials)+' out of '+str(total_no_of_trials)+'\n'
                print(toString)
                toString += '******************************************************************************\n'
                toString += '******************************************************************************\n'
                #with open(dirpath+'/DidFind_LESOfTrials.txt','w') as LESOfTrials:
                #    LESOfTrials.write(toString)
                name = dirpath.replace(path+'/','')
                name = name.replace('/','_')
                #with open(path+'/'+ name+'_DidFind_LESOfTrials.txt','w') as LESOfTrials:
                #    LESOfTrials.write(toString)
                dirnames[:] = []
                filenames[:] = []
                #self.make_file_of_data(dirpath,None,LES_Details,energy_LES)
                #self.make_file_of_data(path,name,LES_Details,energy_LES)
                self.results.append((dirpath, number_of_true_trials, total_no_of_trials))

        print('########################################################################')
        print('########################################################################')
        
        print('########################################################################')
        print('########################################################################')

    def get_found_LES_Details(self, dirpath, dirnames, energy_LES, max_generation_to_survey, rounding):

        def Lowest_Energy_from_Trial(filepath, energy_LES, max_generation_to_survey, rounding):
            #LES_clu_dir = -1; LES_gen = -1;
            LES_clu_dir = None; LES_gen = None;
            found_LES = False
            if os.path.exists(filepath):
                got_to_trial = False
                pop_size = 0
                no_of_off_per_gen = 0
                last_gen_counter = 0
                with open(filepath,'r') as DETAILS_FILE:
                    for line in DETAILS_FILE:
                        if line.startswith('Genetic Algorithm Starts Here.'):
                            continue
                        if line.startswith('Restarting due to epoch.'):
                            continue
                        if line.startswith('Finished prematurely as LES energy found.'):
                            got_to_trial = True
                            to_string = 'Error: You have found the message "Finished prematurely as LES energy found." in your energyprofile.txt, but you didnt locate the cluster energy you entered. Check that the energy you put in is the energy of the LES, and run this program again. This error occurred for dirpath: '+str(filepath)
                            raise Exception(to_string)
                            break
                        clu_dir, gen, energy = line.rstrip().split()
                        clu_dir = int(clu_dir); gen = int(gen)
                        if gen == 0:
                            pop_size += 1
                        if gen == 1:
                            no_of_off_per_gen += 1
                        if gen == max_generation_to_survey:
                            got_to_trial = True
                            last_gen_counter += 1
                        if gen > max_generation_to_survey:
                            break
                        energy = Rounding_Method(float(energy),rounding)
                        if energy == energy_LES:
                            LES_clu_dir = clu_dir; LES_gen = gen;
                            found_LES = True
                            got_to_trial = True
                            break
                        #if energy < energy_LES:
                        #    LES_clu_dir = clu_dir; LES_gen = gen; energy_LES = energy
                if got_to_trial == False:
                    print(filepath)
                    print('Error, 2. Gen: '+ str(gen))
                    import pdb; pdb.set_trace()
                    exit()
                if gen == max_generation_to_survey:
                    if last_gen_counter < no_of_off_per_gen:
                        exit('Error, 3')
            return found_LES, LES_clu_dir, LES_gen

        LES_Data_from_Trials = []
        dirnames = [dirname for dirname in dirnames if dirname.startswith('Trial')]
        dirnames.sort(key=lambda dirname: int(dirname.replace('Trial','')))
        number_of_dirnames = len(dirnames)
        for index in range(number_of_dirnames):
            dirname = dirnames[index]
            trial_no = int(dirname.replace('Trial',''))
            found_LES, LES_clu_dir, LES_gen = Lowest_Energy_from_Trial(dirpath+'/'+dirname+'/Population/EnergyProfile.txt',energy_LES,max_generation_to_survey,rounding)
            LES_Data_from_Trials.append([dirname, found_LES, LES_clu_dir, LES_gen])
            ###########
            sys.stdout.write("\r                                                                  ")
            sys.stdout.flush()
            sys.stdout.write("\rScanning Completion: "+str(float(index+1)/float(number_of_dirnames)*100.0)+" % (Checked "+str(dirname)+").")
            sys.stdout.flush()
            ###########
        LES_Data_from_Trials.sort(key=lambda x:x[1],reverse=False)
        return LES_Data_from_Trials

    def make_file_of_data(self, dirpath, name, LES_Details, energy_LES):

        if not name in ['', None]:
            name += '_'

        success_at_gens = [0]*(self.max_generation_to_survey+1)
        LES_Details.sort(key=lambda x:x[3],reverse=False)
        putative_LES_energy = LES_Details[0][3]
        for dirname, LES_clu_dir, LES_gen, LES_energy in LES_Details:
            if LES_energy == putative_LES_energy:
                success_at_gens[LES_gen] += 1

        with open(dirpath+'/'+str(name)+'first_instance_up_to_'+str(self.max_generation_to_survey)+'.txt','w') as first_instanceTXT:
            generation = 0
            for success_at_gen in success_at_gens:
                first_instanceTXT.write(str(generation)+': '+str(success_at_gen)+'\n')
                generation += 1

        success_at_gens_collaborated = [0]
        for success_at_gen in success_at_gens:
            at_gen_success = success_at_gens_collaborated[-1] + success_at_gen
            success_at_gens_collaborated.append(at_gen_success)
        del success_at_gens_collaborated[0]

        with open(dirpath+'/'+str(name)+'_did_find_LES_'+str(energy_LES)+'_up_to_'+str(self.max_generation_to_survey)+'.txt','w') as successTXT:
            generation = 0
            for success_at_gen_collaborated in success_at_gens_collaborated:
                successTXT.write(str(generation)+': '+str(success_at_gen_collaborated)+'\n')
                generation += 1

