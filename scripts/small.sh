#!/usr/bin/env bash
python3 scripts/datagen.py -o data/small_data\
    -W 200 -H 200 --depth 1 --height 10\
     --rows 41 --cols 41 --num-sensor 40 --num-relay 40\
     data/dems_data/*.asc
