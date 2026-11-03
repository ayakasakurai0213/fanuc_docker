import numpy as np
import time
import argparse

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.utils.constants import ACTION
from lerobot.utils.cycle_timer import CycleTimer


class JointCommandPublisher(Node):
    def __init__(self):
        super().__init__("joint_command_publisher")
        
        self.joint_name = ["J1", "J2", "J3", "J4", "J5", "J6", "finger_joint"]
        self.joint_pos = None
        
        self.pub = self.create_publisher(JointState, "/isaac_joint_commands", 10)

    def callback(self):
        msg = JointState()
        msg.name = self.joint_name
        
        if self.joint_pos is not None:
            msg.position = self.joint_pos

        self.pub.publish(msg)
        print(f"joint_pos: {msg.position}")


def main(args):
    rclpy.init()
    joint_command_pub = JointCommandPublisher()

    dataset = LeRobotDataset(args.repo_id, root=args.root, episodes=[args.episode_num])
    actions = dataset.select_columns(ACTION)
    
    timer = CycleTimer(dataset.fps, records_data=False)
    try:     
        for idx in range(dataset.num_frames):
            timer.tick()
            
            with timer.section("read_frame"):
                action = actions[idx][ACTION]
                joint_command_pub.joint_pos = action
                
            if rclpy.ok():
                with timer.section("send"):
                    joint_command_pub.callback()
                
            timer.wait()
                             
    except KeyboardInterrupt:
        pass
    
    finally:
        joint_command_pub.destroy_node()
        rclpy.shutdown()
        

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Replay LeRobot datasets on CRX")
    parser.add_argument("--repo_id", type=str, required=True, help="Repository ID")
    parser.add_argument("--root", type=str, required=True, help="Path of lerobot dataset.")
    parser.add_argument("--episode_num", type=int, default=0, help="Episode number")

    args = parser.parse_args()
    
    main(args)
