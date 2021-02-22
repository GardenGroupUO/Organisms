import os, sys

def make_submit_file(path_to_submit_script,LJ_gm_minTXT,cluster,trial_max):
	with open(path_to_submit_script+'/check_LJ_Sims_submit.sl','w') as submitSL:
		submitSL.write('#!/bin/bash -e\n')
		submitSL.write('#SBATCH -J check_LJ_Sims_'+str(path_to_submit_script)+'\n')
		submitSL.write('#SBATCH -A uoo02568         # Project Account\n')
		submitSL.write('\n')
		submitSL.write('#SBATCH --array=1-'+str(trial_max)+'\n')
		submitSL.write('\n')
		submitSL.write('#SBATCH --time=4:00:00     # Walltime\n')
		submitSL.write('#SBATCH --nodes=1\n')
		submitSL.write('#SBATCH --ntasks-per-node=1\n')
		submitSL.write('#SBATCH --mem=5000MB\n')
		submitSL.write('\n')
		submitSL.write('#SBATCH --partition=large\n')
		submitSL.write('#SBATCH --output=check_LJ_Sims_%A_%a.out\n')
		submitSL.write('#SBATCH --error=check_LJ_Sims_%A_%a.err\n')
		submitSL.write('#SBATCH --mail-user=geoffreywealslurmnotifications@gmail.com\n')
		submitSL.write('#SBATCH --mail-type=ALL\n')
		submitSL.write('\n')
		submitSL.write('######################\n')
		submitSL.write('# Begin work section #\n')
		submitSL.write('######################\n')
		submitSL.write('\n')
		submitSL.write("# Print this sub-job's task ID\n")
		submitSL.write('echo "My SLURM_ARRAY_JOB_ID: "${SLURM_ARRAY_JOB_ID}\n')
		submitSL.write('echo "My SLURM_ARRAY_TASK_ID: "${SLURM_ARRAY_TASK_ID}\n')
		submitSL.write('\n')
		submitSL.write('module load Python/3.6.3-gimkl-2017a\n')
		submitSL.write('module load FFmpeg/3.2.4-gimkl-2017a\n')
		submitSL.write('\n')
		submitSL.write('cp run_check_LJ_sims.py Trial${SLURM_ARRAY_TASK_ID}\n')
		submitSL.write('cd Trial${SLURM_ARRAY_TASK_ID}\n')
		submitSL.write('python run_check_LJ_sims.py\t'+str(path_to_submit_script)+'/Trial${SLURM_ARRAY_TASK_ID}\t'+str(LJ_gm_minTXT)+'\t'+str(cluster)+'\n')
		submitSL.write('rm run_check_LJ_sims.py\n')

def make_run_file(path_to_submit_script):
	with open(path_to_submit_script+'/run_check_LJ_sims.py','w') as RunPY:
		RunPY.write('import sys\n')
		RunPY.write('from check_LJ_Sims_Get_results_v3 import get_data\n')
		RunPY.write('from check_LJ_Sims_Process_results_v3 import process_data\n')
		RunPY.write('\n')
		RunPY.write('LJ_data_path = sys.argv[1]\n')
		RunPY.write('LJ_gm_minTXT = sys.argv[2]\n')
		RunPY.write('cluster_type = sys.argv[3]\n')
		RunPY.write('\n')
		RunPY.write('get_data(LJ_data_path,LJ_gm_minTXT,cluster_type)\n')
		RunPY.write('process_data(LJ_data_path,LJ_gm_minTXT,cluster_type)\n')

for root, dirs, files in os.walk(os.getcwd()): 
	if 'Trial1' in dirs:
		if 'LJ38' in root:
			cluster = 'LJ38'
		elif 'LJ75' in root:
			cluster = 'LJ75'
		elif 'LJ98' in root:
			cluster = 'LJ98'
		#import pdb; pdb.set_trace()
		LJ_gm_minTXT = os.getcwd()+'/'+'energy_data/'+str(cluster)+'_positions_1.txt'
		number_of_trials = len([a_dir for a_dir in dirs if a_dir.startswith('Trial')])
		print('making Bird poo submit script in: '+str(root))
		root_path = root
		make_submit_file(root_path,LJ_gm_minTXT,cluster,number_of_trials)
		make_run_file(root_path)
		dirs[:] = []
		files[:] = []



