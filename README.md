# fanuc_docker
moveit with mock
```
ros2 launch fanuc_moveit_config fanuc_moveit.launch.py robot_model:=crx5ia_2f_85gripper use_mock:=true
```
moveit with actual robot
```
ros2 launch fanuc_moveit_config fanuc_moveit.launch.py robot_model:=crx5ia_2f_85gripper robot_ip:="192.168.XXX.XXX"
```

in isaac sim
```
ros2 launch fanuc_moveit_config fanuc_moveit.launch.py robot_model:=crx5ia_2f_85gripper sim_isaac:=true
```

teleop with keyboard
```
ros2 launch fanuc_moveit_config demo_ros_api.launch.py robot_model:=crx5ia_2f_85gripper use_mock:=true
```