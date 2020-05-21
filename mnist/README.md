# MNIST

This is a tutorial for training MNIST in the cluster with handling all of the various signals and timing that could be needed.

## mnist.py

Inside of the section labeled `CUSTOM CLUSTER OVERHEAD` is ClusterStateManager that handles:

1) Signals - external signals for preemption (for this small example this is a non issue, but can be observed by running this directly in interactive and using ctrl+c)
2) Timing - this is handled through a signal and an alarm that triggers after the prespecified amount of time
3) Exit Code - based on the type of signal (or lack there of) this class creates a cluster compliant exit code to requeue or complete

There is also some small code that saves a network, optimizer, and current epoch and reloads it if the checkpoint exists. In a larger setup, you may want to save more information such as current step, the current state of your dataloader, etc. but for this small example the epoch will be enough. Throughout the code, these components are used to load the model, check if we need to exit and save, and finally generate an appropriate exit code. The ClusterStateManager is a class that is applicable to any computation that you want to use in the cluster as is just manages an internal state asynchronously.


It is important to note that due to the asynchronous nature of CUDA, we encourage you to keep to the philosophy of not checkpointing in the signal handler as you will not know what kernels are loaded up to run. The only time we know the state is when we finish a training iteration and thus that is where we suggest you checkpoint. This is more work, but will lead to much more robust code.

## mnist.bash

This is the file that you will submit to SLURM to actually run your code. It contains the parameters for the compute configuration as well as passing along the python exit code to SLURM for appropriate handling.


## Running the code

```
sbatch mnist.bash
```

You will be able to look at the queue and see your job progress through the various states.


## QUIRKS / NOTES

So you may notice that your job spends a lot of time in the queue pending. This is due to the high turn around rate on this since we are only training for 10 seconds at a time. This means that the overhead of running in SLURM is very high for this small of a task because you have to wait for the scheduler to get back around to your job.
