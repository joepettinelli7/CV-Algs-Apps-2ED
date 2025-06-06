import numpy as np
from src.transforms.transform_base import TransformBase2D
from src.transforms.translation import TranslationTransform2D
from src.primitives.rectangle import Rectangle2D


class ShearTransform2D(TransformBase2D):
    """
    Preserves: parallelism, straight lines.
    """

    def __init__(self, theta: float = 0.) -> None:
        """
        Theta is angle to shear lines and should be in radians.
        """
        super().__init__()
        self._theta = theta
        self._M[0][1] = np.tan(theta)
        self._DoF = 1

    @property
    def theta(self) -> float:
        """
        Angle to shear lines in radians.

        Returns:
            Theta
        """
        return self._theta

    @theta.setter
    def theta(self, new_theta: float) -> None:
        """
        Set the new theta value.

        Args:
            new_shear_factor: New theta in radians.
        """
        self._theta = new_theta

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply shear to the rectangle corners.

        Args:
            rect: Rectangle object

        Returns:
            The rectangle with sheared corner points.
        """
        if not super().from_origin:
            center = rect.center
            to_origin = TranslationTransform2D(-center.x, -center.y)
            to_center = TranslationTransform2D(center.x, center.y)
            # Shift to origin, shear, shift back to object center
            self._M = to_center.M @ self._M @ to_origin.M
        rect = super().apply_to_rectangle(rect)
        self.reset()  # Need to reset with instance variables
        return rect

    def reset(self) -> None:
        """
        Reset M with instance variables.
        """
        super().reset()
        self._M[0][1] = np.tan(self._theta)


if __name__ == "__main__":
    pass
    