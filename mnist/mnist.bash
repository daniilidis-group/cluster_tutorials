#!/bin/bash
#SBATCH --gpus=1
#SBATCH --mem-per-gpu=10G
#SBATCH --cpus-per-gpu=4
#SBATCH --time=00:01:00
#SBATCH --qos=low

python3 mnist.py

PYTHON_EXIT_CODE=$?

exit $PYTHON_EXIT_CODE
