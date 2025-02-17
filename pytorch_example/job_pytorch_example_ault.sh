#!/bin/bash -l
#
#SBATCH --job-name="pytorch_example_mnist"
#SBATCH --time=02:10:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[42-43]
#SBATCH --ntasks-per-node=2
#SBATCH --gpus-per-task=1    
#SBATCH --output=pytorch_example_mnist.%j.o
#SBATCH --error=pytorch_example_mnist.%j.e
#SBATCH --account=g34

module load python/3.8.12
module load openmpi/4.1.1
# module load cuda/11.6.2
module load cuda/11.8.0
# module load cuda/12.1.1

srun nvidia-smi -L

export NCCL_ALGO=Ring
export NCCL_PROTO=Simple
export NCCL_DEBUG=INFO ## For debug
export NCCL_TOPO_DUMP_FILE="Topology_Intra_Node.txt" ## NCCL_PARAM(TopoDumpFileRank, "TOPO_DUMP_FILE_RANK", 0);
export NCCL_GRAPH_DUMP_FILE="Graph.txt" ## NCCL_PARAM(GraphDumpFileRank, "GRAPH_DUMP_FILE_RANK", 0);

# export LD_DEBUG=libs

export MPI_ROOT=/apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/openmpi-4.1.1-epxpvnwjl2smjwuwqg67h2wrmdxw6nhj
# export USE_SYSTEM_NCCL=1
# export NCCL_ROOT=/users/zhu/nccl_npkit/nccl/build
# export NCCL_ROOT=/users/zhu/nccl_npkit_2.22.3-1/nccl/build
# export LD_LIBRARY_PATH=/users/zhu/nccl_npkit/nccl/build/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/users/zhu/pytorch/build/lib:$LD_LIBRARY_PATH
export PATH=/users/zhu/pytorch/build/bin:$PATH
# export LD_PRELOAD=/users/zhu/nccl_npkit/nccl/build/lib/libnccl.so:$LD_PRELOAD

# nvcc -I${MPI_ROOT}/include -L${MPI_ROOT}/lib -lmpi -I${NCCL_ROOT}/include -L${NCCL_ROOT}/lib -lnccl -I/users/zhu/nccl_npkit/nccl/src/include example_2.cu -o example_2

export NPKIT_RUN_DIR="/users/zhu/DistributedSysLab_FS24/pytorch_examples/npkit_run"
npkit_run_tag="mnist"  # Tag of this NPKit run.
npkit_dump_dir="${NPKIT_RUN_DIR}/npkit_dump/${npkit_run_tag}"  # Path to NPKit dump directory.
npkit_trace_dir="${NPKIT_RUN_DIR}/npkit_trace/${npkit_run_tag}"  # Path to NPKit post-process directory.
npkit_result_dir="${NPKIT_RUN_DIR}/npkit_result/${npkit_run_tag}"  # Path to NPKit result directory.
export NPKIT_DUMP_DIR="${NPKIT_RUN_DIR}/npkit_dump/${npkit_run_tag}" # Path to generate dump files

rm -rf $npkit_dump_dir
rm -rf $npkit_trace_dir
rm -rf $npkit_result_dir

# mkdir -p $npkit_dump_dir
# mkdir -p $npkit_trace_dir
# mkdir -p $npkit_result_dir

export NSYS_REPORT_DIR="/users/zhu/DistributedSysLab_FS24/pytorch_examples/nsys_reports"
rm -rf $NSYS_REPORT_DIR
mkdir -p $NSYS_REPORT_DIR

# srun python3 ~/examples/$npkit_run_tag/main.py --no-mps | tee $npkit_result_dir/log.txt
# srun python3 ~/examples/$npkit_run_tag/main.py | tee $npkit_result_dir/log.txt
srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys profile --trace=osrt,nvtx,cuda --output=${NSYS_REPORT_DIR}/pytorch_example_mnist_nsys_report_%h_%p python3 ~/examples/$npkit_run_tag/main.py

# python3 npkit_trace_generator.py --npkit_dump_dir=$npkit_dump_dir\
#                                  --npkit_event_header_path="/users/zhu/nccl_npkit/nccl/src/include/npkit/npkit_event.h"\
#                                  --output_dir=$npkit_trace_dir
# python3 parser_json2goal_Ring.py
# python3 goal2dot.py