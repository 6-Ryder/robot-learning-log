import math

import numpy as np
import pytest

from se2 import SE2, chain, rotation, transform_points


def test_rotation_90() -> None:
    R = rotation(math.pi / 2)
    assert R == pytest.approx(np.array([[0.0, -1.0], [1.0, 0.0]]), abs=1e-12)


def test_rotation_is_orthonormal() -> None:
    R = rotation(0.7)
    assert R.T @ R == pytest.approx(np.eye(2), abs=1e-12)
    assert np.linalg.det(R) == pytest.approx(1.0, abs=1e-12)


def test_identity() -> None:
    T = SE2.identity()
    assert T.R == pytest.approx(np.eye(2))
    assert T.t == pytest.approx(np.zeros(2))
    assert T.transform_point(np.array([2.0, 3.0])) == pytest.approx([2.0, 3.0])


def test_compose_translation() -> None:
    T1 = SE2.from_pose(1.0, 0.0, 0.0)
    T2 = SE2.from_pose(0.0, 2.0, 0.0)
    T = T1.compose(T2)
    assert T.t == pytest.approx([1.0, 2.0])
    assert T.R == pytest.approx(np.eye(2))


def test_compose_rotation_translation() -> None:
    T1 = SE2.from_pose(1.0, 0.0, math.pi / 2)
    T2 = SE2.from_pose(0.0, 1.0, 0.0)
    T = T1.compose(T2)
    assert T.t == pytest.approx([0.0, 0.0], abs=1e-12)
    assert T.R == pytest.approx(rotation(math.pi / 2))


def test_inverse_compose_is_identity() -> None:
    T = SE2.from_pose(1.0, 2.0, 0.7)
    assert T.compose(T.inverse()).as_matrix() == pytest.approx(np.eye(3), abs=1e-12)


def test_inverse_maps_back() -> None:
    T = SE2.from_pose(1.0, 2.0, 0.7)
    p = np.array([0.3, -0.4])
    q = T.transform_point(p)
    assert T.inverse().transform_point(q) == pytest.approx(p, abs=1e-12)


def test_transform_point() -> None:
    T = SE2.from_pose(1.0, 0.0, math.pi / 2)
    assert T.transform_point(np.array([1.0, 0.0])) == pytest.approx([1.0, 1.0], abs=1e-12)


def test_transform_points_vectorized() -> None:
    T = SE2.from_pose(1.0, 0.0, math.pi / 2)
    points = np.array([[1.0, 0.0], [0.0, 1.0]])
    expected = np.array([[1.0, 1.0], [0.0, 0.0]])
    assert transform_points(T, points) == pytest.approx(expected, abs=1e-12)


def test_chain() -> None:
    T1 = SE2.from_pose(1.0, 0.0, 0.2)
    T2 = SE2.from_pose(0.0, 1.0, -0.3)
    assert chain([T1, T2]).as_matrix() == pytest.approx(T1.compose(T2).as_matrix())


def test_chain_empty_is_identity() -> None:
    assert chain([]).as_matrix() == pytest.approx(np.eye(3))


def test_as_matrix() -> None:
    T = SE2.from_pose(1.0, 2.0, 0.0)
    assert T.as_matrix() == pytest.approx(
        np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 2.0], [0.0, 0.0, 1.0]])
    )


def test_invalid_shapes() -> None:
    with pytest.raises(ValueError):
        SE2(np.eye(3), np.zeros(2))
    with pytest.raises(ValueError):
        SE2(np.eye(2), np.zeros(3))
    T = SE2.identity()
    with pytest.raises(ValueError):
        T.transform_point(np.zeros(3))
    with pytest.raises(ValueError):
        transform_points(T, np.zeros((2, 3)))