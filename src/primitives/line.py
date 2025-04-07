from typing import Callable, Optional, Union
from src.primitives.point import Point2D
import numpy as np


class Line2D:
    """
    The class to represent a 2D line. By default, Line2D is homogenous line (ax + by + cw = 0).
    It can be defined by the cross product of the two homogenous points, or by the coefficients
    a, b, c. It can be converted to cartesian line (ax + by + c = 0).
    """
    
    def __init__(self, p1: Optional[Point2D] = None, p2: Optional[Point2D] = None,
                 a: Optional[float] = None, b: Optional[float] = None, c: Optional[float]= None) -> None:
        """
        Either need two points to define the line or all three line vector elements
        """
        assert (isinstance(p1, Point2D) and isinstance(p2, Point2D)) or (isinstance(a, float) and isinstance(b, float) and isinstance(c, float))
        self._p1 = p1
        self._p2 = p2
        self._a = a
        self._b = b
        self._c = c

    def __repr__(self) -> str:
        if not self.is_homogenous:
            return f"Line2D({self.a}x + {self.b}y + {self.c} = 0)"
        else:
            return f"Line2D({self.vector})"

    @property
    def p1(self) -> Optional[Point2D]:
        return self._p1

    @property
    def p2(self) -> Optional[Point2D]:
        return self._p2

    @property
    def is_homogenous(self) -> bool:
        """
        """
        if self._p1 and self._p2:
            return self._p1.is_homogenous and self._p2.is_homogenous
        else:
            return True

    @property
    def a(self) -> Optional[float]:
        """
        Coefficient of homogenous line
        """
        return self._a

    @property
    def b(self) -> Optional[float]:
        """
        
        """
        return self._b
        
    @property
    def c(self) -> Optional[float]:
        """
        
        """
        return self._c


    # @property
    # def a(self) -> float:
    #     """
    #     For cartesian line
    #     """
    #     assert not self.is_homogenous
    #     a = self._p2.y - self._p1.y
    #     return a

    # @property
    # def b(self) -> float:
    #     """
    #     For cartesian line
    #     """
    #     assert not self.is_homogenous
    #     b = -(self._p2.x - self._p1.x)
    #     return b

    # @property
    # def c(self) -> float:
    #     """
    #     For cartesian line
    #     """
    #     assert not self.is_homogenous
    #     c = (self._p2.x - self._p1.x)*self._p1.y - (self._p2.y - self._p1.y)*self._p1.x
    #     return c

    # @property
    # def vector(self) -> Optional[np.ndarray]:
    #     """
    #     Only for homogenous lines. Make an array to
    #     represent a vector. In the book, all vectors
    #     are column vectors that post-multiply matrices
        
    #     Returns:
    #         A ndarray
    #     """
    #     if self.is_homogenous:
    #         return np.array(self.cross_product)

    def to_homogenous(self, w1: float = 1.0, w2: float = 1.0) -> None:
        """
        This will convert the line to homogenous from
        cartesian / inhomogenous by converting all points
        comprising the line to homogenous
        """
        assert not self.is_homogenous
        self._p1.to_homogenous(w=w)
        self._p2.to_homogenous(w=w)

    def from_homogenous(self) -> None:
        """
        This will convert the line from homogenous to
        cartesian / inhomogenous by converting all points
        comprising the line to cartesian / inhomogenous
        """
        assert self.is_homogenous
        self._p1.from_homogenous()
        self._p2.from_homogenous()

    @property
    def vector(self) -> np.ndarray:
        """
        Get the cross product of the two points
        which is the line vector

        Returns:
            The 3 element vector
        """
        if self._p1 and self._p2:
            pv1 = self._p1.vector
            pv2 = self._p2.vector
            cp = np.cross(pv1, pv2, axis=0)
        else:
            assert self._a and self._b and self._c
            cp = np.vstack([self._a, self._b, self._c])
        return cp

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
        If point is on line then dot product will equal 0.0
        """
        return np.dot(self.vector.T, point.vector).item() == 0.0
        