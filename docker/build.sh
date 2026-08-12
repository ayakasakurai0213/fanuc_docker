#!/bin/bash
cd ~/moveit_ws/src
vcs import --recursive < moveit2_tutorials/moveit2_tutorials.repos
cd ..
apt remove ros-$ROS_DISTRO-moveit*
apt update && rosdep install -r --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y
colcon build --mixin release

cd ~/fanuc_ws
# apt update && rosdep install --ignore-src --from-paths src -y
git config --global --add safe.directory '*'    # test
colcon build --symlink-install --cmake-args -DBUILD_TESTING=1 -DBUILD_EXAMPLES=1