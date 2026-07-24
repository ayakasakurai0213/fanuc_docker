#!/bin/bash
cd ~/ws_fanuc
apt update && rosdep install --ignore-src --from-paths src -y
git config --global --add safe.directory '*'    # test
colcon build --symlink-install --cmake-args -DBUILD_TESTING=1 -DBUILD_EXAMPLES=1