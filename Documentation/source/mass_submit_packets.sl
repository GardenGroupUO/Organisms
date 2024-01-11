#!/bin/bash -e
#SBATCH -J Data_fitness_changed_in_epoch_max_repeat_5_try2_Epoch_D_Energy_F_1rCut_SCM_alpha_3_fitness_normalised_F_SCM_0.0_1rCut_Ne38_P20_O16
#SBATCH -A uoo00084         # Project Account

#SBATCH --array=1-50

#SBATCH --time=72:00:00     # Walltime
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=300MB

#SBATCH --partition=large
#SBATCH --output=arrayJob_%A_%a.out
#SBATCH --error=arrayJob_%A_%a.err
#SBATCH --mail-user=geoffreywealslurmnotifications@gmail.com
#SBATCH --mail-type=ALL

######################
# Begin work section #
######################

# Print this sub-job's task ID
echo "My SLURM_ARRAY_JOB_ID: "${SLURM_ARRAY_JOB_ID}
echo "My SLURM_ARRAY_TASK_ID: "${SLURM_ARRAY_TASK_ID}

module load Python/3.6.3-gimkl-2017a

number_of_divides=20
for i in $( eval echo {1..${number_of_divides}} ); do

trial_no=$(( $(( $(( ${SLURM_ARRAY_TASK_ID} - 1)) * ${number_of_divides} )) + $i ))
echo Currently performing caluclation on trial: $trial_no

if [ ! -d Trial${trial_no} ]; then
    mkdir Trial${trial_no}
fi
cp Run.py Trial${trial_no}
cp RunMinimisation_LJ.py Trial${trial_no}
cd Trial${trial_no}
python Run.py
cd ..
cp arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out Trial${trial_no}/arrayJob_${SLURM_ARRAY_JOB_ID}_${trial_no}.out
cp arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.err Trial${trial_no}/arrayJob_${SLURM_ARRAY_JOB_ID}_${trial_no}.err
echo -n "" > arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out
echo -n "" > arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.err

done