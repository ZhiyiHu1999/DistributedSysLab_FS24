#!/bin/bash -l
#
#SBATCH --job-name="nanotron_example"
#SBATCH --time=24:00:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[43-44]
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=2
#SBATCH --mem=200G
#SBATCH --output=nanotron_example.%j.o
#SBATCH --error=nanotron_example.%j.e
#SBATCH --account=g34

conda activate nanotron_env

module load openmpi/4.1.1
module load cuda/12.1.1
module load rdma-core/34.0

srun nvidia-smi -L

export NCCL_DEBUG=INFO ## For debug
export NCCL_TOPO_DUMP_FILE="./results/Topology_Intra_Node.txt" ## NCCL_PARAM(TopoDumpFileRank, "TOPO_DUMP_FILE_RANK", 0);
export NCCL_GRAPH_DUMP_FILE="./results/Graph.txt" ## NCCL_PARAM(GraphDumpFileRank, "GRAPH_DUMP_FILE_RANK", 0);

rm -rf "./results"
mkdir -p "./results"

export NSYS_REPORT_DIR="/users/zhu/DistributedSysLab_FS24/nanotron_example/results/nsys_reports"
# export NSYS_REPORT_DIR="./results/nsys_reports"
rm -rf $NSYS_REPORT_DIR
mkdir -p $NSYS_REPORT_DIR

cd /users/zhu/nanotron

export CUDA_DEVICE_MAX_CONNECTIONS=1 # Important for Nanotron
export OMP_NUM_THREADS=16  ## Unused

# EDIT if it's not 2-gpus per node
GPUS_PER_NODE=2
NNODES=$SLURM_NNODES

# define the node 0 hostname:port
MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)  ## use hostname not ip
MASTER_PORT=29500
echo "Master addr: $MASTER_ADDR:$MASTER_PORT"

LAUNCHER="python -u -m torch.distributed.run \
    --nproc_per_node $GPUS_PER_NODE \
    --nnodes $NNODES \
    --node_rank $SLURM_PROCID \
    --rdzv_id $SLURM_JOB_ID \
    --rdzv_endpoint $MASTER_ADDR:$MASTER_PORT \
    --rdzv_backend c10d \
    --max_restarts 0 \
    --role $(hostname -s|tr -dc '0-9'): "

# Check that relative paths to your `run_train.py` are correct
PROGRAM="--master_port $MASTER_PORT run_train.py --config-file /users/zhu/DistributedSysLab_FS24/nanotron_example/config_tiny_llama.yaml"

export CMD="${LAUNCHER} ${PROGRAM}"

echo $CMD

# bash -c is needed for the delayed interpolation of env vars to work
srun bash -c "$CMD"
# srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys profile --trace=nvtx,cuda  --cuda-memory-usage=false --cuda-um-cpu-page-faults=false --cuda-um-gpu-page-faults=false -s none --output=${NSYS_REPORT_DIR}/nanotron_llama_train_nsys_report_%h_%p bash -c "$CMD"

# for report_file in ${NSYS_REPORT_DIR}/*.nsys-rep; do
#   if [ -f "$report_file" ]; then
#     sqlite_file="${report_file%.nsys-rep}.sqlite"
#     # srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --sqlite "$sqlite_file" "$report_file"
#     ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --type=sqlite --ts-normalize=true --output="$sqlite_file" "$report_file"
#     echo "Exported $report_file to $sqlite_file"
#   fi
# done

conda deactivate
