#!/bin/bash -l

#SBATCH --job-name="nccl_example_reduce"
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=1        # Do not change
#SBATCH --gpus-per-node=1          # number of gpus per node
#SBATCH --partition=normal
#SBATCH --account=a-g34
#SBATCH --mem=200G
#SBATCH --time=00:20:00            # total run time limit (HH:MM:SS)
#SBATCH --output=example_reduce.%j.o
#SBATCH --error=example_reduce.%j.e

rm -rf "./results"
mkdir -p "./results"

srun --mpi=pmi2 --environment=megatron bash -c '
    if [ "$SLURM_NODEID" -eq 0 ]; then
        export MPI_ROOT=/usr/local/mpi
        export NCCL_ROOT=/users/zhu/nccl_nvtx_v2.20.5-1/nccl/build
        export LD_LIBRARY_PATH=/users/zhu/nccl_nvtx_v2.20.5-1/nccl/build/lib:$LD_LIBRARY_PATH

        nvcc -I${MPI_ROOT}/include -L${MPI_ROOT}/lib -lmpi -I${NCCL_ROOT}/include -L${NCCL_ROOT}/lib -lnccl /users/zhu/DistributedSysLab_FS24/nccl_example/example_reduce/example_reduce.cu -o /users/zhu/DistributedSysLab_FS24/nccl_example/example_reduce/example_reduce
        echo "nvcc compile successful"
    fi
'

wait

srun --mpi=pmi2 --environment=megatron bash -c '
    export MPI_ROOT=/usr/local/mpi
    export NCCL_ROOT=/users/zhu/nccl_nvtx_v2.20.5-1/nccl/build
    export LD_LIBRARY_PATH=/users/zhu/nccl_nvtx_v2.20.5-1/nccl/build/lib:$LD_LIBRARY_PATH

    export NCCL_ALGO=Ring
    export NCCL_PROTO=LL
    # export NCCL_MIN_NCHANNELS=16
    export NCCL_MAX_NCHANNELS=1
    export NCCL_DEBUG=INFO ## For debug
    
    export NSYS_REPORT_DIR="/users/zhu/DistributedSysLab_FS24/nccl_example/example_reduce/results/nsys_reports"
    rm -rf $NSYS_REPORT_DIR
    mkdir -p $NSYS_REPORT_DIR

    nsys profile --trace=nvtx,cuda -s none --output=${NSYS_REPORT_DIR}/example_reduce_nsys_report_%h_%p /users/zhu/DistributedSysLab_FS24/nccl_example/example_reduce/example_reduce
'

# for report_file in ${NSYS_REPORT_DIR}/*.nsys-rep; do
#   if [ -f "$report_file" ]; then
#     sqlite_file="${report_file%.nsys-rep}.sqlite"
#     # srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --sqlite "$sqlite_file" "$report_file"
#     nsys export --type=sqlite --ts-normalize=true --output="$sqlite_file" "$report_file"
#     echo "Exported $report_file to $sqlite_file"
#   fi
# done

# python3 get_traced_events.py

# python3 goal2dot.py

# dot -Tsvg ./results/InGPU_MicroEvents_Dependency.dot -o ./results/InGPU_MicroEvents_Dependency.svg

# dot -Tsvg ./results/InterNode_MicroEvents_Dependency.dot -o ./results/InterNode_MicroEvents_Dependency.svg

# python3 parser_sqlite2goal.py
