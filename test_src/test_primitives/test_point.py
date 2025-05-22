import pytest
from src.primitives.point import Point2D


class TestPoint2D:

    @pytest.mark.parametrize(["points", "valid"], [((Point2D(2.0, 1.0, 2.0), Point2D(2.0, 1.0, 3.0)), True), 
                                                   ((Point2D(3.0, 3.0, None), Point2D(3.0, 3.0, None)), True),
                                                   ((Point2D(3.0, 3.0, 1.0), Point2D(3.0, 3.0, None)), False),
                                                   ((Point2D(2.0, 3.0, 1.0), Point2D(4.0, 4.0, 1.0)), False)])
    def test_equal(self, points: tuple[Point2D, Point2D], valid: bool) -> None:
        """
        """
        if valid:
            assert points[0] == points[1]
        else:
            assert points[0] != points[1]
    
    def test_add(self) -> None:
        """
        """
        p1 = Point2D(x=1.0, y=1.0, w=None)
        p2 = Point2D(x=2.0, y=2.0, w=None)
        p3 = p1 + p2
        assert p3.x == 3.0 and p3.y == 3.0

    def test_subtract(self) -> None:
        """
        """
        p1 = Point2D(x=1.0, y=1.0, w=None)
        p2 = Point2D(x=2.0, y=2.0, w=None)
        p3 = p1 - p2
        assert p3.x == -1.0 and p3.y == -1.0

    def test_true_divide(self) -> None:
        """
        """
        p1 = Point2D(x=4.0, y=4.0, w=None)
        p2 = Point2D(x=2.0, y=2.0, w=None)
        p3 = p1 / p2
        assert p3.x == 2.0 and p3.y == 2.0


if __name__ == "__main__":
    pass
    