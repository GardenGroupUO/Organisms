#!/usr/bin/python
'''
HasCompletedUpToGeneration.py, Geoffrey Weal, 08/03/2019

This program will determine if the genetic algorithm has completed up to a certain generation. 

This program will also return the success of your genetic algorithm trials in obtaining the putative global minimum as well as the average number of minimisations required to obtain the putative global minimum.

To get the proper average number of minimisations, you want to enter your generations value to infinity. You can do this by not entering in a value of the generation. The default is set to infinity.
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

class GetLESOfAllTrials_Main:

    def __init__(self,max_generation_to_survey,set_rounding):
        self.max_generation_to_survey = max_generation_to_survey
        self.set_rounding =set_rounding
        self.run()

    def run(self):
        path = os.getcwd()
        Overall_Trials_to_check = {}
        for dirpath, dirnames, filenames in os.walk(path):
            dirnames.sort()
            if any([(dirname.startswith('Trial') and dirname.replace('Trial','').isdigit()) for dirname in dirnames]):
                print('Getting LES data for '+str(dirpath))
                LES_Details = self.get_LES_Details(dirpath, dirnames, self.max_generation_to_survey, self.set_rounding)
                #import pdb; pdb.set_trace()
                toString = ''
                toString += '******************************************************************************\n'
                toString += '******************************************************************************\n'
                toString += 'This is the information of the LES of these genetic algorithm trials.\n'
                toString += 'Trial\tdir\tGen.\tEnergy (eV)\n'
                for LES_of_a_Trial in LES_Details:
                    LES_Trial, LES_clu_dir, LES_gen, LES_energy = LES_of_a_Trial
                    toString += str(LES_Trial)+'\t'+str(LES_clu_dir)+'\t'+str(LES_gen)+'\t'+str(LES_energy)+'\n'
                toString += '******************************************************************************\n'
                toString += '******************************************************************************\n'
                toString += 'Overall Details'+'\n'
                toString += 'Lowest Recorded LES: '+str(LES_Details[0][3])+' eV or equivalent.\n'
                LLES_Details = [x for x in LES_Details if x[3] == LES_Details[0][3]]
                toString += 'No of Trials that got this LES: '+str(len(LLES_Details))+' out of '+str(len(LES_Details))+'\n'
                all_gens = [x[2] for x in LLES_Details]
                average_gen, ci_gen = mean_confidence_interval(all_gens)
                toString += 'Average Generation: '+str(average_gen)+' +- '+str(ci_gen)+'\n'
                all_dirs = [x[1] for x in LLES_Details]
                average_dir, ci_dir = mean_confidence_interval(all_dirs)
                percentage_of_successful_trials = (float(len(LLES_Details))/float(len(LES_Details)))*100.0
                percentage_of_successful_trials = round(percentage_of_successful_trials,1)
                toString += 'Average Number of Minimisations (of the '+str(len(LLES_Details))+' successful trials ('+str(percentage_of_successful_trials)+' %)): '+str(average_dir)+' +- '+str(ci_dir)+'\n'
                print(toString)
                toString += '******************************************************************************\n'
                toString += '******************************************************************************\n'
                with open(dirpath+'/LESOfTrials_'+str(self.max_generation_to_survey)+'.txt','w') as LESOfTrials:
                    LESOfTrials.write(toString)
                name = dirpath.replace(path+'/','')
                name = name.replace('/','_')
                with open(path+'/'+ name+'_LESOfTrials'+str(self.max_generation_to_survey)+'.txt','w') as LESOfTrials:
                    LESOfTrials.write(toString)
                dirnames[:] = []
                filenames[:] = []
                self.make_file_of_data(dirpath,None,LES_Details)
                self.make_file_of_data(path,name,LES_Details)

        print('########################################################################')
        print('########################################################################')
        
        print('########################################################################')
        print('########################################################################')

    def get_LES_Details(self, dirpath, dirnames, max_generation_to_survey, rounding):

        def Lowest_Energy_from_Trial(filepath, rounding):
            LES_clu_dir = -1; LES_gen = -1; LES_energy = float('inf')
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
                        if energy < LES_energy:
                            LES_clu_dir = clu_dir; LES_gen = gen; LES_energy = energy
                if got_to_trial == False:
                    print(filepath)
                    print('Error, 2. Gen: '+ str(gen))
                    import pdb; pdb.set_trace()
                    exit()
                if gen == max_generation_to_survey:
                    if last_gen_counter < no_of_off_per_gen:
                        exit('Error, 3')
            return LES_clu_dir, LES_gen, LES_energy

        LES_Data_from_Trials = []
        dirnames = [dirname for dirname in dirnames if dirname.startswith('Trial')]
        dirnames.sort(key=lambda dirname: int(dirname.replace('Trial','')))
        number_of_dirnames = len(dirnames)
        for index in range(number_of_dirnames):
            dirname = dirnames[index]
            trial_no = int(dirname.replace('Trial',''))
            LES_clu_dir, LES_gen, LES_energy = Lowest_Energy_from_Trial(dirpath+'/'+dirname+'/Population/EnergyProfile.txt',rounding)
            LES_Data_from_Trials.append([dirname, LES_clu_dir, LES_gen, LES_energy])
            ###########
            sys.stdout.write("\r                                                                  ")
            sys.stdout.flush()
            sys.stdout.write("\rScanning Completion: "+str(float(index+1)/float(number_of_dirnames)*100.0)+" % (Checked "+str(dirname)+").")
            sys.stdout.flush()
            ###########
        LES_Data_from_Trials.sort(key=lambda x:x[3],reverse=False)
        return LES_Data_from_Trials

    def make_file_of_data(self, dirpath, name, LES_Details):

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

        with open(dirpath+'/'+str(name)+'success_up_to_'+str(self.max_generation_to_survey)+'.txt','w') as successTXT:
            generation = 0
            for success_at_gen_collaborated in success_at_gens_collaborated:
                successTXT.write(str(generation)+': '+str(success_at_gen_collaborated)+'\n')
                generation += 1
