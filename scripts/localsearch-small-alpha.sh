PROCS=4

python LSR.py --indir small_data --init 0 --alpha 0.0 --procs $PROCS
python LSR.py --indir small_data --init 0 --alpha 0.25 --procs $PROCS
python LSR.py --indir small_data --init 0 --alpha 0.75 --procs $PROCS
python LSR.py --indir small_data --init 0 --alpha 1.0 --procs $PROCS
