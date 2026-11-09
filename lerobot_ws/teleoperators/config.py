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


_DEFAULT_BASE_T_ANCHOR: list[list[float]] = [
    [0.0, 0.0, -1.0, 0.0],
    [-1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1.0],
]

@TeleoperatorConfig.register_subclass("xr_ros_controller")
@dataclass
class XRROSControllerConfig(TeleoperatorConfig):
    """Config for Isaac Teleop XR (VR) controller teleoperation.

    Exposes the raw base-frame grip pose, squeeze, and trigger via ``ControllersSource``.
    No retargeters: the clutch and gripper mapping live in the owning loop.
    """

    app_name: str = "LeTeleop"
    """Application name for the OpenXR / Isaac Teleop session."""

    auto_launch_cloudxr: bool = True
    """Auto-launch the CloudXR runtime on :meth:`connect`. Set ``False`` (or export
    ``LEROBOT_CLOUDXR_SKIP_AUTOLAUNCH=1``, which wins) when CloudXR runs externally.
    """

    cloudxr_env_file: str | None = None
    """Optional CloudXR device-profile ``.env`` (an INPUT profile selecting the headset
    transport) passed to ``CloudXRLauncher``. ``None`` keeps the default auto-WebRTC profile.
    """

    hand_side: str = "right"
    """Which controller hand to use: ``"left"`` or ``"right"``. A plain ``str`` (validated in
    ``__post_init__``) because draccus cannot decode ``Literal``-typed fields from the CLI."""

    clutch_threshold: float = 0.5
    """Squeeze value above which the owning loop's clutch engages (held-to-enable). The
    device reports only the raw squeeze; the threshold is applied by the loop."""

    base_T_anchor: list[list[float]] = field(  # noqa: N815  (frameA_T_frameB transform-matrix convention)
        # Fresh copy per instance: returning the module-level list itself would alias one
        # mutable matrix across every config.
        default_factory=lambda: [row.copy() for row in _DEFAULT_BASE_T_ANCHOR]
    )
    """Static 4x4 [row-major] transform rebasing the OpenXR controller anchor frame into
    the robot base frame. Defaults to OpenXR (X=Right, Y=Up, Z=Backward) -> robot
    (X=Forward, Y=Left, Z=Up). Plain nested lists so the config stays serializable.
    """

    def __post_init__(self):
        if self.hand_side not in ("left", "right"):
            raise ValueError(f"hand_side must be 'left' or 'right', got {self.hand_side!r}")