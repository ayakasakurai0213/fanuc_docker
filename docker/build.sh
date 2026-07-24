#!/bin/bash
cd ~/ws_fanuc
apt update && rosdep install --ignore-src --from-paths src -y
git config --global --add safe.directory '*'    # test
colcon build --symlink-install --cmake-args -DBUILD_TESTING=1 -DBUILD_EXAMPLES=1

cd ~/ws_moveit/
apt remove ros-$ROS_DISTRO-moveit*
apt update && rosdep install -r --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y
colcon build --mixin release