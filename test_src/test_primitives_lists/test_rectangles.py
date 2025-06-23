import pytest
from numpy.testing import assert_allclose
from src.transforms.affine import AffineTransform2D
from src.transforms.projective import ProjectiveTransform2D
from src.transforms.transform_base import TransformBase2D
from src.primitives.rectangle import Rectangle2D
from src.primitives_lists.rectangles import Rectangles2D
from src.primitives.point import Point2D


@pytest.fixture
def aff_fix() -> AffineTransform2D:
    return AffineTransform2D(sx=2.0, sy=2.0, shear_theta=0.39, theta=0.79, tx=160, ty=20)


@pytest.fixture
def proj_fix() -> ProjectiveTransform2D:
    return ProjectiveTransform2D(per_x=0.01, per_y=0.01, sx=2.0, sy=2.0, shear_theta=0.39, theta=0.79, tx=160, ty=20)


@pytest.fixture
def rect_fix() -> Rectangle2D:
    p1 = Point2D(10., 10., 1.)
    p2 = Point2D(20., 10., 1.)
    p3 = Point2D(20., 20., 1.)
    p4 = Point2D(10., 20., 1.)
    return Rectangle2D(p1, p2, p3, p4)


class TestRectangles2D:

    @pytest.mark.parametrize("transform", ("aff_fix", "proj_fix"))
    def test_calculate_transforms1(self, transform: TransformBase2D, rect_fix: Rectangle2D, request) -> None:
        """
        Test the transforms.
        """
        transform = request.getfixturevalue(transform)
        transform.from_origin = True
        new_rect = rect_fix.apply_transform(transform)
        rects2d = Rectangles2D([rect_fix, new_rect])
        point_calc_trans = rects2d.calculate_transforms(transform)
        assert point_calc_trans.from_origin
        assert_allclose(transform.normalized_M, point_calc_trans.normalized_M, atol=1e-2)
        point_calc_trans.normalize_M()  # Only changes transform when projective transform.
        test_rect = rect_fix.apply_transform(point_calc_trans)
        assert new_rect.to_int() == test_rect.to_int()
        
    @pytest.mark.parametrize("from_origin", (True, False))
    def test_calculate_transforms2(self, aff_fix: AffineTransform2D, rect_fix: Rectangle2D, from_origin: bool) -> None:
        """
        Test from origin using affine transform.
        """
        aff_fix.from_origin = from_origin
        new_rect = rect_fix.apply_transform(aff_fix)
        rects2d = Rectangles2D([rect_fix, new_rect])
        point_calc_aff = rects2d.calculate_transforms(aff_fix)
        assert point_calc_aff.from_origin
        test_rect = rect_fix.apply_transform(point_calc_aff)
        if from_origin:
            # The matrices should be equal
            assert_allclose(aff_fix.M, point_calc_aff.M)
        else:
            # The matrices should not be equal. Only rects are.
            with pytest.raises(AssertionError):
                assert_allclose(aff_fix.M, point_calc_aff.M)
        # Rects are always equal as long as point_calc_aff.from_origin is True
        assert new_rect == test_rect
        
    
if __name__ == "__main__":
    pass
    