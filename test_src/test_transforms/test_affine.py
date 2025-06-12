import pytest
from unittest.mock import patch
from numpy.testing import assert_allclose
from src.transforms.transform_base import TransformBase2D
from src.transforms.affine import AffineTransform2D
from src.primitives.rectangle import Rectangle2D
from src.primitives.point import Point2D


@pytest.fixture
def aff_fix() -> AffineTransform2D:
    return AffineTransform2D(sx=2.0, sy=2.0, shear_theta=0.39, theta=0.79, tx=160, ty=20)


@pytest.fixture
def rect_fix() -> Rectangle2D:
    p1 = Point2D(1., 1., 1.)
    p2 = Point2D(2., 1., 1.)
    p3 = Point2D(2., 2., 1.)
    p4 = Point2D(1., 2., 1.)
    return Rectangle2D(p1, p2, p3, p4)


class TestAffineTransform2D:
    
    def test_init(self, aff_fix: AffineTransform2D) -> None:
        """
        """
        assert aff_fix._DoF == 5 or 6 or 7

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

    @pytest.mark.parametrize("from_origin", (True, False))
    def test_apply_to_rectangle(self, aff_fix: AffineTransform2D, rect_fix: Rectangle2D, from_origin: bool) -> None:
        """
        """
        aff_fix.from_origin = from_origin
        with patch.object(aff_fix, "update_M") as patch_update:
            transformed_rect = aff_fix.apply_to_rectangle(rect_fix)
            assert transformed_rect is rect_fix
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
        
        
if __name__ == "__main__":
    pass
    