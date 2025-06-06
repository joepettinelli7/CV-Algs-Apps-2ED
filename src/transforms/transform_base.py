from typing import Optional
import numpy as np
from src.primitives.point import Point2D
from src.primitives.rectangle import Rectangle2D


class TransformBase2D:
    """
    Base class for all other transforms. Currently implemented
    for 2D and homogenous coordinates.
    """

    def __init__(self) -> None:
        """
        Initialize with 3x3 identity matrix and set degrees of
        freedom to -1. By default, objects will be transformed
        from their center (not from the canvas origin).
        """
        self._M: np.ndarray = np.array([
            [1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]], dtype=float)
        self._DoF: int = -1
        self._from_origin: bool = False

    def __repr__(self) -> str:
        """
        Use the matrix to represent transform.
        
        Returns:
            The transform name and the matrix.
        """
        return f"{self.__class__.__name__}: {self._M}\n"

    @property
    def M(self) -> np.ndarray:
        """
        The transformation matrix.

        Returns:
            3x3 numpy array
        """
        return self._M

    @M.setter
    def M(self, new_M: np.ndarray) -> None:
        """
        Set the matrix M.

        Args:
            new_M: The new matrix to set.
        """
        self._M = new_M

    @property
    def DoF(self) -> int:
        """
        Degrees of freedom (number of values needed
        to constuct the transform matrix).
        
        Returns:
            Degrees of freedom
        """
        return self._DoF

    @DoF.setter
    def DoF(self, new_DoF: int) -> None:
        """
        Set the degrees of freedom.
        
        Args:
            new_DoF: New degrees of freedom
        """
        self._DoF = new_DoF

    @property
    def from_origin(self) -> bool:
        """
        Whether to apply the transform from origin
        or from the object center.

        Returns:
            True if transform should be applied from
            the canvas origin. False for object center.
        """
        return self._from_origin

    @from_origin.setter
    def from_origin(self, new_from_origin: bool) -> None:
        """
        Set new value.

        Args:
            new_from_origin: Whether to transform object from
                             canvas origin or object center.
        """
        self._from_origin = new_from_origin

    def apply_to_point(self, point: Point2D, in_place: bool = True) -> Point2D:
        """
        Apply the matrix to a single point object.

        Args:
            point: The homogenous point to apply transform to.
            in_place: Whether to transform the point in place.
                      * Be careful when True because it can lead
                        to a compounding effect when multiple transformations
                        are applied to the same point inadvertently. *

        Returns:
            The transformed point.
        """
        transformed = np.dot(self._M, point.vector)
        if in_place:
            point.x, point.y, point.w = transformed[:3]
            return point
        else:
            x, y, w = transformed[:3]
            return Point2D(x, y, w)

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply the transform to the rectangle corners.
        Apply transform to all 4 corner points that define
        the rectangle in-place.

        Args:
            rect: Rectangle object

        Returns:
            The transformed rectangle
        """
        for idx, corner in enumerate(rect.corners):
            rect[idx] = self.apply_to_point(corner)
        return rect

    def reset(self) -> None:
        """
        Reset M to the same 3x3 identity matrix that
        the instance was initialized with.
        """
        self._M = np.identity(3, dtype=float)
        

if __name__ == "__main__":
    pass
