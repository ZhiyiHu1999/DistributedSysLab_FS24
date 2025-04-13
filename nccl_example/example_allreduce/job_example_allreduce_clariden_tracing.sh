#!/bin/bash -l
#
#SBATCH --job-name="nccl_example_allreduce"
#SBATCH --time=02:10:00
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=1        # Do not change
#SBATCH --gpus-per-node=1          # number of gpus per node
#SBATCH --partition=normal
#SBATCH --mem=200G
#SBATCH --output=nccl_example.%j.o
#SBATCH --error=nccl_example.%j.e
#SBATCH --account=a-g34

rm -rf "./results"
mkdir -p "./results"

srun --mpi=pmi2 --environment=megatron bash -c '
    if [ "$SLURM_NODEID" -eq 0 ]; then
        export MPI_ROOT=/usr/local/mpi
        export NCCL_ROOT=/users/zhu/nccl_nvtx_v2.20.5-1/nccl/build
        export LD_LIBRARY_PATH=/users/zhu/nccl_nvtx_v2.20.5-1/nccl/build/lib:$LD_LIBRARY_PATH

        nvcc -I${MPI_ROOT}/include -L${MPI_ROOT}/lib -lmpi -I${NCCL_ROOT}/include -L${NCCL_ROOT}/lib -lnccl /users/zhu/DistributedSysLab_FS24/nccl_example/example_allreduce/example_allreduce.cu -o /users/zhu/DistributedSysLab_FS24/nccl_example/example_allreduce/example_allreduce
        echo "nvcc compile successful"
    fi
'

wait

export NSYS_REPORT_DIR="/users/zhu/DistributedSysLab_FS24/nccl_example/example_allreduce/results/nsys_reports"
rm -rf $NSYS_REPORT_DIR
mkdir -p $NSYS_REPORT_DIR

srun --mpi=pmi2 --environment=megatron bash -c "
    export NCCL_ALGO=Ring
    export NCCL_PROTO=Simple
    # export NCCL_MIN_NCHANNELS=2
    export NCCL_MAX_NCHANNELS=1
    export NCCL_DEBUG=INFO ## For debug

    # export NCCL_TOPO_DUMP_FILE="./results/Topology_Intra_Node.txt" ## NCCL_PARAM(TopoDumpFileRank, "TOPO_DUMP_FILE_RANK", 0);
    # export NCCL_GRAPH_DUMP_FILE="./results/Graph.txt" ## NCCL_PARAM(GraphDumpFileRank, "GRAPH_DUMP_FILE_RANK", 0);

    export MPI_ROOT=/usr/local/mpi
    export NCCL_ROOT=/users/zhu/nccl_nvtx_v2.20.5-1/nccl/build
    export LD_LIBRARY_PATH=/users/zhu/nccl_nvtx_v2.20.5-1/nccl/build/lib:$LD_LIBRARY_PATH

    export NSYS_REPORT_DIR="/users/zhu/DistributedSysLab_FS24/nccl_example/example_allreduce/results/nsys_reports"

    nsys profile --trace=nvtx,cuda -s none --output=${NSYS_REPORT_DIR}/example_allreduce_nsys_report_%h_%p /users/zhu/DistributedSysLab_FS24/nccl_example/example_allreduce/example_allreduce
"


# export NSYS_REPORT_DIR="./results/nsys_reports"

# for report_file in ${NSYS_REPORT_DIR}/*.nsys-rep; do
#   if [ -f "$report_file" ]; then
#     sqlite_file="${report_file%.nsys-rep}.sqlite"
#     # srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --sqlite "$sqlite_file" "$report_file"
#     ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --type=sqlite --ts-normalize=true --output="$sqlite_file" "$report_file"
#     echo "Exported $report_file to $sqlite_file"
#   fi
# done

# python3 get_traced_events.py

# python3 goal2dot.py

# dot -Tsvg ./results/Events_Dependency.dot -o ./results/Events_Dependency.svg

# dot -Tsvg ./results/InGPU_MicroEvents_Dependency.dot -o ./results/InGPU_MicroEvents_Dependency.svg

# dot -Tsvg ./results/InterNode_MicroEvents_Dependency.dot -o ./results/InterNode_MicroEvents_Dependency.svg

