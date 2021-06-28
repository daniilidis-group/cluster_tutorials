# Cluster Intro

Start here for a quick getting started tutorial.

## Logging in

You need to be:

1) Wired on campus
2) Wireless on campus
3) UPenn VPN

## Getting resources

All computation in the cluster must be done after creating a request for resources.

### Direct interactive session

This method enables you to get an interactive terminal that holds the resouces

```
srun --partition debug --qos debug --mem=8G --gres=gpu:1 --pty bash
```

### Direct blocking request

This method enables you to submit a job and blocks your terminal until the command has been completed.

```
srun --mem-per-gpu=10G --cpus-per-gpu=4 --gpus=1 nvidia-smi
```

### Non-blocking batch request

This method allows you to schedule a job for the cluster to get to later. These jobs can be significantly more complex than `srun` allows for. This file will be run with `sbatch <filename>`

```
#!/bin/bash
#SBATCH --mem-per-gpu=10G
#SBATCH --cpus-per-gpu=4
#SBATCH --gpus=1
#SBATCH --time=00:10:00
#SBATCH --qos=low
#SBATCH --partition=compute

hostname
nvidia-smi

exit 0
```

## Visualization

Follow the tensorboard tutorial:

[Tensorboard](https://github.com/daniilidis-group/cluster_tutorials/tree/master/tensorboard)
