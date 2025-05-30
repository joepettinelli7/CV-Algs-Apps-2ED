from typing import Optional
import numpy as np
from src.primitives.rectangle import Rectangle2D
from src.transforms.transform_base import TransformBase2D
from src.transforms.rigid import RigidTransform2D
from src.transforms.scale import ScaleTransform2D
from src.transforms.shear import ShearTransform2D


class AffineTransform2D(TransformBase2D):
    """
    Composed of rigid + non-uniform scale + shear transforms (Cannot
    use similarity transform because it does not allow non-uniform scale).
    Preserves: parallelism, straight lines
    """

    def __init__(self, sx: float = 1., sy: float = 1., shear_theta: float = 0.,
                 theta: float = 0., tx: int = 0., ty: int = 0., from_origin: bool = False) -> None:
        """

        Args:
            sx: Scale x
            sy: Scale y
            shear_theta: Shear theta
            theta: Rotation theta
            tx: Translate x
            ty: Translate y
            from_origin: Whether to apply from origin
        """
        self._rigid: RigidTransform2D = RigidTransform2D(theta=theta, tx=tx, ty=ty, from_origin=from_origin)
        self._scale: ScaleTransform2D = ScaleTransform2D(sx=sx, sy=sy, from_origin=from_origin)
        self._shear: ShearTransform2D = ShearTransform2D(theta=shear_theta, from_origin=from_origin)
        self._M: np.ndarray = self._scale.M @ self._shear.M @ self._rigid.M  # scale, shear, rigid
        self._DoF: int = 6

    @property
    def shear_val(self) -> float:
        """
        Get shear val from the ShearTransform2D class
        
        """
        return self._shear.shear_val

    @shear_val.setter
    def shear_val(self, new_shear_val: float) -> None:
        """
        Set shear val in the ShearTransform2D class
        
        """
        self._shear.shear_val = new_shear_val

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
        Update M, but first update scale, shear, rigid matrices.
        """
        self._scale.update_M()
        self._shear.update_M()
        self._rigid.update_M()
        self._M = self._scale.M @ self._shear.M @ self._rigid.M

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply affine transform (shear, scale, rigid) to the rectangle corners.
        Implementation similar to that of rigid and similarity transforms.

        Args:
            rect: Rectangle object

        Returns:
            The affine transformed corner points
        """
        rect = self._scale.apply_to_rectangle(rect=rect)
        rect = self._shear.apply_to_rectangle(rect=rect)
        rect = self._rigid.apply_to_rectangle(rect=rect)
        return rect
        

if __name__ == "__main__":
    pass
    