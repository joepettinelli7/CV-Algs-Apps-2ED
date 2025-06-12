import pytest
from unittest.mock import patch
from numpy.testing import assert_array_equal
from src.transforms.transform_base import TransformBase2D
from src.transforms.similarity import SimilarityTransform2D
from src.primitives.rectangle import Rectangle2D
from src.primitives.point import Point2D


@pytest.fixture
def sim_fix() -> SimilarityTransform2D:
    return SimilarityTransform2D(sx=2.0, sy=2.0, theta=0.79, tx=160, ty=20)


@pytest.fixture
def rect_fix() -> Rectangle2D:
    p1 = Point2D(1., 1., 1.)
    p2 = Point2D(2., 1., 1.)
    p3 = Point2D(2., 2., 1.)
    p4 = Point2D(1., 2., 1.)
    return Rectangle2D(p1, p2, p3, p4)


class TestSimilarityTransform2D:
    
    @pytest.mark.parametrize("sx", (2.0, 3.0))
    def test_init(self, sx: float) -> None:
        """
        """
        if sx == 2.0:
            sim = SimilarityTransform2D(sx=sx, sy=2.0)
            assert sim._DoF == 4
        else:
            with pytest.raises(AssertionError):
                sim = SimilarityTransform2D(sx=sx, sy=2.0)

    def test_sx_setter(self, sim_fix: SimilarityTransform2D) -> None:
        """
        """
        with patch.object(sim_fix, "update_M") as patch_update:
            sim_fix.sx = 2.0
            patch_update.assert_called_once()

    def test_sy_setter(self, sim_fix: SimilarityTransform2D) -> None:
        """
        """
        with patch.object(sim_fix, "update_M") as patch_update:
            sim_fix.sy = 2.0
            patch_update.assert_called_once()

    def test_theta_setter(self, sim_fix: SimilarityTransform2D) -> None:
        """
        """
        with patch.object(sim_fix, "update_M") as patch_update:
            sim_fix.theta = 0.79
            patch_update.assert_called_once()

    def test_tx_setter(self, sim_fix: SimilarityTransform2D) -> None:
        """
        """
        with patch.object(sim_fix, "update_M") as patch_update:
            sim_fix.tx = 10
            patch_update.assert_called_once()

    def test_ty_setter(self, sim_fix: SimilarityTransform2D) -> None:
        """
        """
        with patch.object(sim_fix, "update_M") as patch_update:
            sim_fix.ty = 10
            patch_update.assert_called_once()

    @pytest.mark.parametrize("from_origin", (True, False))
    def test_apply_to_rectangle(self, sim_fix: SimilarityTransform2D, rect_fix: Rectangle2D, from_origin: bool) -> None:
        """
        """
        sim_fix.from_origin = from_origin
        with patch.object(sim_fix, "update_M") as patch_update:
            transformed_rect = sim_fix.apply_to_rectangle(rect_fix)
            assert transformed_rect is rect_fix
            patch_update.assert_called_once()

    def test_update_M(self, sim_fix: SimilarityTransform2D) -> None:
        """
        """
        with patch.object(TransformBase2D, "reset") as patch_reset:
            sim_fix.update_M()
            patch_reset.assert_called_once()

    def test_get_decomposed(self, sim_fix: SimilarityTransform2D) -> None:
        """
        """
        scale, rigid = sim_fix.get_decomposed()
        assert_array_equal(scale.M, sim_fix.scale.M)
        assert_array_equal(rigid.M, sim_fix.rigid.M)
        
        
if __name__ == "__main__":
    pass
    