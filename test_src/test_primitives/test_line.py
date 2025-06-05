import pytest
import math
from typing import Union
from src.primitives.point import Point2D
from src.primitives.line import Line2D


class TestLine2D:

    def test_init(self) -> None:
        """
        """
        p1 = Point2D()
        p2 = Point2D()
        line = Line2D(points=(p1, p2))
        # should always have a, b, c
        assert line._a is not None
        assert line._b is not None
        assert line._c is not None

    def test_polar_coords(self) -> None:
        """
        """
        line = Line2D(coeffs=(1.0, 2.0, 1.0))
        assert line.polar_coords.shape == (2, 1)

    def test_normalized_line_vector(self) -> None:
        """
        """
        line = Line2D(coeffs=(1.0, 2.0, 1.0))
        assert line.normalized_line_vector.shape == (3, 1)

    def test_normalized_normal_vector(self) -> None:
        """
        Normalized vector is defined by (cos(theta), sin(theta)). It
        should be equal to dividing (a, b) by it's magnitude (nx, ny).
        The magnitude of this normalized vector should also equal 1.
        """
        line1 = Line2D(coeffs=(1.0, 3.0, 1.0))
        norm_vec = line1.normalized_normal_vector
        assert norm_vec[0][0] == line1.nx
        assert norm_vec[1][0] == line1.ny
        mag = math.sqrt(norm_vec[0][0] ** 2 + norm_vec[1][0] ** 2)
        assert math.isclose(mag, 1.0)

    def test_nx(self) -> None:
        """
        """
        line1 = Line2D(coeffs=(1.0, 3.0, 1.0))
        assert line1.nx == math.cos(line1.theta)

    def test_ny(self) -> None:
        """
        """
        line1 = Line2D(coeffs=(1.0, 3.0, 1.0))
        assert line1.ny == math.sin(line1.theta)

    def test_magnitude(self) -> None:
        """
        """
        line1 = Line2D(coeffs=(3.0, 4.0, 1.0))
        mag = line1.magnitude
        assert mag == 5.0

    def test_theta(self) -> None:
        """
        """
        line1 = Line2D(coeffs=(3.0, 4.0, 1.0))
        assert math.isclose(round(line1.theta, 4), 0.9273)
    
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
        point3 = Point2D(2.0, 2.0, 1.0)  # change
        line1 = Line2D(points=(point1, point2))
        assert line1.contains_point(point1)
        assert not line1.contains_point(point3)

    @pytest.mark.parametrize("x", (2.0, [2.0, 3.0, 4.0]))
    def test_get_point_y_from_x(self, x: Union[float, list[float]]) -> None:
        """
        """
        line1 = Line2D(coeffs=(1.0, 1.0, 1.0))
        y = line1.get_point_y_from_x(x)
        if isinstance(x, float):
            assert y == -3.0
        else:
            assert y == [-3.0, -4.0, -5.0]
        
    @pytest.mark.parametrize("y", (2.0, [2.0, 3.0, 4.0]))
    def test_get_point_x_from_y(self, y: Union[float, list[float]]) -> None:
        """
        """
        line1 = Line2D(coeffs=(1.0, 1.0, 2.0))
        x = line1.get_point_x_from_y(y)
        if isinstance(y, float):
            assert x == -4.0
        else:
            assert x == [-4.0, -5.0, -6.0]

    @pytest.mark.parametrize(["other", "equal"], [(Line2D(coeffs=(6.0, 3.0, 1.0)), True),
                                                  (Line2D(coeffs=(5.0, 3.0, 1.0)), False),
                                                  (Line2D(coeffs=(6.0, 4.0, 1.0)), False),
                                                  (Line2D(coeffs=(6.0, 3.0, 0.0)), False)])
    def test_equal(self, other: Line2D, equal: bool) -> None:
        """
        """
        line = Line2D(coeffs=(6.0, 3.0, 1.0))
        result = line == other
        assert result == equal


if __name__ == "__main__":
    pass
    