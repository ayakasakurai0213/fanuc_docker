# fanuc_docker

## install
```
cd fanuc_docker/docker
docker compose build
```
```
docker compose up
docker exec -it fanuc_ros2 bash
```
## build
```
cd ~/moveit_ws
./build_moveit.sh
```
```
cd ~/fanuc_ws
./build_fanuc.sh
```

## How to use
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
lerobot-teleoperate --robot.type=fanuc_ros --robot.id=fanuc_arm --teleop.type=keyboard_joint --teleop.id=fanuc_arm --display_data=true --robot.use_isaac=true
```

record data
```
lerobot-record --robot.type=fanuc_ros --robot.id=fanuc_arm --teleop.type=keyboard_joint --teleop.id=fanuc_arm --display_data=true --robot.use_isaac=true --dataset.repo_id=/test --dataset.num_episodes=5 --dataset.single_task="test" --dataset.root=./datasets/test
```