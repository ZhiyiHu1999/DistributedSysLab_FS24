# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
# This file is adapted from pretrain_llama.sh in Megatron-LM

#!/bin/bash

cd /users/zhu/DeepSpeedExamples/training/DeepSpeed-Domino

export CUDA_DEVICE_MAX_CONNECTIONS=1
 
GPUS_PER_NODE=2
# Change for multinode config
MASTER_ADDR=$(scontrol show hostnames $SLURM_JOB_NODELIST | head -n 1)  ## use hostname not ip
# MASTER_ADDR=$(getent hosts $(scontrol show hostname $SLURM_NODELIST | head -n 1) | awk '{ print $1 }')
MASTER_PORT=29500
NNODES=$SLURM_NNODES
NODE_RANK=$SLURM_PROCID
WORLD_SIZE=$(($GPUS_PER_NODE*$NNODES))
 
CHECKPOINT_PATH=checkpoint
rm -rf $CHECKPOINT_PATH/*
VOCAB_FILE="dataset/gpt2-vocab.json"
MERGE_FILE="dataset/gpt2-merges.txt"
DATA_PATH="dataset/my-gpt2_text_document"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export PYTHONPATH=$SCRIPT_DIR:$PYTHONPATH
 
DISTRIBUTED_ARGS="
    --nproc_per_node $GPUS_PER_NODE \
    --nnodes $NNODES \
    --node_rank $NODE_RANK \
    --master_addr $MASTER_ADDR \
    --master_port $MASTER_PORT
"
 
LLAMA_ARGS="
    --num-layers 2 \
    --hidden-size 256 \
    --num-attention-heads 4 \
    --seq-length 128 \
    --max-position-embeddings 128 \
    --position-embedding-type rope \
    --swiglu \
    --ffn-hidden-size 11008\
    --normalization RMSNorm \
    --layernorm-epsilon 1e-6 \
    --micro-batch-size 1 \
    --global-batch-size 2 \
    --lr 0.00015 \
    --train-iters 10 \
    --lr-decay-iters 320000 \
    --lr-decay-style cosine \
    --min-lr 1.0e-5 \
    --weight-decay 1e-2 \
    --lr-warmup-fraction .01 \
    --clip-grad 1.0 \
    --fp16 \
    --tensor-model-parallel-size $GPUS_PER_NODE \
    --seed 3407 
"

DATA_ARGS="
    --data-path $DATA_PATH \
    --vocab-file $VOCAB_FILE \
    --merge-file $MERGE_FILE \
    --split 949,50,1
"
 
OUTPUT_ARGS="
    --log-interval 1 \
    --save-interval 10000 \
    --eval-interval 1000 \
    --eval-iters 1
"
 
cmd="deepspeed --num_gpus $GPUS_PER_NODE \
    --num_nodes $NNODES \
    --hostfile='/users/zhu/DistributedSysLab_FS24/deepspeed_example/myhostfile' \
    --no_ssh --node_rank=$NODE_RANK \
    --master_addr=$MASTER_ADDR --master_port=$MASTER_PORT \
    pretrain_llama.py \
    $LLAMA_ARGS \
    $DATA_ARGS \
    $OUTPUT_ARGS 
    "
echo $cmd
eval $cmd 
