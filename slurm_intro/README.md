# SLURM Intro

## Getting comfortable with SLURM

### Partitions
All nodes in the systems are assigned to one or more partitions that are available for user access given they have sufficient permissions. The non-specific partitions are as follows:

|     Partition    | Time Limit | Valid QOSs              | Nodes                            | Default |
|------------------|------------|-------------------------|----------------------------------|---------|
|  batch           |  1-00:00:00| normal                  |               ALL                |   YES   |
| \<prof\>-compute | 14-00:00:00| varies                  | Professor Specific               |    NO   |


To view the current state of each partition:

```
sinfo
```

In addition to the above partitions, you will see the professor specific partitions that you may or may not have access to.

## srun

Now that you have some idea of how everything is broken down, you can run your first command. `srun` provides a blocking way to run a single command using remote resources.

```
srun --mem-per-gpu=10G --cpus-per-gpu=4 --gpus=1 nvidia-smi
```

The requested resources will be allocated and then your command will run. In this case you should see the GPU information displayed on your console.

## sbatch

Running invidual commands in a blocking manner is often too cumbersome for any large scale projects. `sbatch` provides a method to submit a job(s) to be scheduled and run at the most optimal time.

```
#!/bin/bash
#SBATCH --mem-per-gpu=10G
#SBATCH --cpus-per-gpu=4
#SBATCH --gpus=1
#SBATCH --time=00:10:00

hostname
nvidia-smi

exit 0
```

If the above contents are in `example.bash`, you can submit this job through `sbatch example.bash`. Upon being scheduled you will see a new file `slurm-<job_id>.out` that contains the contents of stdout from the above bash script.

## A note about accurate estimates

Accurate time and resource estimates are critical to ensure that as many jobs can be scheduled as possible. If you don't request enough, your job could crash in often unpredictable ways. If you request too much, those resources go to waste as they could be used for another job at the same time. In addition, your `fairshare` will be billed for resources that you request and thus could be adversely affected if you request a large number of unused resources.

## Running an interactive session

Interactive session are designed to help facilitate efficient debugging of your code. You can request an interactive terminal on any partition or QOS, however debug is recommended as it will be able to preempt most currently running jobs.

```
srun --partition debug --qos debug --mem=8G --gres=gpu:1 --pty bash
```

## Stopping jobs

To stop a job you will need to know your Job ID which is announced after you use any command that requests resources. In addition, you can look at squeue to find a jobid.

```
scancel <job_id>
```

## Monitoring your jobs

### Queue
Checking the work queue:
```
squeue
```
You will see all of the currently running jobs and scheduled jobs when running this command. Use the `sprio` command to check the priority level of each job.


## Advanced scheduling options

### QOS

Depending on your affiliation, you will have at least 3 QOSs available to you:

| QOS  | # GPUs | Preempts | Exempt Time | Max GPU Min Per Job | Max Jobs | Max Submit Jobs | Priority | Usage Factor | Default |
|------|--------|----------|-------------|---------------------|----------|-----------------|----------|--------------|---------|
|normal|        |          |  00:30:00   |                     |   60     |      120        |    1     |       10     |   YES   |

Professors who have their own resources have defined their own QOS to ensure equitable distribution of resources within their group. Examples are as follows:

|     QOS     | # GPUs |     Preempts   |
|-------------|--------|----------------|
| \<prof\>-med  |     10 | low            |
| \<prof\>-high |      1 | low, \<prof\>-med|
  
For more specifics of what currently exists you can look at:

```
sacctmgr show qos
```

Each QOS attempts to fufil a separate requirement that people might have and encourages smaller more managable chunks of runtime.

- \# GPUs is the total per user for that QOS
- Preempts indicates which QOS can be preempted when you start a job with that QOS
- Exempt time indicates the amount of wall time that must pass before a job can be preempted (this is considered "safe" time)
- Max GPU Min Per Job is the total number of minutes your job can use on a GPU, (i.e. using 3 GPUs for 15 minutes is 45 GPU minutes)
- Max Jobs is the total number of jobs that can be accruing time in that QOS per user
- Max Submit Jobs is the total number of jobs that you can submit in that QOS per user
- Priority is an additional priority factor that gets accounted for in the scheduler
- Usage Factor is how much it "costs" to run in this partition

The basic QOSs (listed above) provide general access to a large number of resources. More specialized QOSs will be assigned by each group for their specific resources, these will take priority over these more generic QOSs.

### Requesting a specific GPU

You are allowed to be more specific about the type of GPU that you want to use:

```
srun --mem-per-gpu=10G --cpus-per-gpu=4 --gpus=gtx1080ti:1 nvidia-smi
```

The list of types:

|      Name    | Architecture | VRAM |
|--------------|--------------|------|
| geforce_rtx_2080_ti   |   Turing     | 11GB |
| rtx_a6000 | Ampere | 48GB |
| a40       | Ampere | 48GB |
| a10       | Ampere | 24GB |
| geforce_rtx_3090 | Ampere | 24GB |
| l40 | Lovelace | 48GB |



### Requesting a specific node

If a specific node has the configuration that you'd like:
```
srun --mem-per-gpu=10G --cpus-per-gpu=4 --gpus=1 -w <node_name> nvidia-smi
```


## Batches

You will need to make a file that contains the parameters of the batch of jobs:

```
#!/bin/bash
#SBATCH --mem-per-gpu=10G
#SBATCH --cpus-per-gpu=4
#SBATCH --gpus=1
#SBATCH --array=0-3
#SBATCH --time=00:10:00

hostname
nvidia-smi

echo "My unique array ID is $SLURM_ARRAY_TASK_ID out of $SLURM_ARRAY_TASK_MAX"

exit 0
```

Write that to a file called test.bash and to run it use:

```
sbatch test.bash
```

This will run 4 jobs (--array=0-3) that each check the host they ran on and check the GPU itself.

Each SBATCH line denotes a separate option which is further defined in https://slurm.schedmd.com/sbatch.html

By default, a log file named `slurm-<job_id>.out` should also be generated in the same directory as `test.bash`, which you can view as a live log with:
```
tail -f slurm-<job_id>.out
```
sbatch allows you to specify this file to be anything you would like. Check their documentation for more info.

You can also start an interactive terminal for a job that you started with sbatch (to check CPU or GPU utilization, e.g.). To do so, you need to start a new step/task within the running job:
```
srun --jobid <job_id> --pty bash
```
With `squeue -s` you can see that your new step has a step id like `<job_id>.<int>.`

## Long running jobs

Jobs that run for a long time (i.e. more time than the QOS allows for) can still be scheduled in blocks and automatically requeued. This is handled by having the correct exiting conditions:

1) Exit code 3 from the primary job script
2) No signal was sent to your sub job

This is an example in bash to create a job array with 4 elements that repeats forever. Please feel free to try this script, but do not allow it to run for forever.

```
#!/bin/bash
#SBATCH --mem-per-gpu=10G
#SBATCH --cpus-per-gpu=4
#SBATCH --gpus=1
#SBATCH --array=0-3
#SBATCH --time=00:10:00

hostname
nvidia-smi
exit 3
```

## Handling preemption

Jobs that are in a lower QOS allow other jobs to preempt them. This can be handled in a couple different ways. The most robust is to catch the signal (SIGTERM) and checkpoint your model. This can be seen further in the `mnist` tutorial. Jobs that are preempted are automatically placed back into the queue to be rescheduled.

# Deep Learning Packages

We provide the following packages installed on the base of every machine:

| Name    | Version |
|---------|---------|
| Python  |  3.10   |
| Pytorch |  1.13   |
| Tensorflow | 2.0 |

If the following command:
```
nvcc --version
```
returns `Command 'nvcc' not found` you may need to update your path to include cuda. To do so temporarily, run:
```
export PATH=$PATH:/usr/local/cuda/bin
```
To do so perminantly, add the line above to the bottom of your bashrc, which should be at `~/.bashrc`.

In addition, you can always use venv for your specific use case. It is recommended to keep libraries like that on NVMe for speed of loading. For example, from inside of a slurm interactive session:

```
cd /scratch/<username>/virtual_envs
python3 -m venv test
```


# Helpful Debugging Tools

If you want to see how many cpus and gpus each node has/how many are allocated, you can run the following command.
```
scontrol show node
```
This will display a list of all of the nodes and information about them. An example output is shown below.

```
NodeName=node-2080ti-3 Arch=x86_64 CoresPerSocket=20 
   CPUAlloc=10 CPUTot=40 CPULoad=8.42
   AvailableFeatures=(null)
   ActiveFeatures=(null)
   Gres=gpu:rtx2080ti:4(S:0)
   NodeAddr=node-2080ti-3 NodeHostName=node-2080ti-3 Version=19.05.5
   OS=Linux 4.15.0-108-generic #109-Ubuntu SMP Fri Jun 19 11:33:10 UTC 2020 
   RealMemory=92000 AllocMem=0 FreeMem=59361 Sockets=1 Boards=1
   State=MIXED ThreadsPerCore=2 TmpDisk=0 Weight=1 Owner=N/A MCS_label=N/A
   Partitions=compute,kostas-compute 
   BootTime=2020-06-29T13:54:09 SlurmdStartTime=2020-07-11T11:24:16
   CfgTRES=cpu=40,mem=92000M,billing=40,gres/gpu=4
   AllocTRES=cpu=10,gres/gpu=3
   CapWatts=n/a
   CurrentWatts=0 AveWatts=0
   ExtSensorsJoules=n/s ExtSensorsWatts=0 ExtSensorsTemp=n/s
```
For this node, the second line shows the allocated vs total cpus.  The total number and type of gpus is shown under `Gres`.  The number of allocated gpus is shown under `AllocTRES`.

