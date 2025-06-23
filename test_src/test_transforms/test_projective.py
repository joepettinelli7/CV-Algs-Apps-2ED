import pytest
from unittest.mock import patch
from numpy.testing import assert_allclose
from src.transforms.transform_base import TransformBase2D
from src.transforms.projective import ProjectiveTransform2D
from src.primitives.rectangle import Rectangle2D
from src.primitives.point import Point2D


@pytest.fixture
def proj_fix() -> ProjectiveTransform2D:
    return ProjectiveTransform2D(per_x=0.01, per_y=0.01, sx=2.0, sy=2.0,
                                 shear_theta=0.39, theta=0.79, tx=160, ty=20)


@pytest.fixture
def rect_fix() -> Rectangle2D:
    p1 = Point2D(1., 1., 1.)
    p2 = Point2D(2., 1., 1.)
    p3 = Point2D(2., 2., 1.)
    p4 = Point2D(1., 2., 1.)
    return Rectangle2D(p1, p2, p3, p4)


class TestProjectiveTransform2D:
    
    def test_init(self, proj_fix: ProjectiveTransform2D) -> None:
        """
        """
        assert proj_fix._DoF == 6 or 7

    def test_per_x_setter(self, proj_fix: ProjectiveTransform2D) -> None:
        """
        """
        with patch.object(proj_fix, "update_M") as patch_update:
            proj_fix.per_x = 0.01
            patch_update.assert_called_once()
            
    def test_per_y_setter(self, proj_fix: ProjectiveTransform2D) -> None:
        """
        """
        with patch.object(proj_fix, "update_M") as patch_update:
            proj_fix.per_y = 0.01
            patch_update.assert_called_once()

    def test_sx_setter(self, proj_fix: ProjectiveTransform2D) -> None:
        """
        """
        with patch.object(proj_fix, "update_M") as patch_update:
            proj_fix.sx = 2.0
            patch_update.assert_called_once()

    def test_sy_setter(self, proj_fix: ProjectiveTransform2D) -> None:
        """
        """
        with patch.object(proj_fix, "update_M") as patch_update:
            proj_fix.sy = 2.0
            patch_update.assert_called_once()

    def test_shear_theta_setter(self, proj_fix: ProjectiveTransform2D) -> None:
        """
        """
        with patch.object(proj_fix, "update_M") as patch_update:
            proj_fix.shear_theta = 0.79
            patch_update.assert_called_once()

    def test_theta_setter(self, proj_fix: ProjectiveTransform2D) -> None:
        """
        """
        with patch.object(proj_fix, "update_M") as patch_update:
            proj_fix.theta = 0.79
            patch_update.assert_called_once()

    def test_tx_setter(self, proj_fix: ProjectiveTransform2D) -> None:
        """
        """
        with patch.object(proj_fix, "update_M") as patch_update:
            proj_fix.tx = 10
            patch_update.assert_called_once()

    def test_ty_setter(self, proj_fix: ProjectiveTransform2D) -> None:
        """
        """
        with patch.object(proj_fix, "update_M") as patch_update:
            proj_fix.ty = 10
            patch_update.assert_called_once()

    def test_update_M(self, proj_fix: ProjectiveTransform2D) -> None:
        """
        """
        with patch.object(TransformBase2D, "reset") as patch_reset:
            proj_fix.update_M()
            patch_reset.assert_called_once()
    
    def test_get_decomposed(self, proj_fix: ProjectiveTransform2D) -> None:
        """
        """
        affine, perspective = proj_fix.get_decomposed()
        assert_allclose(affine.M, proj_fix.affine.M)
        # Allow some error because this is an optimization problem.
        assert_allclose(perspective.M, proj_fix.perspective.M, rtol=1e-4, atol=1e-7)
        assert_allclose(perspective.M @ affine.M, proj_fix.M, rtol=1e-3, atol=1e-7)
        
        
if __name__ == "__main__":
    pass
    