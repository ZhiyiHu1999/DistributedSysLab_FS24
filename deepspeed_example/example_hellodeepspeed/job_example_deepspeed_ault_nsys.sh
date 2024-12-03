#!/bin/bash -l
#
#SBATCH --job-name="deepspeed_example"
#SBATCH --time=24:00:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[43-44]
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=1
#SBATCH --mem=200G
#SBATCH --output=deepspeed_example.%j.o
#SBATCH --error=deepspeed_example.%j.e
#SBATCH --account=g34

module load openmpi/4.1.1
module load cuda/11.8.0
module load rdma-core/34.0
module load gcc/10.2.0

srun nvidia-smi -L

export NCCL_DEBUG=INFO ## For debug
export NCCL_TOPO_DUMP_FILE="./results/Topology_Intra_Node.txt" ## NCCL_PARAM(TopoDumpFileRank, "TOPO_DUMP_FILE_RANK", 0);
export NCCL_GRAPH_DUMP_FILE="./results/Graph.txt" ## NCCL_PARAM(GraphDumpFileRank, "GRAPH_DUMP_FILE_RANK", 0);

rm -rf "./results"
mkdir -p "./results"

export NSYS_REPORT_DIR="/users/zhu/DistributedSysLab_FS24/deepspeed_example/example_hellodeepspeed/results/nsys_reports"
# export NSYS_REPORT_DIR="./results/nsys_reports"
rm -rf $NSYS_REPORT_DIR
mkdir -p $NSYS_REPORT_DIR

export LD_LIBRARY_PATH=/apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/cuda-11.8.0-fjdnxm6yggxxp75sb62xrxxmeg4s24ml/lib64:/users/zhu/nccl_nvtx_npkit/nccl/build/lib:$LD_LIBRARY_PATH
export LD_PRELOAD=/users/zhu/nccl-tracer/src/libncclprof.so
export NCCL_TRACE_PREFIX=/users/zhu/DistributedSysLab_FS24/deepspeed_example/example_hellodeepspeed/results/result

# cd /users/zhu/DeepSpeedExamples/training/HelloDeepSpeed
# rm -rf "./experiments"
# mkdir -p "./experiments"
rm -rf "/users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed"
mkdir -p "/users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed"
# pip install -r requirements.txt
# srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys profile --trace=nvtx,cuda -s none --output=${NSYS_REPORT_DIR}/HelloDeepSpeed_train_bert_nsys_report_%h_%p deepspeed train_bert.py --checkpoint_dir '/users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiments'
# srun deepspeed train_bert.py --deepspeed --num_gpus=2 --checkpoint_dir ./experiments

srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys profile --trace=nvtx,cuda  --cuda-memory-usage=false --cuda-um-cpu-page-faults=false --cuda-um-gpu-page-faults=false -s none --output=${NSYS_REPORT_DIR}/HelloDeepSpeed_train_bert_nsys_report_%h_%p bash run_ds.sh

# srun deepspeed --hostfile='/users/zhu/DistributedSysLab_FS24/deepspeed_example/myhostfile' \
#     --no_ssh --node_rank=$NODE_RANK \
#     --master_addr=$MASTER_ADDR --master_port=$MASTER_PORT \
#     train_bert_ds.py --checkpoint_dir '/users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed'

for report_file in ${NSYS_REPORT_DIR}/*.nsys-rep; do
  if [ -f "$report_file" ]; then
    sqlite_file="${report_file%.nsys-rep}.sqlite"
    # srun ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --sqlite "$sqlite_file" "$report_file"
    ~/opt/nvidia/nsight-systems-cli/2024.5.1/bin/nsys export --type=sqlite --ts-normalize=true --output="$sqlite_file" "$report_file"
    echo "Exported $report_file to $sqlite_file"
  fi
done

python3 parser_sqlite2goal.py

python3 get_collectives_statistics.py