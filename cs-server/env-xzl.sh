module load nvtop
module load cuda-toolkit-12.4.0   # needed.

# needed for cnn training 
module load cudnn-8.9.5_cuda12.x
# why need this???
export LD_LIBRARY_PATH=/sw/ubuntu-22.04/cudnn/8.9.5_cuda12.x/lib:$LD_LIBRARY_PATH

alias python='python3'
alias pip3='python3 -m pip'

#export CUDA_VISIBLE_DEVICES=1,2,3

#expected by deepspeed installation
export CUDA_HOME=/sw/ubuntu-22.04/cuda/12.4.0/
# many things will install here
export PATH=$PATH:${HOME}/.local/bin