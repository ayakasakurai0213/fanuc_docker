#!/bin/bash
cd ~/moveit_ws/src
vcs import --recursive < moveit2_tutorials/moveit2_tutorials.repos
apt remove ros-$ROS_DISTRO-moveit*
apt update && rosdep install -r --from-paths . --ignore-src --rosdistro $ROS_DISTRO -r -y
# colcon build --mixin release
cd ..
colcon build --event-handlers desktop_notification- status- --cmake-args -DCMAKE_BUILD_TYPE=Release --continue-on-error

cd ~/fanuc_ws
# apt update && rosdep install --ignore-src --from-paths src -y
git config --global --add safe.directory '*'    # test
colcon build --symlink-install --cmake-args -DBUILD_TESTING=1 -DBUILD_EXAMPLES=1