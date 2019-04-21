#!/usr/bin/env bash

DATASET=${1-"small"}
PROCS=2
ALPHA=0.5

python3 exact.py -p $PROCS --alpha $ALPHA -i 1\
    -o data/${DATASET}_data/approx\
    --lax data/${DATASET}_data/*.in #> data/${DATASET}_data/BOUND1

python3 exact.py -p $PROCS --alpha $ALPHA -i 2\
    -o data/${DATASET}_data/approx\
    --lax data/${DATASET}_data/*.in #> data/${DATASET}_data/BOUND1

python3 exact.py -p $PROCS --alpha $ALPHA -i 3\
    -o data/${DATASET}_data/approx\
    --lax data/${DATASET}_data/*.in #> data/${DATASET}_data/BOUND1

python3 exact.py -p $PROCS --alpha $ALPHA -i 4\
    -o data/${DATASET}_data/approx\
    --lax data/${DATASET}_data/*.in #> data/${DATASET}_data/BOUND1

python3 exact.py -p $PROCS --alpha $ALPHA -i 5\
    -o data/${DATASET}_data/approx\
    --lax data/${DATASET}_data/*.in #> data/${DATASET}_data/BOUND1

python3 exact.py -p $PROCS --alpha $ALPHA -i 6\
    -o data/${DATASET}_data/approx\
    --lax data/${DATASET}_data/*.in #> data/${DATASET}_data/BOUND1

python3 exact.py -p $PROCS --alpha $ALPHA -i 7\
    -o data/${DATASET}_data/approx\
    --lax data/${DATASET}_data/*.in #> data/${DATASET}_data/BOUND1

python3 exact.py -p $PROCS --alpha $ALPHA -i 8\
    -o data/${DATASET}_data/approx\
    --lax data/${DATASET}_data/*.in #> data/${DATASET}_data/BOUND1

python3 exact.py -p $PROCS --alpha $ALPHA -i 9\
    -o data/${DATASET}_data/approx\
    --lax data/${DATASET}_data/*.in #> data/${DATASET}_data/BOUND1

python3 exact.py -p $PROCS --alpha $ALPHA -i 10\
    -o data/${DATASET}_data/approx\
    --lax data/${DATASET}_data/*.in #> data/${DATASET}_data/BOUND1