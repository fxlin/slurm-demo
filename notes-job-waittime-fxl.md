notes on job submission time, wait time, etc. 

## squeue
can only show: the time a job has been pending (for pending jobs), and the time a job has been running (for running jobs).
cannot show: pending time for running jobs. (cf sacct below)

#### sqwueue limitation
However, squeue can provide the elapsed time for running jobs, as well as some
information about pending jobs, such as how long they have been in the queue

### find a list of gpu pending jobs 

```
squeue --states=PD --format="%.8u %.18i %.10P %.8j %.2t %.10M %.6D %R %b" | grep "gres/gpu"
```

### find a list of gpu running jobs 
```
squeue --states=R --format="%.8u %.18i %.10P %.8j %.2t %.10M %.6D %R %b" | grep "gres/gpu"
```

### find users that have gpu jobs (runnign or pending) 

```
squeue --format="%.8u %.18i %.10P %.8j %.2t %.10M %.6D %R %b" | grep "gres/gpu" | awk '{print $1}' | sort | uniq
```

### find users that have gpu jobs (runnign or pending), sort by # running jobs
```
squeue --format="%.8u %.2t %b" | grep gpu | awk '
{
    user=$1; state=$2;
    if (state == "R") { running[user]++; }
    else if (state == "PD") { pending[user]++; }
    total[user]++;
}
END {
    for (user in total) {
        printf "%s %d %d\n", user, running[user], pending[user];
    }
}' | sort -k2,2nr

# user running pending
ssy4uh 32 11
qwp4pk 15 0
etc6bd 11 0
kca4vg 7 0
nkp2mr 5 0
csk4sr 4 0
dcs3zc 4 1
```

## sacct

sacct, by default, only shows own jobs. (both on cs servers and rivanna, configurable??)

only shows GPU jobs. 
elapsed: time the job has been running 
"-P: Use the "parsable" format to make it easier for further processing."
```
sacct --format=JobID,JobName,Submit,Start,Elapsed,ReqTRES -P | grep "gres/gpu"
84586|1b5-pre-x59|2024-11-21T14:39:35|2024-11-21T15:06:03|2-00:14:36|billing=2,cpu=2,gres/gpu=4,mem=256G,node=1
84602|3b-pre-x52|2024-11-21T14:39:43|2024-11-21T15:27:00|1-23:53:39|billing=2,cpu=2,gres/gpu=4,mem=256G,node=1
```

if the user ID is known, can specify to show all jobs of that user.
```
sacct -u ssy4uh --format=JobID,JobName,Submit,Start,Elapsed,ReqTRES -P | grep "gres/gpu"
```

or specify a particular job ID
```
sacct -j 84586 --format=JobID,JobName,Submit,Start,Elapsed,ReqTRES -P | grep "gres/gpu"
```