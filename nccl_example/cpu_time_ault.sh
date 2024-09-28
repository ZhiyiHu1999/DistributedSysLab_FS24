#!/bin/bash -l
#
#SBATCH --job-name="cpu_time"
#SBATCH --time=02:10:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[42-44]
#SBATCH --ntasks-per-node=3
#SBATCH --gpus-per-task=1
#SBATCH --output=cpu_time.%j.o
#SBATCH --error=cpu_time.%j.e
#SBATCH --account=g34

srun bash -c 'echo "Hostname: $(hostname), CPU: $(taskset -c -p $$ | awk -F: "{print \$2}"), UNIX Timestamp: $(date +%s)"'
