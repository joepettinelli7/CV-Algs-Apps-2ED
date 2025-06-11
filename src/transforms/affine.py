from typing import Optional
import numpy as np
from src.primitives.rectangle import Rectangle2D
from src.transforms.transform_base import TransformBase2D
from src.transforms.rigid import RigidTransform2D
from src.transforms.scale import ScaleTransform2D
from src.transforms.shear import ShearTransform2D
from src.transforms.translation import TranslationTransform2D


class AffineTransform2D(TransformBase2D):
    """
    Composed of rigid + non-uniform scale + shear transforms (Cannot
    use similarity transform because it does not allow non-uniform scale).
    Preserves: parallelism, straight lines.
    """

    def __init__(self, sx: float = 1., sy: float = 1., shear_theta: float = 0.,
                 theta: float = 0., tx: int = 0, ty: int = 0) -> None:
        """
        Default is no change.
        
        Args:
            sx: Scale x
            sy: Scale y
            shear_theta: Shear angle in radians
            theta: Rotation angle in radians
            tx: Translation x distance
            ty: Translation y distance
        """
        super().__init__()
        self._scale = ScaleTransform2D(sx, sy)
        self._shear = ShearTransform2D(shear_theta)
        self._rigid = RigidTransform2D(theta, tx, ty)
        self._M: np.ndarray = self._rigid.M @ self._shear.M @ self._scale.M  # scale, shear, rigid
        self._DoF: int = self._scale.DoF + self._shear.DoF + self._rigid.DoF  # 6

    @property
    def sx(self) -> float:
        """
        Get the scale x value from ScaleTransform2D instance.

        Returns:
            Scale x factor
        """
        return self._scale.sx

    @sx.setter
    def sx(self, new_scale_x: float) -> None:
        """
        Set the scale x value in ScaleTransform2D instance.

        Args:
            new_scale_x: New scale factor
        """
        self._scale.sx = new_scale_x

    @property
    def sy(self) -> float:
        """
        Get the scale y value from ScaleTransform2D instance.

        Returns:
            Scale y factor
        """
        return self._scale.sy

    @sy.setter
    def sy(self, new_scale_y: float) -> None:
        """
        Set the scale y value in ScaleTransform2D instance.

        Args:
            new_scale_y: New scale factor
        """
        self._scale.sy = new_scale_y

    @property
    def shear_theta(self) -> float:
        """
        Get shear theta from the ShearTransform2D instance.

        Returns:
            The shear theta
        """
        return self._shear.theta

    @shear_theta.setter
    def shear_theta(self, new_shear_theta: float) -> None:
        """
        Set shear theta in the ShearTransform2D instance.

        Args:
            new_shear_theta: New shear theta
        """
        self._shear.theta = new_shear_theta

    @property
    def theta(self) -> float:
        """
        Get rotation theta from the RigidTransform2D instance.

        Returns:
            Theta in radians.
        """
        return self._rigid.theta

    @theta.setter
    def theta(self, new_theta: float) -> None:
        """
        Set rotation theta in the RigidTransform2D instance.

        Args:
            theta: New theta in radians.
        """
        self._rigid.theta = new_theta

    @property
    def tx(self) -> int:
        """
        Translation in x direction

        Returns:
            Translation distance
        """
        return self._rigid.tx

    @tx.setter
    def tx(self, new_tx: int) -> None:
        """
        Set new translation in x direction

        Args:
            new_tx: New translation distance
        """
        self._rigid.tx = new_tx

    @property
    def ty(self) -> int:
        """
        Translation in y direction

        Returns:
            Translation distance
        """
        return self._rigid.ty

    @ty.setter
    def ty(self, new_ty: int) -> None:
        """
        Set new translation in y direction

        Args:
            new_ty: New translation distance
        """
        self._rigid.ty = new_ty

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply affine transform (shear, scale, rigid) to the rectangle corners.

        Args:
            rect: Rectangle object

        Returns:
            The rectangle object with affine transformed corner points.
        """
        if not super().from_origin:
            center = rect.center
            to_origin = TranslationTransform2D(-center.x, -center.y)
            to_center = TranslationTransform2D(center.x, center.y)
            # Shift to origin, affine, shift back to object center
            self._M = to_center.M @ self._M @ to_origin.M
        rect = super().apply_to_rectangle(rect)
        self.reset()
        return rect

    def reset(self) -> None:
        """
        Reset M with instance variables.
        """
        super().reset()
        self._M = self._rigid.M @ self._shear.M @ self._scale.M
        

if __name__ == "__main__":
    pass
    