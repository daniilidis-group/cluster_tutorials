# Mujoco

Daniilidis-group has an academic lab license for [Mujoco](http://www.mujoco.org/), a physics simulation software useful for robotic simulations and general simulations of physical processes with both rigid and deformable objects. It is widely used in reinforcement learning as well as robotics research. 

By using this license, you acknowledge that you understand the limitations. A single PI license only covers personnel working under the direct supervision of the PI and students enrolled in a PhD-level class taught by the PI. Here's a list of the licenses that currently exist on the cluster. (These licenses will only be accessible on the appropriate machines.)

| Name | License Type |  Experation Date  |
|------|--------------|-------------------|
|Kostas|   Single PI  | February 18, 2021 |


# Setting up mujoco

Run the following to setup your environment:
```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mujoco-kostas/mujoco200_linux/bin
# For mujoco_py:
export MUJOCO_PY_MUJOCO_PATH=/opt/mujoco-kostas/mujoco200_linux
export MUJOCO_PY_MJKEY_PATH=/opt/mujoco-kostas/mjkey.txt
# If you want to use DM Control Suite, also specify:
export MJLIB_PATH=/opt/mujoco-kostas/mujoco200_linux/bin/libmujoco.so
export MJKEY_PATH=/opt/mujoco-kostas/mjkey.txt
```

Once you set up the environment variables, you should be able to use the mujoco library. You might want to use a python wrapper around it, such as OpenAI's [mujoco_py](https://github.com/openai/mujoco-py) or [DeepMind Control Suite](https://github.com/deepmind/dm_control). Install mujoco_py as follows:

```
srun --partition debug --qos debug --pty bash
# Install mujoco_py. Here, we install the 2.0.2.8 version to avoid conflict with the pre-installed mujoco_py
pip3 install --user mujoco_py==2.0.2.8
exit
```

# Getting started

You can play around with mujoco_py by executing the following on kostas-ap

```
# Get an interactive session
srun --partition debug --qos debug --mem=8G --gpus=1 --pty bash
# Setup environment (if you haven't yet)
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mujoco-kostas/mujoco200_linux/bin
export MUJOCO_PY_MUJOCO_PATH=/opt/mujoco-kostas/mujoco200_linux
export MUJOCO_PY_MJKEY_PATH=/opt/mujoco-kostas/mjkey.txt
# Open an interactive python shell
python3
# Run mujoco_py toy program
import mujoco_py
import os
mj_path, _ = mujoco_py.utils.discover_mujoco()
xml_path = os.path.join(mj_path, 'model', 'humanoid.xml')
model = mujoco_py.load_model_from_path(xml_path)
sim = mujoco_py.MjSim(model)

print(sim.data.qpos)

sim.step()
print(sim.data.qpos)
```

If this code executes without an error, you are likely to have just used mujoco.

# Submitting a job

The code above is provided in the form of an example script in the [mujoco_test.py](mujoco_test.py) file. To run this script as a job, you will need to use srun or sbatch. 

```
# It is convenient to put the mujoco variables in your bashrc file:
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/mujoco-kostas/mujoco200_linux/bin' >> ~/.bashrc
echo 'export MUJOCO_PY_MUJOCO_PATH=/opt/mujoco-kostas/mujoco200_linux' >> ~/.bashrc
echo 'export MUJOCO_PY_MJKEY_PATH=/opt/mujoco-kostas/mjkey.txt' >> ~/.bashrc
source ~/.bashrc

# You will further need to make the mujoco script executable
chmod 744 mujoco_test.py

# You can now run the job
srun --qos=low --time=00:01:00 mujoco_test.py
```

You can also use sbatch in the same way
```
sbatch --qos=low --time=00:01:00 mujoco_test.py
```

# Getting help
If you are having trouble with using the daniilidis-group mujoco license, you could contact Oleg (oleh@seas.upenn.edu).
