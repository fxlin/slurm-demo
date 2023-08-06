# SLURM

## Command lists
* `sinfo`
* `squeue`
* `scontrol`
* `srun`
* `sbatch`

## SLURM on conda with 
```
# create a demo env 
conda env create -f environment.yml

# install llama.cpp
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install --upgrade --force-reinstall llama-cpp-python --no-cache-dir

sbatch demo.sh
```


## Direct access to a server
This is for debugging. You shall not use it as an altertive `ssh`
```
# access to a server where your script is running
srun --nodelist ai02 --partition gnolim --pty bash -i -l -
```

