from typing import Optional, Tuple
import math
import numpy as np
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
    def rotation(self) -> RotationTransform2D:
        """
        The rotation matrix

        Returns:
            The rotation matrix
        """
        return self._rotation

    @property
    def translation(self) -> TranslationTransform2D:
        """
        The translation matrix

        Returns:
            The translation matrix
        """
        return self._translation

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
        Also update M with new rotation to synchronize.

        Args:
            new_theta: New theta in radians.
        """
        self._rotation.theta = new_theta
        self.update_M()

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
        Set new translation in x direction in TranslationTransform2D
        instance. Also update M to synchronize.

        Args:
            new_tx: New translation x
        """
        self._translation.tx = new_tx
        self.update_M()

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
        Set new translation in y direction in TranslationTransform2D
        instance. Also update M to synchronize.

        Args:
            new_ty: New translation y
        """
        self._translation.ty = new_ty
        self.update_M()

    def update_M(self) -> None:
        """
        Update M with instance variables.
        """
        super().reset()
        self._M = self._translation.M @ self._rotation.M

    def get_decomposed(self) -> Tuple[RotationTransform2D, TranslationTransform2D]:
        """
        Decompose the matrix M into it's component rotation and translation matrices.
        Do this as if component matrices are unknown. Do not change M.

        Returns:
            (rotation transform, translation transform)
        """
        theta = math.atan2(self._M[1][0], self._M[0][0])
        rotation = RotationTransform2D(theta)
        tx, ty = self._M[0][2], self._M[1][2]
        translation = TranslationTransform2D(tx, ty)
        return rotation, translation


if __name__ == "__main__":
    pass
    