from typing import Union
import pytest
from src.primitives.point import Point2D


class TestPoint2D:

    def test_vector(self) -> None:
        """
        """
        p = Point2D(2.0, 2.0, 1.0)
        assert p.vector.shape == (3, 1)

    def test_cartesian_vector(self) -> None:
        """
        """
        p = Point2D(2.0, 2.0, 1.0)
        assert p.cartesian_vector.shape == (2, 1)

    @pytest.mark.parametrize(["w", "expected"], [(2, Point2D(2.0, 2.0, 2.0)), (2.0, Point2D(2.0, 2.0, 2.0))])
    def test_homogenize(self, w: Union[int, float], expected: Point2D) -> None:
        """
        """
        p = Point2D(1.0, 1.0, 1.0)
        p.homogenize(w)
        assert p.x == expected.x and p.y == expected.y and p.w == expected.w
    
    @pytest.mark.parametrize(["point", "expected"], [(Point2D(4.0, 4.0, 2.0), Point2D(2.0, 2.0, 1.0)), 
                                                     (Point2D(4.0, 2.0, 0.0), Point2D(4.0, 2.0, 0.0))])
    def test_normalize(self, point: Point2D, expected: Point2D) -> None:
        """
        """
        point.normalize()
        assert point.x == expected.x
        assert point.y == expected.y
        assert point.w == expected.w

    @pytest.mark.parametrize(["point", "expected"], [(Point2D(4.0, 4.0, 2.0), Point2D(2.0, 2.0, 1.0)), 
                                                     (Point2D(4.0, 2.0, 0.0), None)])
    def test_normalized(self, point: Point2D, expected: Point2D) -> None:
        """
        """
        p2 = point.normalized()
        if point.w != 0.0:
            assert p2.x == expected.x
            assert p2.y == expected.y
            assert p2.w == expected.w
        else:
            assert p2 is None

    @pytest.mark.parametrize(["points", "equal"], [((Point2D(4.0, 2.0, 2.0), Point2D(2.0, 1.0, 1.0)), True),
                                                   ((Point2D(4.0, 2.0, 1.0), Point2D(2.0, 1.0, 1.0)), False),
                                                   ((Point2D(4.0, 3.0, 1.0), Point2D(4.0, 3.0, 1.0)), True),
                                                   ((Point2D(4.0, 3.0, 0.0), Point2D(4.0, 3.0, 0.0)), True),
                                                   ((Point2D(5.0, 3.0, 0.0), Point2D(4.0, 3.0, 0.0)), False)])
    def test_equal(self, points: tuple[Point2D, Point2D], equal: bool) -> None:
        """
        """
        if equal:
            assert points[0] == points[1]
        else:
            assert points[0] != points[1]

    @pytest.mark.parametrize(["points", "expected"], [((Point2D(4.0, 2.0, 1.0), Point2D(2.0, 1.0, 0.0)), Point2D(6.0, 3.0, 1.0)),
                                                      ((Point2D(4.0, 3.0, 0.0), Point2D(1.0, 1.0, 0.0)), Point2D(5.0, 4.0, 0.0)),
                                                      ((Point2D(6.0, 6.0, 2.0), Point2D(1.0, 1.0, 1.0)), Point2D(4.0, 4.0, 1.0))])
    def test_add(self, points: tuple[Point2D, Point2D], expected: Point2D) -> None:
        """
        """
        sum_point = points[0] + points[1]
        assert sum_point.x == expected.x
        assert sum_point.y == expected.y
        assert sum_point.w == expected.w

    @pytest.mark.parametrize(["points", "expected"], [((Point2D(4.0, 2.0, 1.0), Point2D(2.0, 1.0, 0.0)), Point2D(6.0, 3.0, 1.0)),
                                                      ((Point2D(4.0, 3.0, 0.0), Point2D(1.0, 1.0, 0.0)), Point2D(5.0, 4.0, 0.0))])
    def test_inplace_add(self, points: tuple[Point2D, Point2D], expected: Point2D) -> None:
        """
        """
        p1 = points[0]
        p2 = points[1]
        p1 += p2
        assert p1.x == expected.x
        assert p1.y == expected.y
        assert p1.w == expected.w

    @pytest.mark.parametrize(["points", "expected"], [((Point2D(4.0, 4.0, 1.0), Point2D(2.0, 2.0, 1.0)), Point2D(2.0, 2.0, 0.0)),
                                                      ((Point2D(4.0, 2.0, 1.0), Point2D(2.0, 1.0, 0.0)), Point2D(2.0, 1.0, 1.0)),
                                                      ((Point2D(4.0, 3.0, 0.0), Point2D(1.0, 1.0, 0.0)), Point2D(3.0, 2.0, 0.0))])
    def test_subtract(self, points: tuple[Point2D, Point2D], expected: Point2D) -> None:
        """
        """
        diff_point = points[0] - points[1]
        assert diff_point.x == expected.x
        assert diff_point.y == expected.y
        assert diff_point.w == expected.w

    @pytest.mark.parametrize(["points", "expected"], [((Point2D(4.0, 4.0, 1.0), Point2D(2.0, 2.0, 1.0)), Point2D(2.0, 2.0, 0.0)),
                                                      ((Point2D(4.0, 2.0, 1.0), Point2D(2.0, 1.0, 0.0)), Point2D(2.0, 1.0, 1.0)),
                                                      ((Point2D(4.0, 3.0, 0.0), Point2D(1.0, 1.0, 0.0)), Point2D(3.0, 2.0, 0.0))])
    def test_inplace_subtract(self, points: tuple[Point2D, Point2D], expected: Point2D) -> None:
        """
        """
        p1 = points[0]
        p2 = points[1]
        p1 -= p2
        assert p1.x == expected.x
        assert p1.y == expected.y
        assert p1.w == expected.w
        

if __name__ == "__main__":
    pass
    