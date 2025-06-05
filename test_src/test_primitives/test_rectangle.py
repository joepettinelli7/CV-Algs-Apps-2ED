import pytest
from src.primitives.point import Point2D
from src.primitives.rectangle import Rectangle2D


@pytest.fixture
def points_fix() -> tuple[Point2D]:
    p1 = Point2D(1.0, 1.0, 1.0)
    p2 = Point2D(3.0, 1.0, 1.0)
    p3 = Point2D(3.0, 3.0, 1.0)
    p4 = Point2D(1.0, 3.0, 1.0)
    return (p1, p2, p3, p4)


class TestRectangle2D:

    def test_corners(self, points_fix: tuple[Point2D]) -> None:
        """
        """
        p1, p2, p3, p4 = points_fix
        rect = Rectangle2D(p1, p2, p3, p4)
        assert rect.corners == points_fix

    def test_center(self, points_fix: tuple[Point2D]) -> None:
        """
        """
        p1, p2, p3, p4 = points_fix
        rect = Rectangle2D(p1, p2, p3, p4)
        assert rect.center == Point2D(2.0, 2.0, 1.0)
        p1.x, p1.y, p1.w = 2.0, 2.0, 2.0
        rect = Rectangle2D(p1, p2, p3, p4)
        assert rect.center == Point2D(2.0, 2.0, 1.0)

    def test_get_item(self, points_fix: tuple[Point2D]) -> None:
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

    def test_set_item(self, points_fix: tuple[Point2D]) -> None:
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


if __name__ == "__main__":
    pass
    