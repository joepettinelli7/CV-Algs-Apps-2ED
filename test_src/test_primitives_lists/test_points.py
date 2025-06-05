import pytest
from numpy.testing import assert_array_equal
import numpy as np
from src.primitives.point import Point2D
from src.primitives.line import Line2D
from src.primitives_lists.points import Points2D


@pytest.fixture
def points_fix() -> Points2D:
    p1 = Point2D(1.0, 1.0, 1.0)
    p2 = Point2D(3.0, 1.0, 1.0)
    p3 = Point2D(3.0, 3.0, 1.0)
    p4 = Point2D(1.0, 3.0, 1.0)
    return Points2D([p1, p2, p3, p4])


class TestPoints2D:


    def test_num_points(self, points_fix: Points2D) -> None:
        """
        """
        assert points_fix.num_points == 4

    def test_array_form(self, points_fix: Points2D) -> None:
        """
        """
        expected = np.array([[1., 1., 1.],
                             [3., 1., 1.],
                             [3., 3., 1.],
                             [1., 3., 1.]
                   ])
        assert_array_equal(points_fix.array_form, expected)

    def test_centroid(self, points_fix: Points2D) -> None:
        """
        """
        assert_array_equal(points_fix.centroid, np.array([2., 2., 1.]))

    def test_append(self, points_fix: Points2D) -> None:
        """
        """
        original_len = len(points_fix._points)
        points_fix.append(Point2D())
        new_len = len(points_fix._points)
        assert new_len == original_len + 1

    def test_calculate_fit_line(self, points_fix: Points2D) -> None:
        """
        """
        fit_line = points_fix.calculate_fit_line()
        assert fit_line == Line2D(coeffs=(0., 1., -2.))

    def test_calculate_covariance_matrix(self, points_fix: Points2D) -> None:
        """
        """
        cov_mat = points_fix.calculate_covariance_matrix()
        expected = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 0.]])
        assert_array_equal(cov_mat, expected)

    def test_subtract(self, points_fix: Points2D) -> None:
        """
        """
        p3 = Point2D(1.0, 1.0, 1.0)
        point_diffs = points_fix - p3
        assert point_diffs.points[0] == Point2D(0.0, 0.0, 0.0)
        assert point_diffs.points[1] == Point2D(2.0, 0.0, 0.0)
        assert point_diffs.points[2] == Point2D(2.0, 2.0, 0.0)
        assert point_diffs.points[3] == Point2D(0.0, 2.0, 0.0)

    def test_inplace_subtract(self, points_fix: Points2D) -> None:
        """
        """
        p3 = Point2D(x=1.0, y=1.0, w=1.0)
        points_fix -= p3
        assert points_fix.points[0] == Point2D(0.0, 0.0, 0.0)
        assert points_fix.points[1] == Point2D(2.0, 0.0, 0.0)
        assert points_fix.points[2] == Point2D(2.0, 2.0, 0.0)
        assert points_fix.points[3] == Point2D(0.0, 2.0, 0.0)

    def test_get_item(self, points_fix: Points2D) -> None:
        """
        """
        for i in range(len(points_fix._points)):
            assert points_fix[i] == points_fix._points[i]
        

if __name__ == "__main__":
    pass
    