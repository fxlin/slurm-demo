#!/bin/bash

# https://www.cs.virginia.edu/computing/doku.php?id=compute_slurm

# Run the training script with srun arguments
sbatch \
    --nodes=1 \
    --ntasks-per-node=4 \
    --gres=gpu:2 \
    --cpus-per-task=8 \
    --mem=32GB \
    --time=12:00:00 \
    --partition="gpu" \
    --error="demo_1node.err" \
    --output="demo_1node.log" \
    --mail-type=BEGIN,END \
    --mail-user=${USER}@virginia.edu  \
    run-train.sh
    