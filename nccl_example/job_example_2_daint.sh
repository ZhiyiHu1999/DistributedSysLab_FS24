#!/bin/bash -l
#
#SBATCH --job-name="nccl_example_2"
#SBATCH --time=02:10:00
#SBATCH --nodes=4
#SBATCH --partition=normal
#SBATCH --ntasks-per-node=1
#SBATCH --output=example_2.%j.o
#SBATCH --error=example_2.%j.e
#SBATCH --account=g34
#SBATCH -C gpu
#SBATCH --gres=gpu:1

module load daint-gpu
module load cray-mpich
module load cudatoolkit/21.5_11.3

srun nvidia-smi -L

export NCCL_ROOT=/users/zhu/nccl_npkit/nccl/build
export LD_LIBRARY_PATH=$CRAY_MPICH_DIR/lib:$NCCL_ROOT/lib:$LD_LIBRARY_PATH
nvcc -I${CRAY_MPICH_DIR}/include -L${CRAY_MPICH_DIR}/lib -lmpich -I${NCCL_ROOT}/include -L${NCCL_ROOT}/lib -lnccl example_2.cu -o example_2

export NCCL_ALGO=Tree
export NCCL_PROTO=Simple
export NCCL_DEBUG=INFO ## For debug
export NCCL_TOPO_DUMP_FILE="Topology_Intra_Node.txt" ## NCCL_PARAM(TopoDumpFileRank, "TOPO_DUMP_FILE_RANK", 0);
export NCCL_GRAPH_DUMP_FILE="Graph.txt" ## NCCL_PARAM(GraphDumpFileRank, "GRAPH_DUMP_FILE_RANK", 0);
# export NCCL_PROXY_PROFILE="Proxy.txt"
# export NPKIT_NET_CHECK_LATENCY_THRESHOLD=1
# export NPKIT_NUM_WARMUP_OPS=1

export NPKIT_RUN_DIR="/users/zhu/DistributedSysLab_FS24/nccl_example/npkit_run"
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

# python3 merge_trace.py Ring_LL.o 