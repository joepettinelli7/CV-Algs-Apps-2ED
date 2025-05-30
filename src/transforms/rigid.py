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

    def __init__(self, theta: float = 0., tx: int = 0., ty: int = 0., from_origin: bool = False) -> None:
        """
        """
        super().__init__()
        self._rotation: RotationTransform2D = RotationTransform2D(theta=theta, from_origin=from_origin)
        self._translation: TranslationTransform2D = TranslationTransform2D(tx=tx, ty=ty)
        self._M: np.ndarray = np.dot(self._rotation.M, self._translation.M)  # rotation then translation
        self._DoF: int = 3

    @property
    def theta(self) -> float:
        """
        Get theta from the RotationTransform2D class
        
        """
        return self._rotation.theta

    @theta.setter
    def theta(self, new_theta: float) -> None:
        """
        Set theta in the RotationTransform2D class
        
        """
        self._rotation.theta = new_theta

    @property
    def t_vector(self) -> np.ndarray[float, float]:
        """
        Get the TranslationTransform2D translation vector
        
        """
        return self._translation.t_vector

    @t_vector.setter
    def t_vector(self, new_t_vector: np.ndarray) -> None:
        """
        Set the TranslationTransform2D translation vector
        
        """
        self._translation.t_vector = new_t_vector

    def update_M(self) -> None:
        """
        Update M, but first update rotation and translation matrices.
        """
        self._rotation.update_M()
        self._translation.update_M()
        self._M = np.dot(self._rotation.M, self._translation.M)

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply rigid transform (rotate then translate) to the rectangle corners.
        Composed of rotation and translation, so utilize those methods and make
        this implementation different.

        Args:
            rect: Rectangle object

        Returns:
            The rigid transformed corner points
        """
        rect = self._rotation.apply_to_rectangle(rect=rect)
        rect = self._translation.apply_to_rectangle(rect=rect)
        return rect


if __name__ == "__main__":
    pass
    