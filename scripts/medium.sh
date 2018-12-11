#!/usr/bin/env bash
python3 scripts/datagen.py -o data/medium_data\
    -W 500 -H 500 --depth 1 --height 10\
     --rows 101 --cols 101 --num-sensor 100 --num-relay 100\
     data/dems_data/*.asc
