#!/usr/bin/env bash

DATASET=${1-"small"}
PROCS=2
ALPHA=0.5

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND1

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND2

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND3

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND4

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND5

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND6

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND7

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND8

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND9

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND10

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND11

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND12

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND13

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND14

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND15

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND16

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND17

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND18

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND19

python3 exact.py -p $PROCS --alpha $ALPHA\
    -o results/approx/${DATASET}\
    --lax data/${DATASET}_data/*.in > data/${DATASET}_data/BOUND20
