#!/bin/bash
# --- this job will be run on any available node
# and simply output the node's hostname to
# my_job.output
#SBATCH --job-name="SLURM Demo"
#SBATCH --error="demo.err"
#SBATCH --output="demo.log"
#SBATCH --partition=gpu
#SBATCH --nodelist=cheetah02
#SBATCH --gres=gpu:2

source /etc/profile.d/modules.sh
eval "$(conda shell.bash hook)"
conda activate slurm-demo
module load cuda-toolkit-11.7.0


python llm.py








# Legacy
#export CNN_PATH=/bigtemp/slurm-demo/detectron2
#
#python $CNN_PATH/demo/demo.py \
#    --config-file "$CNN_PATH/configs/COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml" \
#    --input "$CNN_PATH/demo/input1.jpg" \
#    --opts MODEL.WEIGHTS "$CNN_PATH/demo/model_final_280758.pkl"
#
