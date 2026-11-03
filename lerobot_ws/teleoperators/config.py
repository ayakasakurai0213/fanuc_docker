from dataclasses import dataclass, field
from lerobot.teleoperators import TeleoperatorConfig
from lerobot_teleoperator_devices import KeyboardJointTeleopConfig

import sys
from pathlib import Path
ISAAC_TELEOP_PATH = str(Path(__file__).parent.parent) + "/" + str(Path("lerobot/examples/isaac_teleop_to_so101"))
sys.path.append(ISAAC_TELEOP_PATH)

from isaac_teleop.config_isaac_teleop import XRControllerConfig


@TeleoperatorConfig.register_subclass("crx_keyboard_joint")
@dataclass
class CRXKeyboardJointTeleopConfig(KeyboardJointTeleopConfig):
    def __post_init__(self):
        self.arm_action_keys = ["J1.pos", "J2.pos", "J3.pos", "J4.pos", "J5.pos", "J6.pos"]


@TeleoperatorConfig.register_subclass("xr_ros_controller")
@dataclass
class XRROSControllerConfig(XRControllerConfig):
    """Config for Isaac Teleop XR (VR) controller teleoperation.

    Exposes the raw base-frame grip pose, squeeze, and trigger via ``ControllersSource``.
    No retargeters: the clutch and gripper mapping live in the owning loop.
    """
    pass