from typing import Optional
import numpy as np
from src.primitives.rectangle import Rectangle2D
from src.transforms.transform_base import TransformBase2D
from src.transforms.rotation import RotationTransform2D
from src.transforms.translation import TranslationTransform2D


class RigidTransform2D(TransformBase2D):
    """
    Composed of rotation + translation (AKA rigid body motion or Euclidean).
    Preserves: lengths, angles, parallelism, straight lines.
    """

    def __init__(self, theta: float = 0., tx: int = 0, ty: int = 0) -> None:
        """
        Default is no change.

        Args:
            theta: Rotation angle in radians
            tx: Translation x distance
            ty: Translation y distance
        """
        super().__init__()
        self._rotation = RotationTransform2D(theta)
        self._translation = TranslationTransform2D(tx, ty)
        self._M: np.ndarray = self._translation.M @ self._rotation.M  # rotate then translate
        self._DoF: int = self._rotation.DoF + self._translation.DoF  # 3

    @property
    def theta(self) -> float:
        """
        Get theta from the RotationTransform2D instance.

        Returns:
            Theta
        """
        return self._rotation.theta

    @theta.setter
    def theta(self, new_theta: float) -> None:
        """
        Set theta in the RotationTransform2D instance.

        Args:
            new_theta: New theta in radians.
        """
        self._rotation.theta = new_theta

    @property
    def tx(self) -> int:
        """
        Get translation in x direction from TranslationTransform2D instance.

        Returns:
            Translation
        """
        return self._translation.tx

    @tx.setter
    def tx(self, new_tx: int) -> None:
        """
        Set new translation in x direction in TranslationTransform2D instance.

        Args:
            new_tx: New translation x
        """
        self._translation.tx = new_tx

    @property
    def ty(self) -> int:
        """
        Get translation in y direction from TranslationTransform2D instance.

        Returns:
            Translation
        """
        return self._translation.ty

    @ty.setter
    def ty(self, new_ty: int) -> None:
        """
        Set new translation in y direction in TranslationTransform2D instance.

        Args:
            new_ty: New translation y
        """
        self._translation.ty = new_ty

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply rigid transform (rotate then translate) to the rectangle corners.

        Args:
            rect: Rectangle object

        Returns:
            The rectangle with rigid transformed corner points.
        """
        if not super().from_origin:
            center = rect.center
            to_origin = TranslationTransform2D(-center.x, -center.y)
            to_center = TranslationTransform2D(center.x, center.y)
            # Shift to origin, rigid, shift back to object center
            self._M = to_center.M @ self._M @ to_origin.M
        rect = super().apply_to_rectangle(rect)
        self.reset()
        return rect

    def reset(self) -> None:
        """
        Reset M with instance variables.
        """
        super().reset()
        self._M = self._translation.M @ self._rotation.M


if __name__ == "__main__":
    pass
    