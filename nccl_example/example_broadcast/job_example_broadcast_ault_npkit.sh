#!/bin/bash -l
#
#SBATCH --job-name="nccl_example_broadcast"
#SBATCH --time=02:10:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[42-43]
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=1
#SBATCH --output=example_broadcast.%j.o
#SBATCH --error=example_broadcast.%j.e
#SBATCH --account=g34

module load openmpi/4.1.1
# module load cuda/11.6.2
module load cuda/11.8.0
# module load cuda/12.1.1
# module load rdma-core/34.0

srun nvidia-smi -L

rm -rf "./results"
mkdir -p "./results"

export NCCL_ALGO=Ring
export NCCL_PROTO=Simple
# export NCCL_MIN_NCHANNELS=4
export NCCL_MAX_NCHANNELS=1
export NCCL_DEBUG=INFO ## For debug
export NCCL_TOPO_DUMP_FILE="./results/Topology_Intra_Node.txt" ## NCCL_PARAM(TopoDumpFileRank, "TOPO_DUMP_FILE_RANK", 0);
export NCCL_GRAPH_DUMP_FILE="./results/Graph.txt" ## NCCL_PARAM(GraphDumpFileRank, "GRAPH_DUMP_FILE_RANK", 0);

export MPI_ROOT=/apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/openmpi-4.1.1-epxpvnwjl2smjwuwqg67h2wrmdxw6nhj

# export NCCL_ROOT=/users/zhu/nccl/build
export NCCL_ROOT=/users/zhu/nccl_npkit_dependency/nccl/build
# export NCCL_ROOT=/users/zhu/nccl_npkit/nccl/build
# export NCCL_ROOT=/users/zhu/nccl_npkit_2.22.3-1/nccl/build

export LD_LIBRARY_PATH=/users/zhu/nccl_npkit_dependency/nccl/build/lib:$LD_LIBRARY_PATH
# export LD_LIBRARY_PATH=/users/zhu/nccl_npkit/nccl/build/lib:$LD_LIBRARY_PATH
# export LD_LIBRARY_PATH=/users/zhu/nccl/build/lib:$LD_LIBRARY_PATH

nvcc -I${MPI_ROOT}/include -L${MPI_ROOT}/lib -lmpi -I${NCCL_ROOT}/include -L${NCCL_ROOT}/lib -lnccl example_broadcast.cu -o example_broadcast

export NPKIT_RUN_DIR="/users/zhu/DistributedSysLab_FS24/nccl_example/example_broadcast/results/npkit_run"

# Tag of this NPKit run.
npkit_run_tag="job_example_broadcast"

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

srun ./example_broadcast | tee $npkit_result_dir/log.txt

# python3 ../npkit_dependency_trace_generator.py --npkit_dump_dir=$npkit_dump_dir\
#                                  --npkit_event_header_path="/users/zhu/nccl_npkit_dependency/nccl/src/include/npkit/npkit_event.h"\
#                                  --output_dir=$npkit_trace_dir

python3 ../trace_generator_npkit.py --npkit_dump_dir=$npkit_dump_dir\
                                 --npkit_event_header_path="/users/zhu/nccl_npkit_dependency/nccl/src/include/npkit/npkit_event.h"\
                                 --output_dir=$npkit_trace_dir