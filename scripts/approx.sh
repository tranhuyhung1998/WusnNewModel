#!/usr/bin/env bash

DATASET=${1-"small"}
PROCS=4
ALPHA=0.5

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND
