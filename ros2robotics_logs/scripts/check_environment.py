"""Verify imports and the Python isolation boundary used by scripts/ros."""
import importlib
from pathlib import Path
import site
import warnings

assert not site.ENABLE_USER_SITE, "User site packages must be disabled"
for name in (
    "rclpy", "tf2_ros", "cv_bridge", "moveit", "pymoveit2", "numpy",
    "scipy", "cv2", "torch", "onnxruntime", "pytest", "debugpy",
):
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        module = importlib.import_module(name)
    origin = Path(module.__file__).resolve()
    assert Path(site.getusersitepackages()) not in origin.parents, origin
    print(f"{name}: {origin}")

import numpy as np
from scipy.linalg import solve
import cv2
from cv_bridge import CvBridge
import torch

np.testing.assert_allclose(solve(np.eye(2), np.ones(2)), np.ones(2))
image = np.zeros((2, 2, 3), dtype=np.uint8)
assert cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).shape == (2, 2)
bridge = CvBridge()
np.testing.assert_array_equal(
    bridge.imgmsg_to_cv2(bridge.cv2_to_imgmsg(image, "bgr8"), "bgr8"), image
)
assert torch.tensor([1, 2, 3]).sum().item() == 6
print("ROS Python isolation and numerical/image checks passed")
