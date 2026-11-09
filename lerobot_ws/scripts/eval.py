import numpy as np
import cv2
import torch
import threading
import time
import argparse

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String
from sensor_msgs.msg import JointState, Image

from lerobot.policies.act.modeling_act import ACTPolicy
from lerobot.datasets.lerobot_dataset import LeRobotDataset
from lerobot.utils.constants import ACTION
from lerobot.utils.cycle_timer import CycleTimer


class JointStateSubscriber(Node):
    def __init__(self):
        super().__init__("joint_state_subscriber")

        self.joint_name = None
        self.joint_pos = None
        
        self.create_subscription(JointState, "/isaac_joint_states", self.callback, 10) 
        
    def callback(self, msg):
        self.joint_pos = torch.tensor(msg.position[:7].tolist(), dtype=torch.float32)
        # print(dir(msg.position)) # 'header', 'name', 'position', 'velocity'


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


class ImageClass:
    def __init__(self, args):
        self.images = {}
        self.image_name = args.camera_names
        self.cap = [cv2.VideoCapture(path) for path in args.camera_path]

    def get_images(self):
        for i in range(len(self.cap)):
            if self.cap[i].isOpened():
                ret, frame = self.cap[i].read()
                if ret == True:
                    frame = torch.from_numpy(frame).clone()
                    self.images[self.image_name[i]] = frame.type(torch.float32).permute(2, 0, 1)
                    
                else:
                    print("cannot get frame")
            else:
                print("cannot open capture")
    
    def shutdown(self):
        for cap in self.cap:
            cap.release()


class CameraSubscriber(Node):
    def __init__(self):
        super().__init__("camera_subscriber")
        
        self.images = {}
        
        self.top_camera_sub = self.create_subscription(
            Image,
            '/top_rgb',
            self.image_callback,
            10
        )
        self.hand_camera_sub = self.create_subscription(
            Image,
            '/hand_rgb',
            self.image_callback,
            10
        )
    
    def image_callback(self, msg):
        # ROS Image -> OpenCV image
        height = msg.height
        width = msg.width
        
        data = np.frombuffer(msg.data, dtype=np.uint8)
        data = data.reshape([height, width, 3])
        data = torch.from_numpy(data).clone()
        self.images[msg.header.frame_id] = data.type(torch.float32).permute(2, 0, 1)

    
def get_obs(joint_sub, image_sub, device):
    observations = {}
    
    if joint_sub.joint_pos is not None:
        observations["observation.state"] = joint_sub.joint_pos.unsqueeze(0).to(device)
        # print(observations["observation.state"].shape)
    
    if len(image_sub.images) != 0:
        for img_name in image_sub.images.keys():
            observations[f"observation.images.{img_name}"] = image_sub.images[img_name].unsqueeze(0).to(device)
            # print(observations[f"observation.images.{img_name}"].shape)
        
    return observations


def main(args):
    rclpy.init()
    joint_state_sub = JointStateSubscriber()
    joint_command_pub = JointCommandPublisher()
    
    if args.use_isaac:
        image_sub = CameraSubscriber()
    else:
        image_sub = ImageClass(args)
    
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(joint_state_sub)
    
    if args.use_isaac:
        executor.add_node(image_sub)
    else:
        image_thread = threading.Thread(target=image_sub.get_images)
        image_thread.start()
    
    spin_thread = threading.Thread(target=executor.spin)
    spin_thread.start()
    
    if args.policy == "act":
        policy = ACTPolicy.from_pretrained(args.ckpt_path)
        
    try:
        while rclpy.ok():  
            with (
                torch.inference_mode(), 
                torch.autocast(device_type=args.device) if args.device == "cuda" else nullcontext(),
                ):
                    
                observations = get_obs(joint_state_sub, image_sub, args.device)
                if len(observations) == 0:
                    continue
                else:
                    actions = policy.select_action(observations)
                    for i in range(len(actions)):
                        action = actions[i]
                        joint_command_pub.joint_pos = action
                        
            joint_command_pub.callback()
                    
    except KeyboardInterrupt:
        pass
    
    finally:
        executor.shutdown()
        spin_thread.join()
        joint_state_sub.destroy_node()
        joint_command_pub.destroy_node()
        if args.use_isaac:
            image_sub.destroy_node()
        else:
            image_sub.shutdown()
        rclpy.shutdown()
        

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Eval on CRX")
    parser.add_argument("--ckpt_path", type=str, default=None, help="Pytorch model checkpoint to load.")
    parser.add_argument("--policy", type=str, default=None, help="Name of policy.")
    parser.add_argument("--camera_path", type=str, nargs="*", default=["/dev/video0", "/dev/video2"], help="Path of images.")
    parser.add_argument("--camera_names", type=str, nargs="*", default=["top_image", "hand_image"], help="Name of cameras.")
    parser.add_argument("--device", type=str, default="cuda", help="device")
    parser.add_argument("--use_isaac", type=bool, default=False, help="On isaac sim")
    args = parser.parse_args()
    
    main(args)
