from typing import Optional, Tuple
import math
import numpy as np
from src.primitives.rectangle import Rectangle2D
from src.transforms.transform_base import TransformBase2D
from src.transforms.rigid import RigidTransform2D
from src.transforms.scale import ScaleTransform2D
from src.transforms.shear import ShearTransform2D
from src.transforms.translation import TranslationTransform2D


class AffineTransform2D(TransformBase2D):
    """
    Composed of rigid + non-uniform scale + shear transforms (CANNOT
    use similarity transform because it does NOT allow non-uniform scale).
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
        self._M: np.ndarray = self._rigid.M @ self._scale.M @ self._shear.M  # shear, scale, rigid
        self._DoF: int = self._shear.DoF + self._scale.DoF + self._rigid.DoF  # 5 or 6 depending on scale

    @property
    def shear(self) -> ShearTransform2D:
        """
        Get the shear transform

        Returns:
            The shear transform
        """
        return self._shear

    @property
    def scale(self) -> ScaleTransform2D:
        """
        Get the scale transform

        Returns:
            The scale transform
        """
        return self._scale

    @property
    def rigid(self) -> RigidTransform2D:
        """
        Get the rigid transform

        Returns:
            The rigid transform
        """
        return self._rigid    

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
        self.update_M()

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
        self.update_M()

    @property
    def shear_theta(self) -> float:
        """
        Get shear theta from the ShearTransform2D instance.

        Returns:
            The shear theta
        """
        return self._shear.theta

    @shear_theta.setter
    def shear_theta(self, new_theta: float) -> None:
        """
        Set shear theta in the ShearTransform2D instance.

        Args:
            new_theta: New theta
        """
        self._shear.theta = new_theta
        self.update_M()

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
        self.update_M()

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
        self.update_M()

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
        self.update_M()

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
        self.update_M()
        return rect

    def update_M(self) -> None:
        """
        Update M with instance variables.
        """
        super().reset()
        self._M = self._rigid.M @ self._scale.M @ self._shear.M

    def get_decomposed(self) -> Tuple[ShearTransform2D, ScaleTransform2D, RigidTransform2D]:
        """
        Decompose the matrix M into it's component shear, scale, and rigid matrices.
        Do this as if component matrices are unknown. Do not change M.

        Returns:
            (shear transform, scale transform, rigid transform)
        """
        # translate x, translate y
        tx, ty = self._M[0][2], self._M[1][2]
        # Rotation, Scale, SHear
        RSSH = self._M[:2, :2]
        # Scale, SHear
        SSH = np.linalg.cholesky(RSSH.T @ RSSH).T
        # scale x, scale y
        sx, sy = SSH[0][0], SSH[1][1]
        # normalize to isolate shear value which is tangent(theta)
        tan_theta = SSH[0][1] / sx
        # 2x2 rotation matrix
        R = RSSH @ np.linalg.inv(SSH)
        # Account for reflection
        if np.linalg.det(R) < 0:
            Z[0] *= -1
            ZS[0] *= -1
            R = RSSH @ np.linalg.inv(SSH)

        shear_theta = math.atan(tan_theta)
        shear = ShearTransform2D(shear_theta)
        scale = ScaleTransform2D(sx, sy)
        theta = math.atan2(R[1][0], R[0][0])
        rigid = RigidTransform2D(theta, tx, ty)
        return shear, scale, rigid
        

if __name__ == "__main__":
    pass
    