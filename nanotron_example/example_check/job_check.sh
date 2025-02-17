#!/bin/bash -l
#
#SBATCH --job-name="check"
#SBATCH --time=02:10:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[43]
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=1
#SBATCH --output=example_check.%j.o
#SBATCH --error=example_check.%j.e
#SBATCH --account=g34

module load openmpi/4.1.1
# module load cuda/11.6.2
module load cuda/11.8.0
# module load cuda/12.1.1
module load rdma-core/34.0

# srun docker --version
# srun nvidia-smi
# srun ip addr
srun netstat -tunlp
