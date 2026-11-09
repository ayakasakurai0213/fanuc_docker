import numpy as np
import time
import argparse

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from geometry_msgs.msg import TwistStamped

from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.utils.constants import ACTION
from lerobot.utils.cycle_timer import CycleTimer


class JointCommandPublisher(Node):
    def __init__(self):
        super().__init__("joint_command_publisher")
        
        self.joint_name = ["J1", "J2", "J3", "J4", "J5", "J6", "finger_joint"]
        self.action = None
        
        self.pub = self.create_publisher(JointState, "/isaac_joint_commands", 10)

    def publish(self):
        msg = JointState()
        msg.name = self.joint_name
        
        if self.action is not None:
            msg.position = self.action

        self.pub.publish(msg)


class ServoPublisher(Node):
    def __init__(self):
        super().__init__("servo_publisher")
        
        self.name = ["linear_x", "linear_y", "linear_z", "angular_x", "angular_y", "angular_z"]
        self.gripper_name = ["finger_joint"]
        self.action = None
        
        self.arm_pub = self.create_publisher(
            TwistStamped,
            "/servo_node/delta_twist_cmds",
            10
        )
        self.gripper_pub = self.create_publisher(
            JointTrajectory,
            "/gripper_controller/joint_trajectory", 
            10
        )

    def publish(self):
        arm_msg = TwistStamped()
        gripper_msg = JointTrajectory()
        
        arm_msg.header.stamp = self.get_clock().now().to_msg()
        arm_msg.header.frame_id = 'base_link'
        
        gripper_msg.joint_names = self.gripper_name
        
        if self.action is not None:
            arm_msg.twist.linear.x = float(self.action[0])
            arm_msg.twist.linear.y = float(self.action[1])
            arm_msg.twist.linear.z = float(self.action[2])
            
            arm_msg.twist.angular.x = float(self.action[3])
            arm_msg.twist.angular.y = float(self.action[4])
            arm_msg.twist.angular.z = float(self.action[5])
            
            point = JointTrajectoryPoint()
            point.positions = self.action[6:]
            gripper_msg.points.append(point)
        
        self.arm_pub.publish(arm_msg)
        self.gripper_pub.publish(gripper_msg)


def main(args):
    rclpy.init()
    
    if args.action_type == "joint_pos":
        publisher = JointCommandPublisher()
    elif args.action_type == "cartesian":
        publisher = ServoPublisher()
    
    dataset = LeRobotDataset(args.repo_id, root=args.root, episodes=[args.episode_num])
    actions = dataset.select_columns(ACTION)
    
    timer = CycleTimer(dataset.fps, records_data=False)
    try:     
        for idx in range(dataset.num_frames):
            timer.tick()
            
            with timer.section("read_frame"):
                action = actions[idx][ACTION]
                publisher.action = action
                print(f"action: {action}")
                
            if rclpy.ok():
                with timer.section("send"):
                    publisher.publish()
                
            timer.wait()
                             
    except KeyboardInterrupt:
        pass
    
    finally:
        publisher.destroy_node()
        rclpy.shutdown()
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replay LeRobot datasets on CRX")
    parser.add_argument("--repo_id", type=str, required=True, help="Repository ID")
    parser.add_argument("--root", type=str, required=True, help="Path of lerobot dataset.")
    parser.add_argument("--episode_num", type=int, default=0, help="Episode number")
    parser.add_argument("--action_type", type=str, default="joint_pos", help="'joint_pos' or 'cartesian'")
    parser.add_argument("--use_isaac", type=bool, default=False, help="On isaac sim")
    args = parser.parse_args()
    
    main(args)
