"""SE(2) 练习骨架。

实现所有 raise NotImplementedError 的函数，直到 pytest 全绿。
不要 import scipy / pinocchio；这个练习就是手写。
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def rotation(theta: float) -> np.ndarray:
    """返回 2x2 旋转矩阵 R(theta)。"""
    raise NotImplementedError("实现 rotation")


@dataclass(frozen=True)
class SE2:
    """二维刚体变换：R 是 (2,2)，t 是 (2,)。"""

    R: np.ndarray
    t: np.ndarray

    def __post_init__(self) -> None:
        """校验 R/t 形状；不合法抛 ValueError。"""
        raise NotImplementedError("实现 __post_init__ 形状校验")

    def compose(self, other: "SE2") -> "SE2":
        """返回 self ∘ other（先 other，再 self）。"""
        raise NotImplementedError("实现 compose")

    def inverse(self) -> "SE2":
        """返回逆变换。"""
        raise NotImplementedError("实现 inverse")

    def transform_point(self, p: np.ndarray) -> np.ndarray:
        """变换一个二维点，返回 shape (2,)。"""
        raise NotImplementedError("实现 transform_point")

    def as_matrix(self) -> np.ndarray:
        """返回 3x3 齐次矩阵。"""
        raise NotImplementedError("实现 as_matrix")

    @staticmethod
    def identity() -> "SE2":
        """单位变换。"""
        raise NotImplementedError("实现 identity")

    @staticmethod
    def from_pose(x: float, y: float, theta: float) -> "SE2":
        """从 (x, y, theta) 构造。"""
        raise NotImplementedError("实现 from_pose")


def transform_points(T: SE2, points: np.ndarray) -> np.ndarray:
    """一次变换 (N,2) 个点，返回 (N,2)。必须向量化。"""
    raise NotImplementedError("实现 transform_points")


def chain(transforms: list[SE2]) -> SE2:
    """按顺序组合列表中的变换；空列表返回单位变换。"""
    raise NotImplementedError("实现 chain")