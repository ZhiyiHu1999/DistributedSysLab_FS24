#!/bin/bash -l
#
#SBATCH --job-name="nccl_example_sendrecv"
#SBATCH --time=02:10:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[42,44]
#SBATCH --ntasks-per-node=2
#SBATCH --gpus-per-task=1
#SBATCH --output=example_sendrecv.%j.o
#SBATCH --error=example_sendrecv.%j.e
#SBATCH --account=g34

module load openmpi/4.1.1
# module load cuda/11.6.2
module load cuda/11.8.0
# module load cuda/12.1.1
module load rdma-core/34.0
# module load python/3.8.12

srun nvidia-smi -L

rm -rf "./results"
mkdir -p "./results"

export NCCL_ALGO=Tree
export NCCL_PROTO=LL
export NCCL_MIN_NCHANNELS=2
# export NCCL_MAX_NCHANNELS=1
export NCCL_DEBUG=INFO ## For debug
export NCCL_TOPO_DUMP_FILE="./results/Topology_Intra_Node.txt" ## NCCL_PARAM(TopoDumpFileRank, "TOPO_DUMP_FILE_RANK", 0);
export NCCL_GRAPH_DUMP_FILE="./results/Graph.txt" ## NCCL_PARAM(GraphDumpFileRank, "GRAPH_DUMP_FILE_RANK", 0);

export MPI_ROOT=/apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/openmpi-4.1.1-epxpvnwjl2smjwuwqg67h2wrmdxw6nhj

# export NCCL_ROOT=/users/zhu/nccl_nvtx_npkit/nccl/build
# export LD_LIBRARY_PATH=/users/zhu/nccl_nvtx_npkit/nccl/build/lib:$LD_LIBRARY_PATH

export NCCL_ROOT=/users/zhu/nccl_nvtx_npkit_v2.20.5-1/nccl/build
export LD_LIBRARY_PATH=/users/zhu/nccl_nvtx_npkit_v2.20.5-1/nccl/build/lib:$LD_LIBRARY_PATH

nvcc -I${MPI_ROOT}/include -L${MPI_ROOT}/lib -lmpi -I${NCCL_ROOT}/include -L${NCCL_ROOT}/lib -lnccl example_sendrecv_all2all.cu -o example_sendrecv

# export NSYS_REPORT_DIR="/users/zhu/DistributedSysLab_FS24/nccl_example/results/nsys_reports"
export NSYS_REPORT_DIR="./results/nsys_reports"
rm -rf $NSYS_REPORT_DIR
mkdir -p $NSYS_REPORT_DIR

export NPKIT_RUN_DIR="/users/zhu/DistributedSysLab_FS24/nccl_example/example_sendrecv/results/npkit_run"
# Path to NPKit dump directory.
npkit_dump_dir="${NPKIT_RUN_DIR}/npkit_dump"
# Path to NPKit post-process directory.
npkit_trace_dir="${NPKIT_RUN_DIR}/npkit_trace"
export NPKIT_DUMP_DIR="${NPKIT_RUN_DIR}/npkit_dump/" # Path to generate dump files

rm -rf $npkit_dump_dir
rm -rf $npkit_trace_dir
mkdir -p $npkit_dump_dir
mkdir -p $npkit_trace_dir

# time srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys profile --trace=nvtx,cuda -s none --output=${NSYS_REPORT_DIR}/example_sendrecv_nsys_report_%h_%p ./example_sendrecv
srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys profile --trace=nvtx,cuda -s none --output=${NSYS_REPORT_DIR}/example_sendrecv_nsys_report_%h_%p ./example_sendrecv

for report_file in ${NSYS_REPORT_DIR}/*.nsys-rep; do
  if [ -f "$report_file" ]; then
    sqlite_file="${report_file%.nsys-rep}.sqlite"
    # srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --sqlite "$sqlite_file" "$report_file"
    ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --type=sqlite --ts-normalize=true --output="$sqlite_file" "$report_file"
    echo "Exported $report_file to $sqlite_file"
  fi
done

python3 get_traced_events.py

# python3 goal_generator.py

# python3 goal2dot.py

# python3 ../trace_generator_npkit.py --npkit_dump_dir=$npkit_dump_dir\
#                                  --npkit_event_header_path="/users/zhu/nccl_nvtx_npkit/nccl/src/include/npkit/npkit_event.h"\
#                                  --output_dir=$npkit_trace_dir

# python3 ../parser_sqlite2goal.py

# python3 ../goal2dot.py