import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
from sensor_msgs.msg import JointState


class ServoToJointBridge(Node):
    def __init__(self):
        super().__init__("servo_to_joint_bridge")
        
        self.gripper_msg = None

        self.subscription = self.create_subscription(
            JointTrajectory,
            "/servo_controller/joint_trajectory",
            self.trajectory_callback,
            10
        )
        
        self.subscript_gripper = self.create_subscription(
            JointTrajectory,
            "/gripper_controller/joint_trajectory", 
            self.get_gripper_action, 
            10
        )

        self.publisher = self.create_publisher(
            JointState,
            "/isaac_joint_commands",
            10
        )

        self.get_logger().info("ServoToIsaacBridge started.")

    def trajectory_callback(self, msg):
        if not msg.points:
            return

        point = msg.points[0]

        if len(msg.joint_names) != len(point.positions):
            self.get_logger().error(
                "Joint names and positions length mismatch."
            )
            return

        # JointStateに変換
        command = JointState()

        command.header.stamp = self.get_clock().now().to_msg()
        
        if self.gripper_msg is not None:
            command.name = list(msg.joint_names + self.gripper_msg.joint_names)
            command.position = list(point.positions + self.gripper_msg.points[0].positions)

            # Isaac Simへ送信
            self.publisher.publish(command)
            print(command)
    
    def get_gripper_action(self, msg):
        self.gripper_msg = msg


def main(args=None):
    rclpy.init(args=args)
    node = ServoToJointBridge()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
