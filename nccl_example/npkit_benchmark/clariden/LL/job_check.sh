#!/bin/bash -l
#SBATCH --job-name="check"
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1        # Do not change
#SBATCH --gpus-per-node=1          # number of gpus per node
#SBATCH --partition=normal
#SBATCH --account=a-g34
#SBATCH --mem=200G
#SBATCH --time=02:20:00            # total run time limit (HH:MM:SS)
#SBATCH --output=check.%j.o
#SBATCH --error=check.%j.e

srun nvidia-smi

