#!/bin/bash
cd ~/ws_moveit/
apt remove ros-$ROS_DISTRO-moveit*
apt update && rosdep install -r --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y
colcon build --mixin release