Sample scripts submitting GPU jobs to cs servers
The job trains a simple CNN model (only 4MB of parameters) using the MNIST dataset, leveraging the PyTorch Lightning framework for distributed training. The actual job takes less than 2 minutes to run on two GPUs.

## Usage

Login to "portal".

### Submit a Job Using One Node (2 GPUs)

```bash
xl6yq@portal10 (main)[cs-server]$ ./submit.sh 
Submitted batch job 327638
xl6yq@portal10 (main)[cs-server]$ squeue
    JOBID                 NAME    STATE NODELIST(REASON)     TIME       FEATURES TRES_PER_NODE
    327638         run-train.sh  PENDING (None)               0:00       (null) gres/gpu:2
```

### Submit a Job Using Two Nodes (2 GPUs Each)

```bash
xl6yq@portal10 (main)[cs-server]$ ./submit-2nodes.sh 
Submitted batch job 327639
xl6yq@portal10 (main)[cs-server]$ squeue
    JOBID                 NAME    STATE NODELIST(REASON)     TIME       FEATURES TRES_PER_NODE
    327641         run-train.sh  RUNNING lynx[06-07]          0:39       (null) gres/gpu:2
    327638         run-train.sh  RUNNING sds02                5:39       (null) gres/gpu:2
```

Successful jobs' `.err` files should look like:

```
[W reducer.cpp:1300] Warning: find_unused_parameters=True was specified in DDP constructor, but did not find any unused parameters in the forward pass. This flag results in an extra traversal of the autograd graph every iteration, which can adversely affect performance. If your model indeed never has any unused parameters in the forward pass, consider turning this flag off. Note that this warning may be a false positive if your model has flow control causing later iterations to have unused parameters. (function operator())
`Trainer.fit` stopped: `max_epochs=5` reached.
```
