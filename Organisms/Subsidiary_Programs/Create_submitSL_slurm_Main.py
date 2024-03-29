'''
Geoffrey Weal, Create_submitSL_slurm_Main.py, 10/02/2021

This program is designed to create the various forms of submit.sl/mass_submit.sl files that could be used to submit genetic algorithm trials to slurm.
'''

def make_submitSL(local_path,project,time,nodes,ntasks_per_node,mem=None,mem_per_cpu=None,partition='large',email='',python_version='Python/3.6.3-gimkl-2017a'):
    # create name for job
    print("creating submit.sl for "+str(local_path))
    name = local_path.replace('/','_')
    # writing the submit.sl script
    with open("submit.sl", "w") as submitSL:
        submitSL.write('#!/bin/bash -e\n')
        submitSL.write('#SBATCH -J ' + str(name) + '\n')
        submitSL.write('#SBATCH -A ' + str(project) + '         # Project Account\n')
        submitSL.write('#SBATCH --partition ' + str(partition) + '\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --time=' + str(time) + '     # Walltime\n')
        submitSL.write('#SBATCH --nodes=' + str(nodes) + '\n')
        submitSL.write('#On VASP, Ben Roberts recommends using the same number\n')
        submitSL.write('#of tasks on all nodes, even if this makes scheduling\n')
        submitSL.write('#a little more difficult\n')
        submitSL.write('#SBATCH --ntasks-per-node=' + str(ntasks_per_node) + '\n')
        add_mem_to_submitSL(submitSL,mem=mem,mem_per_cpu=mem_per_cpu)
        #submitSL.write('#SBATCH -C sb\n')
        submitSL.write('\n')
        #submitSL.write("#SBATCH --hint=nomultithread    # don't use hyperthreading"+'\n')
        submitSL.write('#SBATCH --output=slurm-%j.out      # %x and %j are replaced by job name and ID'+'\n')
        submitSL.write('#SBATCH --error=slurm-%j.err'+'\n')
        if not email == '':
            submitSL.write('#SBATCH --mail-user=' + str(email) + '\n')
            submitSL.write('#SBATCH --mail-type=ALL\n')
        submitSL.write('\n')
        submitSL.write('module load '+str(python_version)+'\n')
        submitSL.write('python Run.py\n')

def make_mass_submitSL_full(local_path,project,no_of_trials,time,nodes,ntasks_per_node,mem=None,mem_per_cpu=None,partition='large',email='',RunMinimisation_Script_Name='RunMinimisation',python_version='Python/3.6.3-gimkl-2017a'):
    # create name for job
    print("creating mass_submit.sl for "+str(local_path))
    name = local_path.replace('/','_')
    # writing the mass_submit.sl script
    with open(local_path+'/'+"mass_submit.sl", "w") as submitSL:
        submitSL.write('#!/bin/bash -e\n')
        submitSL.write('#SBATCH -J ' + str(name) + '\n')
        submitSL.write('#SBATCH -A ' + str(project) + '         # Project Account\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --array=1-'+str(no_of_trials)+'\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --time=' + str(time) + '     # Walltime\n')
        submitSL.write('#SBATCH --nodes=' + str(nodes) + '\n')
        submitSL.write('#SBATCH --ntasks-per-node=' + str(ntasks_per_node) + '\n')
        add_mem_to_submitSL(submitSL,mem=mem,mem_per_cpu=mem_per_cpu)
        #submitSL.write('#SBATCH -C sb\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --partition='+str(partition)+'\n')
        submitSL.write('#SBATCH --output=arrayJob_%A_%a.out'+'\n')
        submitSL.write('#SBATCH --error=arrayJob_%A_%a.err'+'\n')
        if not email == '':
            submitSL.write('#SBATCH --mail-user=' + str(email) + '\n')
            submitSL.write('#SBATCH --mail-type=ALL\n')
        #submitSL.write('\n')
        #submitSL.write('#SBATCH --hint=nomultithread\n')
        submitSL.write('\n')
        submitSL.write('######################\n')
        submitSL.write('# Begin work section #\n')
        submitSL.write('######################\n')
        submitSL.write('\n')
        submitSL.write("# Print this sub-job's task ID\n")
        submitSL.write('echo "My SLURM_ARRAY_JOB_ID: "${SLURM_ARRAY_JOB_ID}\n')
        submitSL.write('echo "My SLURM_ARRAY_TASK_ID: "${SLURM_ARRAY_TASK_ID}\n')
        submitSL.write('\n')
        submitSL.write('module load '+str(python_version)+'\n')
        submitSL.write('\n')
        submitSL.write('if [ ! -d Trial${SLURM_ARRAY_TASK_ID} ]; then\n')
        submitSL.write('    mkdir Trial${SLURM_ARRAY_TASK_ID}\n')
        submitSL.write('fi\n')
        submitSL.write('cp Run.py Trial${SLURM_ARRAY_TASK_ID}\n')
        submitSL.write('cp '+str(RunMinimisation_Script_Name)+'.py Trial${SLURM_ARRAY_TASK_ID}\n')
        submitSL.write('cd Trial${SLURM_ARRAY_TASK_ID}\n')
        submitSL.write('python Run.py\n')
        submitSL.write('cd ..\n')
        submitSL.write('mv arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out Trial${SLURM_ARRAY_TASK_ID}\n')
        submitSL.write('mv arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.err Trial${SLURM_ARRAY_TASK_ID}\n')
        submitSL.close()

def make_mass_submitSL_packets(local_path,project,no_of_trials,no_of_packets_to_make,time,nodes,ntasks_per_node,mem=None,mem_per_cpu=None,partition='large',email='',RunMinimisation_Script_Name='RunMinimisation',python_version='Python/3.6.3-gimkl-2017a'):
    # make sure that no_of_packets_to_make is a value and no_of_trials is divisible by it. 
    if not isinstance(no_of_packets_to_make,int):
        print('Error in def make_mass_submitSL_packets, in Create_submitSL_slurm_Main.py')
        print('no_of_packets_to_make needs to be give as a int')
        print('no_of_packets_to_make = '+str(no_of_packets_to_make))
        exit('Check this. The algorithm will finish here.')
    if not (float(no_of_trials)%float(no_of_packets_to_make)) == 0.0:
        print('Error in def make_mass_submitSL_packets, in Create_submitSL_slurm_Main.py')
        print('no_of_trials needs to be divisible by no_of_packets_to_make')
        print('no_of_trials = '+str(no_of_trials))
        print('no_of_packets_to_make = '+str(no_of_packets_to_make))
        exit('Check this. The algorithm will finish here.')
    number_of_divides = int(float(no_of_trials)/float(no_of_packets_to_make))
    # create name for job
    print("creating mass_submit.sl for "+str(local_path))
    name = local_path.replace('/','_')
    # writing the mass_submit.sl script
    with open(local_path+'/'+"mass_submit.sl", "w") as submitSL:
        submitSL.write('#!/bin/bash -e\n')
        submitSL.write('#SBATCH -J ' + str(name) + '\n')
        submitSL.write('#SBATCH -A ' + str(project) + '         # Project Account\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --array=1-'+str(no_of_packets_to_make)+'\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --time=' + str(time) + '     # Walltime\n')
        submitSL.write('#SBATCH --nodes=' + str(nodes) + '\n')
        submitSL.write('#SBATCH --ntasks-per-node=' + str(ntasks_per_node) + '\n')
        add_mem_to_submitSL(submitSL,mem=mem,mem_per_cpu=mem_per_cpu)
        #submitSL.write('#SBATCH -C sb\n')
        submitSL.write('\n')
        submitSL.write('#SBATCH --partition='+str(partition)+'\n')
        submitSL.write('#SBATCH --output=arrayJob_%A_%a.out'+'\n')
        submitSL.write('#SBATCH --error=arrayJob_%A_%a.err'+'\n')
        if not email == '':
            submitSL.write('#SBATCH --mail-user=' + str(email) + '\n')
            submitSL.write('#SBATCH --mail-type=ALL\n')
        #submitSL.write('\n')
        #submitSL.write('#SBATCH --hint=nomultithread\n')
        submitSL.write('\n')
        submitSL.write('######################\n')
        submitSL.write('# Begin work section #\n')
        submitSL.write('######################\n')
        submitSL.write('\n')
        submitSL.write("# Print this sub-job's task ID\n")
        submitSL.write('echo "My SLURM_ARRAY_JOB_ID: "${SLURM_ARRAY_JOB_ID}\n')
        submitSL.write('echo "My SLURM_ARRAY_TASK_ID: "${SLURM_ARRAY_TASK_ID}\n')
        submitSL.write('\n')
        submitSL.write('module load '+str(python_version)+'\n')
        submitSL.write('\n')
        submitSL.write('number_of_divides='+str(number_of_divides)+'\n')
        submitSL.write('for i in $( eval echo {1..${number_of_divides}} ); do\n')
        submitSL.write('\n')
        submitSL.write('trial_no=$(( $(( $(( ${SLURM_ARRAY_TASK_ID} - 1)) * ${number_of_divides} )) + $i ))\n')
        submitSL.write('echo Currently performing caluclation on trial: $trial_no\n')
        submitSL.write('\n')
        submitSL.write('if [ ! -d Trial${trial_no} ]; then\n')
        submitSL.write('    mkdir Trial${trial_no}\n')
        submitSL.write('fi\n')
        submitSL.write("echo '=============================================================================='\n")
        submitSL.write("echo '=============================================================================='\n")
        submitSL.write("echo 'Running Trial'${trial_no}\n")
        submitSL.write("echo '=============================================================================='\n")
        submitSL.write("echo '=============================================================================='\n")
        submitSL.write("1>&2 echo '=============================================================================='\n")
        submitSL.write("1>&2 echo '=============================================================================='\n")
        submitSL.write("1>&2 echo 'Running Trial'${trial_no}\n")
        submitSL.write("1>&2 echo '=============================================================================='\n")
        submitSL.write("1>&2 echo '=============================================================================='\n")
        submitSL.write('cp Run.py Trial${trial_no}\n')
        submitSL.write('cp '+str(RunMinimisation_Script_Name)+'.py Trial${trial_no}\n')
        submitSL.write('cd Trial${trial_no}\n')
        submitSL.write('python Run.py\n')
        submitSL.write("echo '=============================================================================='\n")
        submitSL.write("1>&2 echo '=============================================================================='\n")
        submitSL.write('cd ..\n')
        submitSL.write('cp arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out Trial${trial_no}/arrayJob_${SLURM_ARRAY_JOB_ID}_${trial_no}.out\n')
        submitSL.write('cp arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.err Trial${trial_no}/arrayJob_${SLURM_ARRAY_JOB_ID}_${trial_no}.err\n')
        submitSL.write('echo -n "" > arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out\n')
        submitSL.write('echo -n "" > arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.err\n')
        submitSL.write('\n')
        submitSL.write('done\n')
        submitSL.close()

def add_mem_to_submitSL(submitSL,mem=None,mem_per_cpu=None):
    if (mem is None) and not (mem_per_cpu is None):
        submitSL.write('#SBATCH --mem-per-cpu=' + str(mem_per_cpu) + '\n')
    elif not (mem is None) and (mem_per_cpu is None):
        submitSL.write('#SBATCH --mem=' + str(mem) + '\n')
    else:
        print('===================================')
        print('Error during making the submit.sl file.')
        if (mem is None) and (mem_per_cpu is None):
            print('You have not included any values for either "mem" or "mem-per-cpu"')
            print('Enter a value for either  "mem" or "mem-per-cpu" and rerun this program')
        elif not (mem is None) and not (mem_per_cpu is None):
            print('You have included values for both "mem" or "mem-per-cpu"')
            print('Enter a value for only either  "mem" or "mem-per-cpu" and rerun this program')
        print('This program will finish without completing.')
        print('===================================')
        exit()
