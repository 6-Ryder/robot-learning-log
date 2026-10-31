import numpy as np


def test_numpy_available() -> None:
    assert np.array([1, 2, 3]).sum() == 6


def test_package_imports() -> None:
    import r1_robomath

    assert hasattr(r1_robomath, "main")