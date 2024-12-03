#!/bin/bash

cd /users/zhu/DeepSpeedExamples/training/cifar

MASTER_ADDR=$(getent hosts $(scontrol show hostname $SLURM_NODELIST | head -n 1) | awk '{ print $1 }')
MASTER_PORT=29500
NODE_RANK=$SLURM_NODEID

echo "Master Address: $MASTER_ADDR"
echo "Master Port: $MASTER_PORT"
echo "Node Rank: $NODE_RANK"

# Size of expert parallel world (should be less than total world size)
EP_SIZE=2
# Number of total experts
EXPERTS=2

deepspeed --hostfile='/users/zhu/DistributedSysLab_FS24/deepspeed_example/myhostfile' \
    --no_ssh --node_rank=$NODE_RANK \
    --master_addr=$MASTER_ADDR --master_port=$MASTER_PORT \
    cifar10_deepspeed.py --epochs 1 \
						 --log-interval 100 \
						 --deepspeed \
						 --moe \
						 --ep-world-size ${EP_SIZE} \
						 --num-experts ${EXPERTS} \
						 --top-k 1 \
						 --noisy-gate-policy 'RSample' \
						 --moe-param-group

# # Number of nodes
# NUM_NODES=1
# # Number of GPUs per node
# NUM_GPUS=2
# # Size of expert parallel world (should be less than total world size)
# EP_SIZE=2
# # Number of total experts
# EXPERTS=2

# deepspeed --num_nodes=${NUM_NODES}\
#           --num_gpus=${NUM_GPUS} \
#           --bind_cores_to_rank \
#         cifar10_deepspeed.py \
# 	--log-interval 100 \
# 	--deepspeed \
# 	--moe \
# 	--ep-world-size ${EP_SIZE} \
# 	--num-experts ${EXPERTS} \
# 	--top-k 1 \
# 	--noisy-gate-policy 'RSample' \
# 	--moe-param-group
