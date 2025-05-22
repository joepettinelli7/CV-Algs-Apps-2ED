from typing import Callable, Optional, Union
import numpy as np
from src.primitives.point import Point2D


class Line2D:
    """
    The class to represent a 2D line. By default, Line2D is a homogenous line (Ax + By + Cw = 0).
    A Line2D can be instantiated with two homogenous points with form (x, y, w), or by the coefficients
    of the line A, B, C. It can be converted to cartesian line (Ax + By + C = 0) where x=x/w, y=y/w.
    """

    def __init__(self, points: Optional[tuple[Point2D, Point2D]] = None,
                 coeffs: Optional[tuple[float, float, float]] = None) -> None:
        """
        Either need two points to define the line or all three coefficients.
        """
        assert points is not None or coeffs is not None
        if points is not None:
            self._p1, self._p2 = points
            self._a, self._b, self._c = None, None, None
        else:
            self._p1, self._p2 = None, None
            self._a, self._b, self._c = coeffs[0], coeffs[1], coeffs[2]

    def __repr__(self) -> str:
        """

        Returns:
            For cartesian line use Ax + By + c = 0. For homogenous,
            just use coefficients to represent vector.
        """
        if not self.is_homogenous:
            return f"Line2D({self._a}x + {self._b}y + {self._c} = 0)"
        else:
            return f"Line2D({self.vector})"

    @property
    def p1(self) -> Optional[Point2D]:
        """

        Returns:
            Point in the line
        """
        return self._p1

    @property
    def p2(self) -> Optional[Point2D]:
        """

        Returns:
            Point in the line
        """
        return self._p2

    @property
    def is_homogenous(self) -> bool:
        """
        The line is considered homogeneous if the points comprising
        it are homogenous. * May need to change.
        
        Returns:
            True if the line is homogeneous
        """
        if self._p1 is not None and self._p2 is not None:
            return self._p1.is_homogenous and self._p2.is_homogenous
        else:
            return True

    @property
    def a(self) -> Optional[float]:
        """
        Float when coefficients were used to instantiate
        Line2D. None when Point2D was used instead.
        
        Returns:
            Coefficient of homogenous line or None
        """
        return self._a

    @property
    def b(self) -> Optional[float]:
        """
        Float when coefficients were used to instantiate
        Line2D. None when Point2D was used instead.
        
        Returns:
            Coefficient of homogenous line or None
        """
        return self._b
        
    @property
    def c(self) -> Optional[float]:
        """
        Float when coefficients were used to instantiate
        Line2D. None when Point2D was used instead.
        
        Returns:
            Coefficient of homogenous line or None
        """
        return self._c

    def to_homogenous(self, w1: float = 1.0, w2: float = 1.0) -> None:
        """
        This will convert the line to homogenous from
        cartesian / inhomogenous by converting all points
        comprising the line to homogenous. * May need to change.

        Args:
            w1: w for point 1
            w2: w for point 2
        """
        assert not self.is_homogenous
        self._p1.to_homogenous(w=w)
        self._p2.to_homogenous(w=w)

    def from_homogenous(self) -> None:
        """
        This will convert the line from homogenous to
        cartesian / inhomogenous by converting all points
        comprising the line to cartesian / inhomogenous.
        * May need to change.
        """
        assert self.is_homogenous
        self._p1.from_homogenous()
        self._p2.from_homogenous()

    @property
    def vector(self) -> np.ndarray:
        """
        Get the cross product of the two points which is the
        line vector. In the book, all vectors are column vectors
        that post-multiply matrices unless specified.

        Returns:
            The 3 element vector
        """
        if self._p1 is not None and self._p2 is not None:
            pv1 = self._p1.vector
            pv2 = self._p2.vector
            vec = np.cross(pv1, pv2, axis=0)
        else:
            assert self._a is not None and self._b is not None and self._c is not None
            vec = np.vstack([self._a, self._b, self._c])
        return vec

    def intersection_with(self, other: "Line2D") -> Point2D:
        """
        Intersection of two lines. The cross product of self and other.

        Args:
            other: A line

        Returns:
            The intersection point
        """
        intersec = np.cross(self.vector, other.vector, axis=0)
        return Point2D(x=intersec[0], y=intersec[1], w=intersec[2])

    def contains_point(self, point: Point2D) -> bool:
        """
        If point is on line then dot product will equal 0.0.

        Args:
            point: Point to check

        Returns:
            True if point lies on line
        """
        return np.dot(self.vector.T, point.vector).item() == 0.0

    def get_point_y_from_x(self, x: Union[float, list[float]]) -> Union[float, list[float]]:
        """
        Get the y coordinate on line given x coordinate

        Args:
            x: The x coordinate

        Returns:
            The corresponding y coordinate on the line
        """
        y = (-self._a * x - self._c) / self._b
        return y

    def get_point_x_from_y(self, y: Union[float, list[float]]) -> Union[float, list[float]]:
        """
        Get the x coordinate on line given y coordinate

        Args:
            y: The y coordinate

        Returns:
            The corresponding x coordinate on the line
        """
        x = (-self._b * y - self._c) / self._a
        return x
        