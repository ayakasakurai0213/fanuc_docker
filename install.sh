#!/bin/bash
cd ~
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ~/Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc
rm ~/Miniconda3-latest-Linux-x86_64.sh

conda create -n lerobot-ros python=3.12
conda activate lerobot-ros
conda install -c conda-forge libstdcxx-ng -y

cd ~/lerobot_ws/lerobot_ros
pip install -e lerobot_teleoperator_devices
pip install -e lerobot_robot_ros
pip install -e lerobot