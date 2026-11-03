#!/bin/bash
# source ~/.bashrc
# conda create -n lerobot-ros python=3.12
# conda activate lerobot-ros
# echo "conda activate lerobot-ros" >> ~/.bashrc
conda install -c conda-forge libstdcxx-ng -y
conda install -c conda-forge ffmpeg -y

cd ~/lerobot_ws/lerobot_ros
pip install -e lerobot_teleoperator_devices
pip install -e lerobot_robot_ros
cd ..
pip install -e lerobot
# pip install "isaacteleop[cloudxr,retargeters-lite]~=1.3.131" "scipy>=1.14"
pip install "isaaccapture[cloudxr,retargeters-lite]~=1.7.0" "scipy>=1.14" --extra-index-url https://pypi.nvidia.com