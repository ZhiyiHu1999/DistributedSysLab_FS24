#!/bin/bash -l
#
#SBATCH --job-name="deepspeed_example"
#SBATCH --time=24:00:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[43-44]
#SBATCH --ntasks-per-node=2
#SBATCH --gpus-per-task=1
#SBATCH --mem=200G
#SBATCH --output=deepspeed_example.%j.o
#SBATCH --error=deepspeed_example.%j.e
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

# export NSYS_REPORT_DIR="/users/zhu/DistributedSysLab_FS24/deepspeed_example/results/nsys_reports"
# # export NSYS_REPORT_DIR="./results/nsys_reports"
# rm -rf $NSYS_REPORT_DIR
# mkdir -p $NSYS_REPORT_DIR

cd /users/zhu/nanotron
export CUDA_DEVICE_MAX_CONNECTIONS=1
# export MASTER_ADDR=148.187.105.53
# export MASTER_PORT=29400
export WORLD_SIZE=4
srun torchrun --nproc_per_node=2 --rdzv_endpoint=localhost:29400 run_train.py --config-file /users/zhu/DistributedSysLab_FS24/nanotron_example/config_tiny_llama.yaml

# srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys profile --trace=nvtx,cuda  --cuda-memory-usage=false --cuda-um-cpu-page-faults=false --cuda-um-gpu-page-faults=false -s none --output=${NSYS_REPORT_DIR}/HelloDeepSpeed_train_bert_nsys_report_%h_%p bash run_ds.sh

# for report_file in ${NSYS_REPORT_DIR}/*.nsys-rep; do
#   if [ -f "$report_file" ]; then
#     sqlite_file="${report_file%.nsys-rep}.sqlite"
#     # srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --sqlite "$sqlite_file" "$report_file"
#     ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --type=sqlite --ts-normalize=true --output="$sqlite_file" "$report_file"
#     echo "Exported $report_file to $sqlite_file"
#   fi
# done

conda deactivate
