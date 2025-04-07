import logging
from typing import Optional, Union
import numpy as np


class Point2D():
    """
    The class to represent a 2D point. By default, Point2D is homogenous (x, y, w) 
    Point2D can be converted to cartesian (x, y) and back to homogenous.
    """
    
    def __init__(self, x: float = 0.0, y: float = 0.0, w: Optional[float] = 1.0) -> None:
        self._x = x
        self._y = y
        if w == 0.0:
            w = 1.0
            logging.warning(" Overriding to w = 1.0")
        self._w = w

    def __repr__(self) -> str:
        if self._w is None:
            return f"Point2D({self.vector})"
        else:
            return f"Point2D({self.vector})"

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def w(self) -> Optional[float]:
        return self._w

    @property
    def is_homogenous(self) -> bool:
        """

        Returns:
            True if self is homogenous
        """
        return self._w is not None

    @property
    def vector(self) -> np.ndarray:
        """
        Make an array to represent a vector.
        In the book, all vectors are column
        vectors that post-multiply matrices
        
        Returns:
            A ndarray
        """
        if self._w:
            return np.array([self._x, self._y, self._w])
        else:
            return np.array([self._x, self._y])
    
    def to_homogenous(self, w: Union[int, float] = 1.0) -> None:
        """
        Convert an inhomogenous point to homogenous.

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
        If w is 0, then conversion is not allowed.
        """
        if self._w:
            self._x /= self._w
            self._y /= self._w
            self._w = None
        else:
            logging.error(" Already cartesian. Aborting conversion.")

    def __eq__(self, other: "Point2D") -> bool:
        """
        Determine whether the points are equivalent.

        For points to be equivalent:
            1. x and y are equivalent (For homogenous points, vectors that differ
               only by w are still considered to be equivalent).
            2. The representations should be the same (ex: both are cartesian).
        """
        spatial_eq = self._x == other._x and self._y == other._y
        repr_eq = (self._w is None) == (self._w is None)
        return spatial_eq and repr_eq        
