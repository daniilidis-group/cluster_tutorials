#!/bin/bash
#SBATCH -w node-2080ti-[0-6]
#SBATCH --cores=1
#SBATCH --mem=1G
#SBATCH --time=00:10:00
#SBATCH --qos=low

ENROOT_DATA_PATH="/tmp/enroot-data/user-\$(id -u)"

rm -r $ENROOT_DATA_PATH
