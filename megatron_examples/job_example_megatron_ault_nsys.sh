#!/bin/bash -l
#
#SBATCH --job-name="megatron_example_gpt"
#SBATCH --time=24:00:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[43-44]
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=1
#SBATCH --output=megatron_example_gpt.%j.o
#SBATCH --error=megatron_example_gpt.%j.e
#SBATCH --account=g34

module load openmpi/4.1.1
# module load cuda/11.6.2
module load cuda/11.8.0
# module load cuda/12.1.1
module load rdma-core/34.0
module load sarus/1.6.0

srun nvidia-smi -L

PYTORCH_IMAGE=nvcr.io/nvidia/pytorch:22.08-py3
CHECKPOINT_PATH=/users/zhu/Megatron_examples_checkpoints/GPT #<Specify path>
TENSORBOARD_LOGS_PATH=/users/zhu/Megatron_examples_checkpoints/GPT/tensorboard_logs #<Specify path>
VOCAB_FILE=/users/zhu/Megatron_examples_checkpoints/GPT/gpt2-vocab.json #<Specify path to file>/gpt2-vocab.json
MERGE_FILE=/users/zhu/Megatron_examples_checkpoints/GPT/gpt2-merges.txt #<Specify path to file>/gpt2-merges.txt
DATA_PATH=/users/zhu/Megatron_examples_data/my-gpt2_text_document #<Specify path and file prefix>_text_document

# sarus pull nvcr.io/nvidia/pytorch:22.08-py3

# srun sarus run --mount=type=bind,source=/users/zhu/Megatron-LM,target=/workspace/Megatron-LM \
#                --mount=type=bind,source=/users/zhu/Megatron_examples_data,target=/workspace/dataset \
#                --mount=type=bind,source=/users/zhu/Megatron_examples_checkpoints/GPT,target=/workspace/checkpoints \
#                nvcr.io/nvidia/pytorch:22.08-py3 \
#                bash -c "bash /workspace/Megatron-LM/examples/gpt3/train_gpt3_175b_distributed.sh"

srun sarus run \
  --mount=type=bind,source=/users/zhu/Megatron-LM,target=/workspace/Megatron-LM \
  --mount=type=bind,source=/users/zhu/Megatron_examples_data,target=/workspace/dataset \
  --mount=type=bind,source=/users/zhu/Megatron_examples_checkpoints/GPT,target=/workspace/checkpoints \
  --mount=type=bind,source=/users/zhu/Megatron_examples_checkpoints/GPT/tensorboard_logs,target=/workspace/tensorboard_logs \
  $PYTORCH_IMAGE \
  bash -c "bash /workspace/Megatron-LM/train_gpt3_175b_distributed.sh $CHECKPOINT_PATH $TENSORBOARD_LOGS_PATH $VOCAB_FILE $MERGE_FILE $DATA_PATH"

# rm -rf "./results"
# mkdir -p "./results"

# # export NCCL_ALGO=Tree
# # export NCCL_PROTO=Simple
# # # export NCCL_MIN_NCHANNELS=4
# # export NCCL_MAX_NCHANNELS=1
# # export NCCL_DEBUG=INFO ## For debug
# # export NCCL_TOPO_DUMP_FILE="./results/Topology_Intra_Node.txt" ## NCCL_PARAM(TopoDumpFileRank, "TOPO_DUMP_FILE_RANK", 0);
# # export NCCL_GRAPH_DUMP_FILE="./results/Graph.txt" ## NCCL_PARAM(GraphDumpFileRank, "GRAPH_DUMP_FILE_RANK", 0);

# # export MPI_ROOT=/apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/openmpi-4.1.1-epxpvnwjl2smjwuwqg67h2wrmdxw6nhj

# # export NCCL_ROOT=/users/zhu/nccl_nvtx/nccl/build
# # export LD_LIBRARY_PATH=/users/zhu/nccl_nvtx/nccl/build/lib:$LD_LIBRARY_PATH

# # nvcc -I${MPI_ROOT}/include -L${MPI_ROOT}/lib -lmpi -I${NCCL_ROOT}/include -L${NCCL_ROOT}/lib -lnccl example_2.cu -o example_2

# # export NSYS_REPORT_DIR="/users/zhu/DistributedSysLab_FS24/nccl_example/results/nsys_reports"
# export NSYS_REPORT_DIR="./results/nsys_reports"
# rm -rf $NSYS_REPORT_DIR
# mkdir -p $NSYS_REPORT_DIR

# # time srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys profile --trace=nvtx,cuda -s none --output=${NSYS_REPORT_DIR}/example_2_nsys_report_%h_%p ./example_2
# srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys profile --trace=nvtx,cuda -s none --output=${NSYS_REPORT_DIR}/example_2_nsys_report_%h_%p ./example_2

# for report_file in ${NSYS_REPORT_DIR}/*.nsys-rep; do
#   if [ -f "$report_file" ]; then
#     sqlite_file="${report_file%.nsys-rep}.sqlite"
#     # srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --sqlite "$sqlite_file" "$report_file"
#     ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --type=sqlite --ts-normalize=true --output="$sqlite_file" "$report_file"
#     echo "Exported $report_file to $sqlite_file"
#   fi
# done

# python3 parser_sqlite2goal.py

# python3 goal2dot.py
