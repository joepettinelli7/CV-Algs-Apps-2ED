import pytest
from unittest.mock import patch
import math
from numpy.testing import assert_array_equal
from src.transforms.transform_base import TransformBase2D
from src.primitives.point import Point2D
from src.primitives.rectangle import Rectangle2D


@pytest.fixture
def tb_fix() -> TransformBase2D:
    return TransformBase2D()


@pytest.fixture
def rect_fix() -> Rectangle2D:
    p1 = Point2D(1., 1., 1.)
    p2 = Point2D(2., 1., 1.)
    p3 = Point2D(2., 2., 1.)
    p4 = Point2D(1., 2., 1.)
    return Rectangle2D(p1, p2, p3, p4)


class TestTransformBase2D:

    def test_init(self, tb_fix: TransformBase2D) -> None:
        """
        """
        assert tb_fix.M.dtype == float
        assert tb_fix.M.shape == (3, 3)

    def test_repr(self, tb_fix: TransformBase2D) -> None:
        """
        """
        with patch.object(tb_fix, "get_components") as patch_get:
            tb_fix.__repr__()
            patch_get.assert_called_once()

    def test_reset(self, tb_fix: TransformBase2D) -> None:
        """
        """
        tb_fix.M[0][0] = 3.0
        tb_fix.reset()
        assert tb_fix.M[0][0] == 1.0

    def test_to_degrees(self, tb_fix: TransformBase2D) -> None:
        """
        """
        radians = math.pi / 2.0
        degrees = tb_fix.to_degrees(radians)
        assert degrees == 90.0

    def test_to_radians(self, tb_fix: TransformBase2D) -> None:
        """
        """
        degrees = 90.0
        radians = tb_fix.to_radians(degrees)
        assert radians == math.pi / 2.0

    def test_get_T_inv_M(self, tb_fix: TransformBase2D) -> None:
        """
        """
        T_inv = tb_fix.get_T_inv_M()
        assert_array_equal(T_inv, tb_fix.M)

    def test_get_inv_M(self, tb_fix: TransformBase2D) -> None:
        """
        """
        inv = tb_fix.get_inv_M()
        assert_array_equal(inv, tb_fix.M)

    def test_get_decomposed(self, tb_fix: TransformBase2D) -> None:
        """
        """
        with pytest.raises(NotImplementedError):
            tb_fix.get_decomposed()

    def test_equal(self, tb_fix: TransformBase2D) -> None:
        """
        """
        other_1 = TransformBase2D()
        other_2 = TransformBase2D()
        other_2.M[0][0] += 3
        assert tb_fix == other_1
        assert tb_fix != other_2
        

if __name__ == "__main__":
    pass
    