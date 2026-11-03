from dataclasses import dataclass, field
from lerobot.robots import RobotConfig
from lerobot_robot_ros.config import ROS2Config, ActionType, ROS2InterfaceConfig


@RobotConfig.register_subclass("fanuc_ros")
@dataclass
class CRXROSConfig(ROS2Config):

    action_type: ActionType = ActionType.JOINT_TRAJECTORY

    ros2_interface: ROS2InterfaceConfig = field(
        default_factory=lambda: ROS2InterfaceConfig(
            arm_joint_names=["J1", "J2", "J3", "J4", "J5", "J6"],
            gripper_joint_name="finger_joint",
            base_link="base_link",
            min_joint_positions=[-3.49066, -3.1398473, -1.18682, -3.31613, -3.1398473, -3.92699],     # -200, -179.9, -68, -190, -179.9, -225
            max_joint_positions=[3.49066, 3.1398473, 4.32842, 3.31613, 3.1398473, 3.92699],   # 200, 179.9, 248, 190, 179.9, 225
            gripper_open_position=0.0,
            gripper_close_position=0.7929,
        ),
    )
    
    use_isaac: bool = False