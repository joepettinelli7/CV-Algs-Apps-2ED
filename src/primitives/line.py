import math
from typing import Callable, Optional, Union
import numpy as np
from src.primitives.point import Point2D


class Line2D:
    """
    The class to represent a 2D line. By default, Line2D is a homogenous line
    (ax + by + c = 0). A Line2D can be instantiated with two homogenous points
    with form (x, y, w), or by the coefficients of the line a, b, c. See page 30.
    """

    def __init__(self, points: Optional[tuple[Point2D, Point2D]] = None,
                 coeffs: Optional[tuple[float, float, float]] = None) -> None:
        """
        """
        if points is None:
            self._p1, self._p2 = None, None
            self._a, self._b, self._c = coeffs[0], coeffs[1], coeffs[2]
        else:
            self._p1, self._p2 = points
            coeffs = np.cross(self._p1.vector, self._p2.vector, axis=0)
            self._a, self._b, self._c = coeffs[0][0], coeffs[1][0], coeffs[2][0]

    def __repr__(self) -> str:
        """
        Use the vector of coefficients to represent the line.
        
        Returns:
            Use coefficients to represent vector.
        """
        return f"Line2D({self.vector})"

    @property
    def vector(self) -> np.ndarray:
        """
        Use the coefficients (a, b, c) to represent the line vector.
        In the book, all vectors are column vectors that post-multiply
        matrices unless specified.

        Returns:
            The (3, 1) shape column vector
        """
        return np.vstack([self._a, self._b, self._c])

    @property
    def p1(self) -> Optional[Point2D]:
        """
        One of two points used to define the line
        
        Returns:
            A point
        """
        return self._p1

    @property
    def p2(self) -> Optional[Point2D]:
        """
        One of two points used to define the line
        
        Returns:
            A point
        """
        return self._p2

    @property
    def a(self) -> float:
        """
        Component of normal vector to line
        
        Returns:
            Coefficient or None
        """
        return self._a

    @property
    def b(self) -> float:
        """
        Component of normal vector to line
        
        Returns:
            Coefficient or None
        """
        return self._b
        
    @property
    def c(self) -> float:
        """
        Related to offset
        
        Returns:
            Coefficient or None
        """
        return self._c

    @property
    def polar_coords(self) -> np.ndarray:
        """
        Combination of theta (the angle of the normal
        vector to x-axis) and distance (signed distance from origin)
        is known as the polar coordinates.

        Returns:
            Polar coordinates as column vector
        """
        return np.vstack([self.theta, self.distance])

    @property
    def normalized_line_vector(self) -> np.ndarray:
        """
        Normalized line vector in which the unit normal vector
        perpendicular to the line vector is augmented with the
        distance of the line to the origin.

        Returns:
            (n hat bold, d) in book page 30
        """
        return np.vstack([self.nx, self.ny, self.distance])

    @property
    def normalized_normal_vector(self) -> np.ndarray:
        """
        Normalized normal vector (unit normal vector) that has magnitude of 1.
        Can also be expressed as (nx, ny) as shown on page 30 of book.

        Returns:
            Column vector with cos(theta), sin(theta)
        """
        return np.vstack([math.cos(self.theta), math.sin(self.theta)])

    @property
    def nx(self) -> float:
        """
        Divide by magnitude of the normal vector (a, b).
        
        Returns:
            The x-component of normalized normal vector.
        """
        return self._a * (1 / self.magnitude)

    @property
    def ny(self) -> float:
        """
        Divide by magnitude of the normal vector (a, b).

        Returns:
            The y-component of normalized normal vector.
        """
        return self._b * (1 / self.magnitude)

    @property
    def distance(self) -> float:
        """
        The signed distance of the line to origin along its
        normal direction. Divide by the magnitude of the normal
        vector (a, b).

        Returns:
            The distance.
        """
        return self._c * (1 / self.magnitude)

    @property
    def magnitude(self) -> float:
        """
        The length of the normal vector (a, b).
        This is needed to normalize the line vector
        to the unit normal vector.
        
        Returns:
            The magnitude
        """
        return math.sqrt(self._a ** 2 + self._b ** 2)

    @property
    def theta(self) -> float:
        """
        The angle (in radians) between normal
        vector (a, b) and the x-axis.
        
        Returns:
            The angle
        """
        return math.atan2(self._b, self._a)

    def intersection_with(self, other: "Line2D") -> Point2D:
        """
        Intersection of two lines. The cross product of self and other.

        Args:
            other: A line

        Returns:
            The intersection point
        """
        intersec = np.cross(self.vector, other.vector, axis=0)
        return Point2D(intersec[0], intersec[1], intersec[2])

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
        Get the y coordinate on line given x coordinate / coordinates

        Args:
            x: The x coordinate / coordinates

        Returns:
            The corresponding y coordinate on the line
        """
        if isinstance(x, float):
            y = (-self._a * x - self._c) / self._b
        else:
            y = [(-self._a * _x - self._c) / self._b for _x in x]
        return y

    def get_point_x_from_y(self, y: Union[float, list[float]]) -> Union[float, list[float]]:
        """
        Get the x coordinate on line given y coordinate / coordinates

        Args:
            y: The y coordinate / coordinates

        Returns:
            The corresponding x coordinate on the line
        """
        if isinstance(y, float):
            x = (-self._b * y - self._c) / self._a
        else:
            x = [(-self._b * _y - self._c) / self._a for _y in y]
        return x

    def __eq__(self, other: "Line2D") -> bool:
        """
        Lines are equal if they have the same coefficients.

        Args:
            other: The other line

        Returns:
            True if equal
        """
        return self._a == other.a and self._b == other.b and self._c == other.c


if __name__ == "__main__":
    pass
        