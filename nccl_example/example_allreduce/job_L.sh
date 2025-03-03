#!/bin/bash -l
#
#SBATCH --job-name="dot_visualize"
#SBATCH --time=24:00:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[44]
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=1
#SBATCH --mem=200G
#SBATCH --output=dot_visualize.%j.o
#SBATCH --error=dot_visualize.%j.e
#SBATCH --account=g34

cd ./results

srun LogGOPSim -L 0 -o 0 -G 0 -g 0 -S 20971564 -f InterNode_MicroEvents_Dependency.bin
