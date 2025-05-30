import math
import numpy as np
from src.transforms.transform_base import TransformBase2D
from src.transforms.translation import TranslationTransform2D
from src.primitives.rectangle import Rectangle2D


class RotationTransform2D(TransformBase2D):
    """
    Preserves: lengths, angles, parallelism, straight lines.
    """

    def __init__(self, theta: float = 0., from_origin: bool = False) -> None:
        """
        By default, will rotate from object center. If from_origin is True,
        then object will appear to rotate and translate.

        Args:
            theta: Radians
        """
        super().__init__()
        self._theta = theta
        self._from_origin = from_origin
        self._M[0][0] = math.cos(theta)
        self._M[0][1] = -math.sin(theta)
        self._M[1][0] = math.sin(theta)
        self._M[1][1] = math.cos(theta)
        self._DoF = 1

    @property
    def theta(self) -> float:
        """
        """
        return self._theta

    @theta.setter
    def theta(self, new_theta: float) -> None:
        """
        """
        self._theta = new_theta

    @property
    def from_origin(self) -> bool:
        """
        """
        return self._from_origin

    @from_origin.setter
    def from_origin(self, new_from_origin: bool) -> None:
        """
        """
        self._from_origin = new_from_origin

    def to_degrees(self, radians: float) -> float:
        """
        Convert radians to degrees

        Args:
            radians: Radians

        Returns:
            Degrees
        """
        return radians * (180 / math.pi)

    def to_radians(self, degrees: float) -> float:
        """
        Convert degrees to radians

        Args:
            degrees: Degrees

        Returns:
            Radians
        """
        return degrees * (math.pi / 180)

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply rotation to the rectangle corners

        Args:
            rect: Rectangle object

        Returns:
            The rotated corner points
        """
        if not self._from_origin:
            # Update matrix
            center = rect.center
            translation_to_orig = TranslationTransform2D(tx=-center.x, ty=-center.y)
            translation_to_center = TranslationTransform2D(tx=center.x, ty=center.y)
            # Shift to origin, rotate, shift back to object center
            self._M = translation_to_center.M @ self._M @ translation_to_orig.M
        rect = super().apply_to_rectangle(rect=rect)
        return rect

    def update_M(self) -> None:
        """
        Update M with current rotation values
        """
        self._M[0][0] = math.cos(self._theta)
        self._M[0][1] = -math.sin(self._theta)
        self._M[1][0] = math.sin(self._theta)
        self._M[1][1] = math.cos(self._theta)


if __name__ == "__main__":
    pass
    