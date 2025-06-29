import pytest
from unittest.mock import patch, MagicMock
import math
from numpy.testing import assert_array_equal
from src.transforms.transform_base import TransformBase2D
from src.transforms.rigid import RigidTransform2D
from src.primitives.point import Point2D


@pytest.fixture
def rigid_fix() -> RigidTransform2D:
    return RigidTransform2D(theta=0.79, tx=160, ty=20)


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
        assert_array_equal(translation.M @ rotation.M, rigid_fix.M)


if __name__ == "__main__":
    pass
