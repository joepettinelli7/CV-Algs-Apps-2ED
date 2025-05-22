import logging
from typing import Optional, Union, List
import numpy as np


class Point2D():
    """
    The class to represent a 2D point. By default, Point2D is homogenous (x, y, w). 
    Point2D can be converted to cartesian (x, y) and back to homogenous.
    """
    
    def __init__(self, x: float = 0.0, y: float = 0.0, w: Optional[float] = 1.0) -> None:
        """
        Setting w to 1.0 is equivalent to the cartesian coordinate (x, y)
        """
        self._x = x
        self._y = y
        if w == 0.0:
            w = 1.0
            logging.warning(" Overriding to w = 1.0")
        self._w = w

    def __repr__(self) -> str:
        """
        Use the vector / coordinates to represent the point
        
        Returns:
            The vector (x, y, w) or (x, y)
        """
        if self._w is None:
            return f"Point2D({self.vector})"
        else:
            return f"Point2D({self.vector})"

    @property
    def x(self) -> float:
        """
        
        Returns:
            The x coordinate
        """
        return self._x

    @property
    def y(self) -> float:
        """

        Returns:
            The y coordinate
        """
        return self._y

    @property
    def w(self) -> Optional[float]:
        """
        Will be None when Point2D represents a
        cartesian coordinate. A homogenous coordinate
        when w is 1.0 is equivalent to cartesian (x, y).
        
        Returns:
            The w coordinate
        """
        return self._w

    @property
    def is_homogenous(self) -> bool:
        """
        w will be a float when Point2D is representing
        a homogeneous point. It will be None when cartesian.
        
        Returns:
            True if self is homogenous
        """
        return self._w is not None

    @property
    def vector(self) -> np.ndarray:
        """
        Make an array to represent a column vector.
        In the book, all vectors are column vectors
        that post-multiply matrices unless specified.
        
        Returns:
            A ndarray with shape (n, 1)
        """
        if self._w:
            return np.vstack([self._x, self._y, self._w])
        else:
            return np.vstack([self._x, self._y])
    
    def to_homogenous(self, w: Union[int, float] = 1.0) -> None:
        """
        Convert a cartesian point to homogenous.

        Args:
            w: The scaling factor
        """
        if not self._w:
            if isinstance(w, int):
                w = float(w)
            if w != 0.0:
                self._x *= w
                self._y *= w
                self._w = w
            else:
                logging.warning(f" Do not except w == 0, so aborting conversion.")
        else:
            logging.warning(f" Already homogenous, so aborting conversion.")

    def from_homogenous(self) -> None:
        """
        Convert from homogenous point to cartesian / inhomogenous.
        If w is 0.0, then conversion is not allowed.
        """
        if self._w and self._w != 0.0:
            self._x /= self._w
            self._y /= self._w
            self._w = None
        else:
            logging.error(" Already cartesian or w is 0.0. Aborting conversion.")

    def __eq__(self, other: "Point2D") -> bool:
        """
        Determine whether the points are equivalent.
        
        For points to be equivalent:
            1. x and y are equivalent (For homogenous points, vectors that differ
               only by w are still considered to be equivalent).
            2. The representations should be the same (ex: both are homogenous).

        Args:
            other: The other point

        Returns:
            True if points are equivalent
        """
        spatial_eq = self._x == other._x and self._y == other._y
        repr_eq = (self._w is None) == (other._w is None)
        return spatial_eq and repr_eq

    def __add__(self, other: "Point2D") -> "Point2D":
        """
        Add cartesian points (x1 + x2 and y1 + y2).

        Args:
            other: The other point

        Returns:
            The sum of the points
        """
        if isinstance(other, Point2D):
            assert not other.is_homogenous and not self.is_homogenous
            self._x = self._x + other.x
            self._y = self._y + other.y
            return self
        else:
            raise TypeError(f"Cannot add {other.__class__} object to Point2D object.")

    def __sub__(self, other: "Point2D") -> "Point2D":
        """
        Subtract cartesian points (x1 - x2 and y1 - y2).

        Args:
            other: The other point

        Returns:
            The difference of the points
        """
        if isinstance(other, Point2D):
            assert not other.is_homogenous and not self.is_homogenous
            self._x = self._x - other.x
            self._y = self._y - other.y
            return self
        else:
            raise TypeError(f"Cannot subtract {other.__class__} object from Point2D object.")
    
    def __truediv__(self, other: Union["Point2D", int]) -> "Point2D":
        """
        Divide cartesian points (x1 / x2 and y1 / y2).

        Args:
            other: The other point or float

        Returns:
            The sum of the points
        """
        if isinstance(other, Point2D) or isinstance(other, int):
            if isinstance(other, int):
                other = Point2D(other, other, None)
            assert not other.is_homogenous and not self.is_homogenous
            self._x = self._x / other.x
            self._y = self._y / other.y
            return self
        else:
            raise TypeError(f"Cannot divide Point2D object with {other.__class__} object.")
        