#!/bin/bash

PROJECT_NAME=EE-TUNE
GROUP_NAME=llama-2-7B-8-EXIT-pt
MODEL_SIZE=7

CURRENT_TIME=`date "+%m%d-%H%M"`

MASTER_NAME=${CURRENT_TIME}

export CUDA_DEVICE_MAX_CONNECTIONS=1
export OMP_NUM_THREADS=1

# Checkpoint configuration
BASE_PATH=/workspace
LOAD_PATH=${BASE_PATH}/model_ckpts/llama2-7b_hf-to-meg_ee_tp1_pp2 # your checkpoint path
TOKENIZER_PATH=${BASE_PATH}/tokenizers/Llama2Tokenizer/tokenizer.model # your tokenizer path
CHECKPOINT_PATH=${BASE_PATH}/model_ckpts/llama2-7b_hf-to-meg_ee_ft_tp1_pp2 # checkpoint save path

# Data configuration
DATA_HOME=${BASE_PATH}/data
DATASET_ARXIV=${DATA_HOME}/redpajama-arxiv/all
DATASET_BOOKS=${DATA_HOME}/redpajama-book/all
DATASET_C4=${DATA_HOME}/redpajama-c4/all
DATASET_CC=${DATA_HOME}/redpajama-cc/all
DATASET_STACKEXCHANGE=${DATA_HOME}/redpajama-pile-stackexchange/all
DATASET_CODE=${DATA_HOME}/redpajama-stack-code/all
DATASET_WIKIPEDIA=${DATA_HOME}/redpajama-wiki/all
# DATASET_PILE_EUROPARL=${DATA_HOME}/the-pile-europarl/all
# DATASET_PILE_FREELAW=${DATA_HOME}/the-pile-freelaw/all
# DATASET_PILE_HACKERNEWS=${DATA_HOME}/the-pile-hackernews/all
# DATASET_PILE_NIH=${DATA_HOME}/the-pile-nih/all
# DATASET_PILE_PHILPAPER=${DATA_HOME}/the-pile-philpaper/all
# DATASET_PILE_PMA=${DATA_HOME}/the-pile-pubmed-abstract/all
# DATASET_PILE_PMC=${DATA_HOME}/the-pile-pubmed-central/all
# DATASET_PILE_USPTO=${DATA_HOME}/the-pile-uspto/all

DATASET_PILE_EUROPARL=${DATA_HOME}/the-pile-europarl/the-pile-europarl-meg-llama_text_document
DATASET_PILE_FREELAW=${DATA_HOME}/the-pile-freelaw/the-pile-freelaw-meg-llama_text_document
DATASET_PILE_HACKERNEWS=${DATA_HOME}/the-pile-hackernews/the-pile-hackernews-meg-llama_text_document
DATASET_PILE_NIH=${DATA_HOME}/the-pile-nih/the-pile-nih-meg-llama_text_document
DATASET_PILE_PHILPAPER=${DATA_HOME}/the-pile-philpaper/the-pile-philpaper-meg-llama_text_document
DATASET_PILE_PMA=${DATA_HOME}/the-pile-pubmed-abstract/the-pile-pubmed-abstract-meg-llama_text_document
DATASET_PILE_PMC=${DATA_HOME}/the-pile-pubmed-central/the-pile-pubmed-central-meg-llama_text_document
DATASET_PILE_USPTO=${DATA_HOME}/the-pile-uspto/the-pile-uspto-meg-llama_text_document

# DATA_PATH="\
#     0.0362 ${DATASET_ARXIV} \
#     0.0657 ${DATASET_BOOKS} \
#     0.2264 ${DATASET_C4} \
#     0.4491 ${DATASET_CC} \
#     0.0246 ${DATASET_STACKEXCHANGE} \
#     0.0810 ${DATASET_CODE} \
#     0.0548 ${DATASET_WIKIPEDIA} \
#     0.0010 ${DATASET_PILE_EUROPARL} \
#     0.0162 ${DATASET_PILE_FREELAW} \
#     0.0006 ${DATASET_PILE_HACKERNEWS} \
#     0.0005 ${DATASET_PILE_NIH} \
#     0.0006 ${DATASET_PILE_PHILPAPER} \
#     0.0065 ${DATASET_PILE_PMA} \
#     0.0318 ${DATASET_PILE_PMC} \
#     0.0050 ${DATASET_PILE_USPTO} \
# "
# DATA_PATH="1.0 ${DATASET_PILE_PHILPAPER}"
DATA_PATH="\
    0.0124 ${DATASET_PILE_EUROPARL} \
    0.2532 ${DATASET_PILE_FREELAW} \
    0.0101 ${DATASET_PILE_HACKERNEWS} \
    0.0113 ${DATASET_PILE_NIH} \
    0.0096 ${DATASET_PILE_PHILPAPER} \
    0.1351 ${DATASET_PILE_PMA} \
    0.4670 ${DATASET_PILE_PMC} \
    0.1013 ${DATASET_PILE_USPTO} \
"

if   [[ ${MODEL_SIZE} == 7 ]];   then HIDDEN=4096;  HEADS=32; NUM_QUERY_GROUP=32; NLAYERS=32; FFN_SIZE=11008; NORM_EPS=1e-5;
elif [[ ${MODEL_SIZE} == 13 ]];  then HIDDEN=5120;  HEADS=40; NUM_QUERY_GROUP=40; NLAYERS=40; FFN_SIZE=13824; NORM_EPS=1e-5;
elif [[ ${MODEL_SIZE} == 70 ]];  then HIDDEN=8192;  HEADS=64; NUM_QUERY_GROUP=8;  NLAYERS=80; FFN_SIZE=28672; NORM_EPS=1e-5;
elif [[ ${MODEL_SIZE} == "tiny" ]]; then HIDDEN_SIZE=128;  NUM_HEAD=4; NUM_QUERY_GROUP=4; NLAYERS=4; FFN_SIZE=512; NORM_EPS=1e-5;
else echo "invalid MODEL_SIZE: ${MODEL_SIZE}"; exit 1
fi

#NLAYERS=40
#HIDDEN=5120
#HEADS=40
SEQ=2048
#FFN_SIZE=13824

TP=1
PP=2

MICRO_BATCH=1 # 4
GLOBAL_BATCH=2 # 16

MASTER_ADDR=127.0.0.1
MASTER_PORT=5901
WORLD_SIZE=1
RANK=0
NPROC_PER_NODE=2

TRAIN_ITER=40000 # 40000
EVAL_INTERVAL=50000
SAVE_INTERVAL=20000

DIST_ARGS="
    --master_addr $MASTER_ADDR \
    --master_port $MASTER_PORT \
    --nproc_per_node $NPROC_PER_NODE \
    --nnodes $WORLD_SIZE \
    --node_rank $RANK \
    "

GPT_ARGS="
    --tensor-model-parallel-size $TP \
    --pipeline-model-parallel-size $PP \
    --query-key-layer-scaling \
    --num-layers $NLAYERS \
    --hidden-size $HIDDEN \
    --num-attention-heads $HEADS \
    --seq-length $SEQ \
    --max-position-embeddings $SEQ \
    --micro-batch-size $MICRO_BATCH \
    --global-batch-size $GLOBAL_BATCH \
    --lr 0.0001 \
    --train-iters $TRAIN_ITER \
    --min-lr 1.0e-5 \
    --lr-warmup-fraction .01 \
    --adam-beta1 0.9 \
    --adam-beta2 0.95 \
    --adam-eps 1e-5 \
    --clip-grad 1.0 \
    --bf16 \
    --disable-bias-linear \
    --use-flash-attn \
    --normalization RMSNorm \
    --position-embedding-type rope \
    --swiglu \
    --untie-embeddings-and-output-weights \
    --padded-vocab-size 32000 \
    --ffn-hidden-size $FFN_SIZE \
    --finetune \
    --tune-exit \
    --untie-exit-output-weights \
    --use-exit-norm \
    --use-exit-mlp \
    --tune-exit-pipeline-parallel-size 2 \
    --exit-layer-nums 4 8 12 16 20 24 28 32 \
"
# --tune-exit-pipeline-parallel-size 4

DATA_ARGS="
    --data-path $DATA_PATH \
    --tokenizer-type Llama2Tokenizer \
    --tokenizer-model $TOKENIZER_PATH \
    --split 990,9,1 \
"

OUTPUT_ARGS="
    --log-interval 10 \
    --log-timers-to-tracker \
    --save-interval $SAVE_INTERVAL \
    --eval-interval $EVAL_INTERVAL \
    --eval-iters 1 \
    --wandb-project $PROJECT_NAME \
    --wandb-group $GROUP_NAME \
    --wandb-exp-name $MASTER_NAME \
"

CUR_DIR=$(cd $(dirname "$0") && pwd)
MEGATRON_ROOT_PATH=$(cd "$CUR_DIR/../../.." && pwd)
cd $MEGATRON_ROOT_PATH

nohup torchrun $DIST_ARGS \
    pretrain_early_exit_gpt.py \
    $GPT_ARGS \
    $DATA_ARGS \
    $OUTPUT_ARGS \
    --load $LOAD_PATH \
    --save $CHECKPOINT_PATH > train.log 2>&1 &
disown
