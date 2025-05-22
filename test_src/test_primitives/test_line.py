import pytest
from src.primitives.point import Point2D
from src.primitives.line import Line2D


class TestLine2D:

    def test_intersection_with(self) -> None:
        """
        """
        line1 = Line2D(coeffs=(1.0, -7.0, 8.0))
        line2 = Line2D(coeffs=(3.0, -4.0, 1.0))
        line3 = Line2D(coeffs=(2.0, 3.0, 3.0))
        inter = line1.intersection_with(line2)
        assert inter == Point2D(25.0, 23.0, 17.0)
        inter = line1.intersection_with(line3)
        assert inter != Point2D(25.0, 23.0, 17.0)
    
    def test_contains_point(self) -> None:
        """
        """
        point1 = Point2D(3.0, 1.0, 1.0)
        point2 = Point2D(-4.0, 5.0, 1.0)
        point3 = Point2D(2.0, 2.0, 1.0)
        line1 = Line2D(points=(point1, point2))
        contains = line1.contains_point(point1)
        assert contains
        contains = line1.contains_point(point3)
        assert not contains


if __name__ == "__main__":
    pass