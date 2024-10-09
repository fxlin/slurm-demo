#!/bin/bash

# https://www.cs.virginia.edu/computing/doku.php?id=compute_slurm

# Run the training script with srun arguments

export NGPUS=2
export NNODES=2

sbatch \
    --nodes=${NNODES} \
    --gres=gpu:${NGPUS} \
    --cpus-per-task=8 \
    --mem=32GB \
    --time=12:00:00 \
    --partition="gpu" \
    --error="demo_2nodes.err" \
    --output="demo_2nodes.log" \
    --mail-type=BEGIN,END \
    --mail-user=${USER}@virginia.edu  \
    run-train.sh
    
