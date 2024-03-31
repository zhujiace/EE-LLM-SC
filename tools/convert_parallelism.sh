#!/bin/bash
BASE_PATH=/workspace
# load/save dir
LOAD_DIR=${BASE_PATH}/model_ckpts/EE-LLM-7B-dj-refine-150B
SAVE_DIR=${BASE_PATH}/model_ckpts/EE-LLM-7B-dj-refine-150B-tp1-pp2

LOAD_ITER=0

# target parallelism
TP=1
PP=2

TOKENIZER_PATH=${LOAD_DIR}/tokenizer.model

CUR_DIR=$(cd $(dirname "$0") && pwd)
MEGATRON_ROOT_PATH=$(cd "$CUR_DIR/.." && pwd)
cd $MEGATRON_ROOT_PATH

python $MEGATRON_ROOT_PATH/tools/checkpoint/util.py \
    --model-type EarlyExitGPT \
    --load-dir $LOAD_DIR \
    --save-dir $SAVE_DIR \
    --load-iteration $LOAD_ITER \
    --target-tensor-parallel-size $TP \
    --target-pipeline-parallel-size $PP \
    --megatron-path $MEGATRON_ROOT_PATH
    