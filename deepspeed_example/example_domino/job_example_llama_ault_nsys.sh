#!/bin/bash -l
#
#SBATCH --job-name="deepspeed_example"
#SBATCH --time=24:00:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[41-42]
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=2
#SBATCH --mem=240G
#SBATCH --output=deepspeed_example.%j.o
#SBATCH --error=deepspeed_example.%j.e
#SBATCH --account=g34

conda activate deepspeed_env

module load openmpi/4.1.1
module load cuda/11.8.0
# module load rdma-core/34.0
module load gcc/10.2.0

srun nvidia-smi -L
export CUDA_LAUNCH_BLOCKING=1
export TORCH_USE_CUDA_DSA=1

export NCCL_DEBUG=INFO ## For debug
export NCCL_TOPO_DUMP_FILE="./results/Topology_Intra_Node.txt" ## NCCL_PARAM(TopoDumpFileRank, "TOPO_DUMP_FILE_RANK", 0);
export NCCL_GRAPH_DUMP_FILE="./results/Graph.txt" ## NCCL_PARAM(GraphDumpFileRank, "GRAPH_DUMP_FILE_RANK", 0);
export NCCL_IB_DISABLE=1

rm -rf "./results"
mkdir -p "./results"

export NSYS_REPORT_DIR="/users/zhu/DistributedSysLab_FS24/deepspeed_example/example_domino/results/nsys_reports"
rm -rf $NSYS_REPORT_DIR
mkdir -p $NSYS_REPORT_DIR

# export LD_LIBRARY_PATH=/apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/cuda-11.8.0-fjdnxm6yggxxp75sb62xrxxmeg4s24ml/lib64:/users/zhu/nccl_nvtx_npkit_v2.20.5-1/nccl/build/lib:$LD_LIBRARY_PATH
# export LD_PRELOAD=/users/zhu/nccl_nvtx_npkit_v2.20.5-1/nccl/build/lib/libnccl.so

# rm -rf "/users/zhu/DeepSpeedExamples/training/DeepSpeed-Domino/experiment_deepspeed"
# mkdir -p "/users/zhu/DeepSpeedExamples/training/DeepSpeed-Domino/experiment_deepspeed"
# pip install -r requirements.txt

srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys profile --trace=nvtx,cuda  --cuda-memory-usage=false --cuda-um-cpu-page-faults=false --cuda-um-gpu-page-faults=false -s none --output=${NSYS_REPORT_DIR}/nsys_report_%h_%p bash pretrain_llama_7b.sh

for report_file in ${NSYS_REPORT_DIR}/*.nsys-rep; do
  if [ -f "$report_file" ]; then
    sqlite_file="${report_file%.nsys-rep}.sqlite"
    # srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --sqlite "$sqlite_file" "$report_file"
    ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --type=sqlite --ts-normalize=true --output="$sqlite_file" "$report_file"
    echo "Exported $report_file to $sqlite_file"
  fi
done

# python3 parser_sqlite2goal.py

# python3 get_collectives_statistics.py
