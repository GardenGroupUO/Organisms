#!/bin/bash -e
#SBATCH -J Cu_Cu37_PopSize30_OffPerGenEquals24
#SBATCH -A uoo00084         # Project Account

#SBATCH --array=1-50

#SBATCH --time=8:00:00     # Walltime
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=1G

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

module load Python/2.7.14-gimkl-2017a

mkdir Trial${SLURM_ARRAY_TASK_ID}
cp Run.py Trial${SLURM_ARRAY_TASK_ID}
cp RunMinimisation.py Trial${SLURM_ARRAY_TASK_ID}
cd Trial${SLURM_ARRAY_TASK_ID}
python Run.py
cd ..
mv arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out Trial${SLURM_ARRAY_TASK_ID}
mv arrayJob_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.err Trial${SLURM_ARRAY_TASK_ID}
