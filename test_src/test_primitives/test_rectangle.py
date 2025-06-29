from typing import List
import pytest
from unittest.mock import patch
import math
from numpy.testing import assert_allclose
from src.primitives.point import Point2D
from src.primitives_lists.points import Points2D
from src.primitives.rectangle import Rectangle2D
from src.transforms.rotation import RotationTransform2D


@pytest.fixture
def points_fix() -> List[Point2D]:
    p1 = Point2D(100.0, 100.0, 1.0)
    p2 = Point2D(300.0, 100.0, 1.0)
    p3 = Point2D(300.0, 300.0, 1.0)
    p4 = Point2D(100.0, 300.0, 1.0)
    return [p1, p2, p3, p4]


class TestRectangle2D:

    def test_get_width(self, points_fix: List[Point2D]) -> None:
        """
        """
        rect = Rectangle2D(*points_fix)
        assert rect.width == 200

    def test_get_height(self, points_fix: List[Point2D]) -> None:
        """
        """
        rect = Rectangle2D(*points_fix)
        assert rect.height == 200

    def test_corners(self, points_fix: List[Point2D]) -> None:
        """
        """
        rect = Rectangle2D(*points_fix)
        assert rect.corners == Points2D(points_fix)
        rect.left_top = Point2D(1.0, 1.0, 1.0)
        assert rect.corners != Points2D(points_fix)
    
    def test_center(self, points_fix: List[Point2D]) -> None:
        """
        """
        p1, p2, p3, p4 = points_fix
        rect = Rectangle2D(p1, p2, p3, p4)
        assert rect.center == Point2D(200.0, 200.0, 1.0)
    
    def test_copy(self, points_fix: List[Point2D]) -> None:
        """
        """
        rect = Rectangle2D(*points_fix)
        rect_copy = rect.copy()
        new_point = Point2D(0.5, 0.5, 1.0)
        assert rect.left_top != new_point
        rect.left_top = new_point
        assert rect_copy.left_top != new_point

    @pytest.mark.parametrize(["inplace", "from_origin"], [(True, False), (False, True)])
    def test_apply_transform(self, points_fix: List[Point2D], inplace: bool, from_origin: bool) -> None:
        """
        """
        rect = Rectangle2D(*points_fix)
        t = RotationTransform2D(theta=math.pi / 2)
        t.from_origin = from_origin
        new_rect = rect.apply_transform(t, inplace=inplace)
        if inplace and not from_origin:
            assert new_rect is rect
            # square rectangle rotated around its center
            # at 90 degree rotation will make equal rect
            assert new_rect == rect
        else:
            assert new_rect is not rect
            # rotation will be around the origin
            assert new_rect != rect
            assert new_rect.center != rect.center
    
    def test_get_transform_from_center(self, points_fix: List[Point2D]) -> None:
        """
        """
        rect = Rectangle2D(*points_fix)
        t = RotationTransform2D(theta=math.pi / 2)
        t = rect.get_transform_from_center(t.M)
        expected = [[6.123234e-17, -1.0, 400.0],
                    [1.0, 6.123234e-17, 0.0],
                    [0.0, 0.0, 1.0]]
        assert_allclose(t, expected)
    
    def test_get_item(self, points_fix: List[Point2D]) -> None:
        """
        """
        p1, p2, p3, p4 = points_fix
        rect = Rectangle2D(p1, p2, p3, p4)
        assert rect[0] == p1
        assert rect[1] == p2
        assert rect[2] == p3
        assert rect[3] == p4
        with pytest.raises(IndexError):
            rect[4]

    def test_set_item(self, points_fix: List[Point2D]) -> None:
        """
        """
        p1, p2, p3, p4 = points_fix
        rect = Rectangle2D(p1, p2, p3, p4)
        # Now scramble points
        rect[0] = p4
        rect[1] = p3
        rect[2] = p2
        rect[3] = p1
        assert rect.left_top == p4
        assert rect.right_top == p3
        assert rect.right_bottom == p2
        assert rect.left_bottom == p1
        with pytest.raises(IndexError):
            rect[4] = p4

    def test_equal(self, points_fix: List[Point2D]) -> None:
        """
        """
        rect = Rectangle2D(*points_fix)
        new_rect = Rectangle2D(*points_fix)
        assert rect == new_rect
        rect.left_top = rect.left_top - Point2D(1.0, 1.0, 1.0)
        assert rect != new_rect
        

if __name__ == "__main__":
    pass
    