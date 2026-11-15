#!/usr/bin/env bash
set -e
for s in 0 1 2 3 4; do
  python data/starter/generate_data.py --output data/data_seed_$s --seed $s --urgent-prior 0.30
done
