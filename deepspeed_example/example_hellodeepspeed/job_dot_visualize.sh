#!/bin/bash -l
#
#SBATCH --job-name="dot_visualize"
#SBATCH --time=24:00:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[43]
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=1
#SBATCH --mem=200G
#SBATCH --output=dot_visualize.%j.o
#SBATCH --error=dot_visualize.%j.e
#SBATCH --account=g34

srun dot -Tsvg ./results/Events_Dependency.dot -o ./results/Events_Dependency.svg

srun dot -Tsvg ./results/InGPU_MicroEvents_Dependency.dot -o ./results/InGPU_MicroEvents_Dependency.svg

srun dot -Tsvg ./results/InterNode_MicroEvents_Dependency.dot -o ./results/InterNode_MicroEvents_Dependency.svg
