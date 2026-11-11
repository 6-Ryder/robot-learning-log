"""Smoke checks for the learning environment, independent of exercise skeletons."""
import importlib
import sys

import numpy as np
import pinocchio as pin

for name in ("matplotlib", "scipy", "modern_robotics", "roboticstoolbox", "mujoco", "screws"):
    module = importlib.import_module(name)
    print(f"{name}: {module.__file__}")

model = pin.buildSampleModelManipulator()
q = pin.neutral(model)
mass = pin.crba(model, model.createData(), q)
assert mass.shape == (model.nv, model.nv)
assert np.isfinite(mass).all()
print(f"Pinocchio {pin.__version__}: {model.nv} DOF mass matrix OK; Python {sys.version.split()[0]}")
