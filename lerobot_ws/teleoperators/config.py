from dataclasses import dataclass, field
from lerobot_teleoperator_devices import KeyboardJointTeleopConfig
from isaacteleop.config_isaac_teleop import XRControllerConfig


@TeleoperatorConfig.register_subclass("crx_keyboard_joint")
@dataclass
class CRXKeyboardJointTeleopConfig(KeyboardJointTeleopConfig):
    def __post_init__(self):
        self.arm_action_keys = ["J1.pos", "J2.pos", "J3.pos", "J4.pos", "J5.pos", "J6.pos"]


@IsaacTeleopConfig.register_subclass("xr_ros_controller")
@dataclass(kw_only=True)
class XRRosControllerConfig(XRControllerConfig):
    """Config for Isaac Teleop XR (VR) controller teleoperation.

    Exposes the raw base-frame grip pose, squeeze, and trigger via ``ControllersSource``.
    No retargeters: the clutch and gripper mapping live in the owning loop.
    """
    pass