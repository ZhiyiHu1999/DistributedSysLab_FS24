#!/bin/bash
conda create -n horovod_env python=3.10
conda activate horovod_env

module load openmpi/4.1.1
module load cuda/11.8.0
# module load cuda/12.1.1
# module load CMake/3.13.1  ## Don't use this
module load cmake/3.21.2
module load gcc/10.2.0

conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

pip install tensorflow[and-cuda]
conda install mpi4py
pip install setuptools==58.2.0
pip install jupyterlab
pip install jupyterlab-nvdashboard

export CUDA_HOME=/apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/cuda-11.8.0-fjdnxm6yggxxp75sb62xrxxmeg4s24ml
# export CUDA_HOME=/apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/cuda-12.1.1-zbdbt4aikrp6sdems6n3t5wvqxm3tza5
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

export HOROVOD_CUDA_HOME=$CUDA_HOME
# export HOROVOD_NCCL_HOME=/users/zhu/nccl_nvtx/nccl/build
export HOROVOD_NCCL_INCLUDE=/users/zhu/nccl_nvtx/nccl/build/include
export HOROVOD_NCCL_LIB=/users/zhu/nccl_nvtx/nccl/build/lib
export HOROVOD_GPU_OPERATIONS=NCCL
export HOROVOD_WITHOUT_MXNET=1

# pip install horovod > install_log.txt 2>&1
pip install --no-cache-dir git+https://github.com/thomas-bouvier/horovod.git@compile-cpp17 > install_log.txt 2>&1

conda deactivate
