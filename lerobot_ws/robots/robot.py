from lerobot_robot_ros.robot import ROS2Robot
from lerobot_robot_ros.config import ROS2Config
from .ros_interface import ROS2Interface


class CRXROS(ROS2Robot):
    def __init__(self, config: ROS2Config):
        super().__init__(config)
        self.ros2_interface = ROS2Interface(config.ros2_interface, config.action_type, config.use_isaac)