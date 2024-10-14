#!/bin/bash

cd /users/zhu/DeepSpeedExamples/training/HelloDeepSpeed

MASTER_ADDR=$(getent hosts $(scontrol show hostname $SLURM_NODELIST | head -n 1) | awk '{ print $1 }')
MASTER_PORT=29500
NODE_RANK=$SLURM_NODEID

echo "Master Address: $MASTER_ADDR"
echo "Master Port: $MASTER_PORT"
echo "Node Rank: $NODE_RANK"

deepspeed --hostfile='/users/zhu/DistributedSysLab_FS24/deepspeed_example/myhostfile' \
    --no_ssh --node_rank=$NODE_RANK \
    --master_addr=$MASTER_ADDR --master_port=$MASTER_PORT \
    train_bert_ds.py --checkpoint_dir '/users/zhu/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed'
    