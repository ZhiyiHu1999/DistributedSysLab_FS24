#!/bin/bash -l
#SBATCH --job-name="make"
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1        # Do not change
#SBATCH --partition=normal
#SBATCH --account=a-g34
#SBATCH --time=00:10:00            # total run time limit (HH:MM:SS)
#SBATCH --output=make.%j.o
#SBATCH --error=make.%j.e

srun --mpi=pmi2 --environment=megatron bash -c '
    export MPI_ROOT=/usr/local/mpi
    export NCCL_ROOT=/users/zhu/nccl_npkit_v2.20.5-1/nccl/build
    export LD_LIBRARY_PATH=/users/zhu/nccl_npkit_v2.20.5-1/nccl/build/lib:$LD_LIBRARY_PATH

    nvcc -I${MPI_ROOT}/include -L${MPI_ROOT}/lib -lmpi -I${NCCL_ROOT}/include -L${NCCL_ROOT}/lib -lnccl /users/zhu/DistributedSysLab_FS24/nccl_example/npkit_benchmark/clariden/example_allreduce.cu -o /users/zhu/DistributedSysLab_FS24/nccl_example/npkit_benchmark/clariden/example_allreduce
'