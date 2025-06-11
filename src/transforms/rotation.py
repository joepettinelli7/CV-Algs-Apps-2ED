import math
import numpy as np
from src.transforms.transform_base import TransformBase2D
from src.transforms.translation import TranslationTransform2D
from src.primitives.rectangle import Rectangle2D


class RotationTransform2D(TransformBase2D):
    """
    Preserves: lengths, angles, parallelism, straight lines.
    """

    def __init__(self, theta: float = 0.) -> None:
        """
        Default is no rotation.

        Args:
            Theta: Rotation angle in radians
        """
        super().__init__()
        self._theta = theta
        self._M[0][0] = math.cos(theta)
        self._M[0][1] = -math.sin(theta)
        self._M[1][0] = math.sin(theta)
        self._M[1][1] = math.cos(theta)
        self._DoF = 1

    @property
    def theta(self) -> float:
        """
        The rotion angle in radians

        Returns:
            Theta
        """
        return self._theta

    @theta.setter
    def theta(self, new_theta: float) -> None:
        """
        Set the rotation angle in radians

        Args:
            new_theta: New theta
        """
        self._theta = new_theta

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply rotation to the rectangle corners.

        Args:
            rect: Rectangle object

        Returns:
            The rectangle with rotated corner points.
        """
        if not super().from_origin:
            center = rect.center
            to_origin = TranslationTransform2D(-center.x, -center.y)
            to_center = TranslationTransform2D(center.x, center.y)
            # Shift to origin, rotate, shift back to object center
            self._M = to_center.M @ self._M @ to_origin.M
        rect = super().apply_to_rectangle(rect)
        self.reset()
        return rect

    def reset(self) -> None:
        """
        Reset M with instance variables.
        """
        super().reset()
        self._M[0][0] = math.cos(self._theta)
        self._M[0][1] = -math.sin(self._theta)
        self._M[1][0] = math.sin(self._theta)
        self._M[1][1] = math.cos(self._theta)


if __name__ == "__main__":
    pass
    