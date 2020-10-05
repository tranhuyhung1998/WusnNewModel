#!/usr/bin/env bash

DATASET=${1-"small"}
PROCS=2
ALPHA=0.5

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/exact/${DATASET}\
    data/${DATASET}_data/*.in --lax