#!/bin/bash -l
#SBATCH --job-name="build"
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=normal
#SBATCH --mem=200G
#SBTACH --account=a-g34
#SBATCH --time=02:20:00
#SBATCH --output=build.%j.o
#SBATCH --error=build.%j.e

bash image_build.sh
