import pytest
from unittest.mock import patch, MagicMock
import math
from numpy.testing import assert_array_equal
from src.transforms.transform_base import TransformBase2D
from src.transforms.rigid import RigidTransform2D
from src.primitives.point import Point2D
from src.primitives.rectangle import Rectangle2D


@pytest.fixture
def rigid_fix() -> RigidTransform2D:
    return RigidTransform2D(theta=0.79, tx=160, ty=20)


@pytest.fixture
def rect_fix() -> Rectangle2D:
    p1 = Point2D(1., 1., 1.)
    p2 = Point2D(2., 1., 1.)
    p3 = Point2D(2., 2., 1.)
    p4 = Point2D(1., 2., 1.)
    return Rectangle2D(p1, p2, p3, p4)


class TestRigidTransform2D:


    def test_init(self) -> None:
        """
        """
        rigid = RigidTransform2D()
        assert rigid._DoF == 3

    def test_theta_setter(self, rigid_fix: RigidTransform2D) -> None:
        """
        """
        with patch.object(rigid_fix, "update_M") as patch_update:
            rigid_fix.theta = 0.79
            patch_update.assert_called_once()

    def test_tx_setter(self, rigid_fix: RigidTransform2D) -> None:
        """
        """
        with patch.object(rigid_fix, "update_M") as patch_update:
            rigid_fix.tx = 10
            patch_update.assert_called_once()

    def test_ty_setter(self, rigid_fix: RigidTransform2D) -> None:
        """
        """
        with patch.object(rigid_fix, "update_M") as patch_update:
            rigid_fix.ty = 10
            patch_update.assert_called_once()

    @pytest.mark.parametrize("from_origin", (True, False))
    def test_apply_to_rectangle(self, rigid_fix: RigidTransform2D, rect_fix: Rectangle2D, from_origin: bool) -> None:
        """
        """
        rigid_fix.from_origin = from_origin
        with patch.object(rigid_fix, "update_M") as patch_update:
            transformed_rect = rigid_fix.apply_to_rectangle(rect_fix)
            assert transformed_rect is rect_fix
            patch_update.assert_called_once()

    def test_update_M(self, rigid_fix: RigidTransform2D) -> None:
        """
        """
        with patch.object(TransformBase2D, "reset") as patch_reset:
            rigid_fix.update_M()
            patch_reset.assert_called_once()

    def test_get_decomposed(self, rigid_fix: RigidTransform2D) -> None:
        """
        """
        rotation, translation = rigid_fix.get_decomposed()
        assert_array_equal(rotation.M, rigid_fix.rotation.M)
        assert_array_equal(translation.M, rigid_fix.translation.M)


if __name__ == "__main__":
    pass
