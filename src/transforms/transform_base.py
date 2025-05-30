from typing import Optional
import numpy as np
from src.primitives.point import Point2D
from src.primitives.rectangle import Rectangle2D


class TransformBase2D:

    def __init__(self) -> None:
        """
        Base class for translation, rigid, similarity, affine,
        projective transforms. Default for homogenous coordinates.
        """
        # Initialize with 3x3 identity matrix
        self._M: np.ndarray = np.array([
            [1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]], dtype=float)
        # Degrees of freedom
        self._DoF: int = -1

    def __repr__(self) -> str:
        """
        Use the matrix to represent transform
        
        Returns:
            The transform name and the matrix
        """
        return f"{self.__class__.__name__}: {self._M}\n"

    @property
    def M(self) -> np.ndarray:
        """
        """
        return self._M

    @M.setter
    def M(self, new_M: np.ndarray) -> None:
        """

        Args:
            new_M: The new matrix to set
        """
        self._M = new_M

    @property
    def DoF(self) -> int:
        """
        """
        return self._DoF

    @DoF.setter
    def DoF(self, new_DoF: int) -> None:
        """

        Args:
            new_DoF: New degrees of freedom
        """
        self._DoF = new_DoF

    def apply_to_point(self, point: Point2D) -> Point2D:
        """
        Apply the matrix

        Args:
            point: The point to apply transform to

        Returns:
            The transformed point
        """
        transformed = np.dot(self._M, point.vector)
        point.x, point.y, point.w = transformed[:3]
        return point

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply the transform to the rectangle corners

        Args:
            rect: Rectangle object

        Returns:
            The transformed corner points
        """
        transformed_arrs = [np.dot(self._M, p.vector) for p in rect.corners]
        points: list[Point2D] = []
        for transformed_arr in transformed_arrs:
            x_new, y_new, w_new = transformed_arr[:3]
            points.append(Point2D(x_new, y_new, w_new))
        rect = Rectangle2D(points[0], points[1], points[2], points[3])
        return rect
        

if __name__ == "__main__":
    pass
