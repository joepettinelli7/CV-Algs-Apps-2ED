import pytest
from src.primitives.point import Point2D
from src.primitives_lists.points import Points2D


class TestPoints2D:

    def test_subtract(self) -> None:
        """
        """
        p1 = Point2D(x=5.0, y=4.0, w=None)
        p2 = Point2D(x=3.0, y=2.0, w=None)
        points2d = Points2D([p1, p2])
        p3 = Point2D(x=1.0, y=1.0, w=None)
        points2d - p3
        assert points2d.points[0].x == 4.0
        assert points2d.points[0].y == 3.0
        assert points2d.points[1].x == 2.0
        assert points2d.points[1].y == 1.0
        

if __name__ == "__main__":
    pass
    