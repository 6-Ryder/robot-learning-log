"""SE(2) 参考实现。先自己写完再看。"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def rotation(theta: float) -> np.ndarray:
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


@dataclass(frozen=True)
class SE2:
    R: np.ndarray
    t: np.ndarray

    def __post_init__(self) -> None:
        if np.shape(self.R) != (2, 2):
            raise ValueError(f"R must be (2,2), got {np.shape(self.R)}")
        if np.shape(self.t) != (2,):
            raise ValueError(f"t must be (2,), got {np.shape(self.t)}")

    def compose(self, other: "SE2") -> "SE2":
        return SE2(self.R @ other.R, self.R @ other.t + self.t)

    def inverse(self) -> "SE2":
        Rt = self.R.T
        return SE2(Rt, -Rt @ self.t)

    def transform_point(self, p: np.ndarray) -> np.ndarray:
        p = np.asarray(p, dtype=float)
        if p.shape != (2,):
            raise ValueError(f"p must be (2,), got {p.shape}")
        return self.R @ p + self.t

    def as_matrix(self) -> np.ndarray:
        T = np.eye(3)
        T[:2, :2] = self.R
        T[:2, 2] = self.t
        return T

    @staticmethod
    def identity() -> "SE2":
        return SE2(np.eye(2), np.zeros(2))

    @staticmethod
    def from_pose(x: float, y: float, theta: float) -> "SE2":
        return SE2(rotation(theta), np.array([x, y], dtype=float))


def transform_points(T: SE2, points: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError(f"points must be (N,2), got {points.shape}")
    return points @ T.R.T + T.t


def chain(transforms: list[SE2]) -> SE2:
    result = SE2.identity()
    for T in transforms:
        result = result.compose(T)
    return result