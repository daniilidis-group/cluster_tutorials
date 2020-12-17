#!/usr/bin/python3
# This is a simple util that prints the tensorboard address so that the user doesn't have to look it up manually in the logs. 
# It also removes the log file since they are usually unnecessary and cause clutter

import os.path
import tempfile
import sys
import time

a = tempfile.NamedTemporaryFile('w', suffix='.log', dir="/mnt/beegfs/" + os.path.expanduser('~'))
cmd = 'sbatch --job-name ' + sys.argv[1] + ' --output ' + a.name + ' tensorboard.bash ' + sys.argv[1]
print(cmd)
os.system(cmd)
while not os.path.exists(a.name):
    time.sleep(0.01)

while True:
    with open(a.name, 'r') as file:
        x = file.read()
        if len(x.split('\n')) > 1:
            print(x.split('\n')[0])
            break
        time.sleep(0.01)
