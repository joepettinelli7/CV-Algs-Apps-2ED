import pytest
import numpy as np
from numpy.testing import assert_array_equal
from src.primitives.point import Point2D
from src.primitives.line import Line2D
from src.primitives_lists.lines import Lines2D


@pytest.fixture
def lines_fix() -> Lines2D:
    l1 = Line2D(coeffs=(10.0, -4.0, 1.0))
    l2 = Line2D(coeffs=(-3.0, 10.0, 1.0))
    l3 = Line2D(coeffs=(4.0, 7.0, 1.0))
    return Lines2D([l1, l2, l3])


class TestLines2D:

    def test_calculate_closest_point(self, lines_fix: Lines2D) -> None:
        """
        """
        point = lines_fix.calculate_closest_point()
        assert point == Point2D(-0.12, -0.11, 0.99)

    def test_calculate_A(self, lines_fix: Lines2D) -> None:
        """
        """
        A = lines_fix.calculate_A()
        expected = np.array([[125., -42., 11.],
                             [-42., 165., 13.],
                             [ 11.,  13., 3.]]
                           )
        assert_array_equal(A, expected)

    def test_append(self, lines_fix: Lines2D) -> None:
        """
        """
        original_len = len(lines_fix._lines)
        lines_fix.append(Line2D(coeffs=(1.0, 4.0, 1.0)))
        new_len = len(lines_fix._lines)
        assert new_len == original_len + 1
    
    def test_get_item(self, lines_fix: Lines2D) -> None:
        """
        """
        for i in range(len(lines_fix._lines)):
            assert lines_fix[i] == lines_fix._lines[i]
            

if __name__ == "__main__":
    pass
