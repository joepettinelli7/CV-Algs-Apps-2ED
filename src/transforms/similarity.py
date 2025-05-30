from typing import Optional
import numpy as np
from src.primitives.rectangle import Rectangle2D
from src.transforms.transform_base import TransformBase2D
from src.transforms.rigid import RigidTransform2D
from src.transforms.scale import ScaleTransform2D


class SimilarityTransform2D(TransformBase2D):
    """
    Composed of scale + rigid transforms.
    Preserves: angles, parallelism, straight lines
    """

    def __init__(self, sx: float = 1., sy: float = 1., theta: float = 0., tx: int = 0.,
                 ty: int = 0., from_origin: bool = False) -> None:
        """

        """
        super().__init__()
        assert sx == sy  # scale must be equal unlike affine transform
        self._scale: ScaleTransform2D = ScaleTransform2D(sx=sx, sy=sy, from_origin=from_origin)
        self._rigid: RigidTransform2D = RigidTransform2D(theta=theta, tx=tx, ty=ty, from_origin=from_origin)
        self._M: np.ndarray = np.dot(self._scale.M, self._rigid.M)  # scale then rigid
        self._DoF: int = 4

    @property
    def theta(self) -> float:
        """
        Get theta from the RotationTransform2D class
        
        """
        return self._rigid.theta

    @theta.setter
    def theta(self, new_theta: float) -> None:
        """
        Set theta in the RotationTransform2D class
        
        """
        self._rigid.theta = new_theta

    @property
    def t_vector(self) -> np.ndarray[float, float]:
        """
        Get the TranslationTransform2D translation vector
        
        """
        return self._rigid.t_vector

    @t_vector.setter
    def t_vector(self, new_t_vector: np.ndarray) -> None:
        """
        Set the TranslationTransform2D translation vector
        
        """
        self._rigid.t_vector = new_t_vector

    @property
    def sx(self) -> float:
        """
        Get the scale x value from ScaleTransform2D class
        
        """
        return self._scale.sx

    @sx.setter
    def sx(self, new_scale_x: float) -> None:
        """
        Set the scale x value in ScaleTransform2D class
        
        """
        self._scale.sx = new_scale_x

    @property
    def sy(self) -> float:
        """
        Get the scale y value from ScaleTransform2D class
        
        """
        return self._scale.sy

    @sy.setter
    def sy(self, new_scale_y: float) -> None:
        """
        Set the scale y value in ScaleTransform2D class
        
        """
        self._scale.sy = new_scale_y

    def update_M(self) -> None:
        """
        Update M, but first update scale and rigid matrices.
        """
        self._scale.update_M()
        self._rigid.update_M()
        self._M = np.dot(self._scale.M, self._rigid.M)

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply similarity transform (scale then rigid) to the rectangle corners.
        Implementation similar to that of rigid transform.

        Args:
            rect: Rectangle object

        Returns:
            The similarity transformed corner points
        """
        rect = self._scale.apply_to_rectangle(rect=rect)
        rect = self._rigid.apply_to_rectangle(rect=rect)
        return rect


if __name__ == "__main__":
    pass
    