# Tensorboard

## How to run

We utilize `sbatch` to schedule a job into the tensorboard node. As with any other job, you can pass command line arguments as you normally would to a bash or other script.

```
sbatch tensorboard.bash <folder_name>
```

This will launch your SLURM job and produce output that contains the IP and port as well as any output that tensorboard produces.

## Current limitations

Right now the default script can only use a single core for loading of data. While OverProvisioning does work, we want to pack as many visualization processes onto one machine as possible. If you find yours particularly slow, feel free to try adding extra cores to `tensorboard.bash` as this will most likely help.

| QOS | Max Jobs | Max Submit Jobs | Priority | Usage Factor |
|-----|----------|-----------------|----------|--------------|
|  viz|    3     |       3         |     1    |       1      |
