#!/bin/bash -l
#
#SBATCH --job-name="nccl_example_2"
#SBATCH --time=00:10:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[41-44]
#SBATCH --ntasks-per-node=2  
#SBATCH --gpus-per-task=1    
#SBATCH --output=example_2.%j.o
#SBATCH --error=example_2.%j.e
#SBATCH --account=g34

export NCCL_ALGO=Ring

module load openmpi/4.1.1
module load cuda/11.6.2

export MPI_ROOT=/apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/openmpi-4.1.1-epxpvnwjl2smjwuwqg67h2wrmdxw6nhj
# export NCCL_ROOT=/users/zhu/nccl/build
export NCCL_ROOT=/users/zhu/nccl_npkit/nccl/build

export LD_LIBRARY_PATH=/users/zhu/nccl_npkit/nccl/build/lib:$LD_LIBRARY_PATH

nvcc -I${MPI_ROOT}/include -L${MPI_ROOT}/lib -lmpi -I${NCCL_ROOT}/include -L${NCCL_ROOT}/lib -lnccl -I/users/zhu/nccl_npkit/nccl/src/include example_2.cu -o example_2

export NPKIT_RUN_DIR="/users/zhu/nccl_example/npkit_run"

# Tag of this NPKit run.
npkit_run_tag="job_example_2"

# Path to NPKit dump directory.
npkit_dump_dir="${NPKIT_RUN_DIR}/npkit_dump/${npkit_run_tag}"

# Path to NPKit post-process directory.
npkit_trace_dir="${NPKIT_RUN_DIR}/npkit_trace/${npkit_run_tag}"

# Path to NPKit result directory.
npkit_result_dir="${NPKIT_RUN_DIR}/npkit_result/${npkit_run_tag}"

export NPKIT_DUMP_DIR="${NPKIT_RUN_DIR}/npkit_dump/${npkit_run_tag}" # Path to generate dump files

rm -rf $npkit_dump_dir
rm -rf $npkit_trace_dir
rm -rf $npkit_result_dir

mkdir -p $npkit_dump_dir
mkdir -p $npkit_trace_dir
mkdir -p $npkit_result_dir

srun ./example_2 | tee $npkit_result_dir/log.txt

python3 npkit_trace_generator.py --npkit_dump_dir=$npkit_dump_dir\
                                 --npkit_event_header_path="/users/zhu/nccl_npkit/nccl/src/include/npkit/npkit_event.h"\
                                 --output_dir=$npkit_trace_dir
