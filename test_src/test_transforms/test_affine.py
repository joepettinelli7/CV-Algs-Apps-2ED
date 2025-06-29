import pytest
from unittest.mock import patch
from numpy.testing import assert_allclose
from src.transforms.transform_base import TransformBase2D
from src.transforms.affine import AffineTransform2D
from src.primitives.point import Point2D


@pytest.fixture
def aff_fix() -> AffineTransform2D:
    return AffineTransform2D(sx=2.0, sy=2.0, shear_theta=0.39, theta=0.79, tx=160, ty=20)


class TestAffineTransform2D:
    
    def test_init(self, aff_fix: AffineTransform2D) -> None:
        """
        """
        assert aff_fix._DoF == 5 or 6

    def test_sx_setter(self, aff_fix: AffineTransform2D) -> None:
        """
        """
        with patch.object(aff_fix, "update_M") as patch_update:
            aff_fix.sx = 2.0
            patch_update.assert_called_once()

    def test_sy_setter(self, aff_fix: AffineTransform2D) -> None:
        """
        """
        with patch.object(aff_fix, "update_M") as patch_update:
            aff_fix.sy = 2.0
            patch_update.assert_called_once()

    def test_shear_theta_setter(self, aff_fix: AffineTransform2D) -> None:
        """
        """
        with patch.object(aff_fix, "update_M") as patch_update:
            aff_fix.shear_theta = 0.79
            patch_update.assert_called_once()

    def test_theta_setter(self, aff_fix: AffineTransform2D) -> None:
        """
        """
        with patch.object(aff_fix, "update_M") as patch_update:
            aff_fix.theta = 0.79
            patch_update.assert_called_once()

    def test_tx_setter(self, aff_fix: AffineTransform2D) -> None:
        """
        """
        with patch.object(aff_fix, "update_M") as patch_update:
            aff_fix.tx = 10
            patch_update.assert_called_once()

    def test_ty_setter(self, aff_fix: AffineTransform2D) -> None:
        """
        """
        with patch.object(aff_fix, "update_M") as patch_update:
            aff_fix.ty = 10
            patch_update.assert_called_once()

    def test_update_M(self, aff_fix: AffineTransform2D) -> None:
        """
        """
        with patch.object(TransformBase2D, "reset") as patch_reset:
            aff_fix.update_M()
            patch_reset.assert_called_once()

    def test_get_decomposed(self, aff_fix: AffineTransform2D) -> None:
        """
        """
        shear, scale, rigid = aff_fix.get_decomposed()
        assert_allclose(shear.M, aff_fix.shear.M)
        assert_allclose(scale.M, aff_fix.scale.M)
        assert_allclose(rigid.M, aff_fix.rigid.M)
        assert_allclose(rigid.M @ scale.M @ shear.M, aff_fix.M)
        
        
if __name__ == "__main__":
    pass
    