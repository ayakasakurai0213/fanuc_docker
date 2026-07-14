#!/bin/bash
cd ~/ws_fanuc

rosdep install --ignore-src --from-paths src -y
colcon build --symlink-install --cmake-args -DBUILD_TESTING=1 -DBUILD_EXAMPLES=1