#!/bin/bash
BASE_PATH=/workspace
LOAD_DIR=${BASE_PATH}/model_ckpts/llama2-7b-hf # path to the llama2 huggingface checkpoint dir
SAVE_DIR=${BASE_PATH}/model_ckpts/llama2-7b_hf-to-meg_tp1_pp1 # path to save the converted megatron checkpoint
TP=1  # target tensor parallel size
PP=1  # target pipeline parallel size

TOKENIZER_PATH=${LOAD_DIR}/tokenizer.model

CUR_DIR=$(cd $(dirname "$0") && pwd)
MEGATRON_ROOT_PATH=$(cd "$CUR_DIR/../../.." && pwd)

python $MEGATRON_ROOT_PATH/tools/checkpoint/util.py \
    --model-type EarlyExitGPT \
    --load-dir $LOAD_DIR \
    --save-dir $SAVE_DIR \
    --loader llama2_hf \
    --saver megatron \
    --no-checking \
    --target-tensor-parallel-size $TP \
    --target-pipeline-parallel-size $PP \
    --megatron-path $MEGATRON_ROOT_PATH \
    --tokenizer-model $TOKENIZER_PATH