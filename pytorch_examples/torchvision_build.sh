#!/bin/bash -l
#
#SBATCH --job-name="pytorch_system_nccl_build"
#SBATCH --time=24:00:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[44]
#SBATCH --ntasks-per-node=1
#SBATCH --output=pytorch_system_nccl_build.%j.o
#SBATCH --error=pytorch_system_nccl_build.%j.e
#SBATCH --account=g34

cd ~/pytorch
# git checkout main
git checkout v2.4.1

module load python/3.8.12
module load cmake/3.21.3
module load gcc/10.2.0
module load ninja/1.10.2
module load cuda/11.8.0

export USE_ROCM=0
export USE_XPU=0

export USE_SYSTEM_NCCL=1
export NCCL_ROOT=/users/zhu/nccl_npkit/nccl/build

export CMAKE_PREFIX_PATH=/users/zhu/.local
# export CMAKE_PREFIX_PATH=${NCCL_ROOT}:${CMAKE_PREFIX_PATH}
export LD_LIBRARY_PATH=${NCCL_ROOT}/lib:${LD_LIBRARY_PATH}

# pip install --user -r requirements.txt
# # pip install -r requirements.txt
# python3 setup.py clean
# python3 setup.py develop
# python3 setup.py install --user
python3 setup.py install --prefix=/users/zhu/.local

# pip install --user torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# pip install --user --pre torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu118