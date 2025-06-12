from typing import Optional, Tuple
import math
import numpy as np
from src.primitives.rectangle import Rectangle2D
from src.transforms.transform_base import TransformBase2D
from src.transforms.rigid import RigidTransform2D
from src.transforms.scale import ScaleTransform2D
from src.transforms.translation import TranslationTransform2D


class SimilarityTransform2D(TransformBase2D):
    """
    Composed of scale (uniform) + rigid transforms.
    Preserves: angles, parallelism, straight lines.
    """

    def __init__(self, sx: float = 1., sy: float = 1., theta: float = 0., tx: int = 0, ty: int = 0) -> None:
        """
        Default is no change.

        Args:
            sx: Scale in x direction
            sy: Scale in y direction
            theta: Rotation angle in radians
            tx: Translation x distance
            ty: Translation y distance
        """
        super().__init__()
        assert sx == sy  # uniform scaling
        self._scale = ScaleTransform2D(sx, sy)
        self._rigid = RigidTransform2D(theta, tx, ty)
        self._M: np.ndarray = self._rigid.M @ self._scale.M   # scale then rigid
        self._DoF: int = self._scale.DoF + self._rigid.DoF  # 4

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
    def theta(self) -> float:
        """
        Get theta from the RigidTransform2D instance.

        Returns:
            Theta in radians.
        """
        return self._rigid.theta

    @theta.setter
    def theta(self, new_theta: float) -> None:
        """
        Set theta in the RigidTransform2D instance.

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
        return self._tx

    @tx.setter
    def tx(self, new_tx: int) -> None:
        """
        Set new translation in x direction

        Args:
            new_tx: New translation distance
        """
        self._tx = new_tx
        self.update_M()

    @property
    def ty(self) -> int:
        """
        Translation in y direction

        Returns:
            Translation distance
        """
        return self._ty

    @ty.setter
    def ty(self, new_ty: int) -> None:
        """
        Set new translation in y direction

        Args:
            new_ty: New translation distance
        """
        self._ty = new_ty
        self.update_M()

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply similarity transform (scale then rigid) to the rectangle corners.

        Args:
            rect: Rectangle object

        Returns:
            The rectangle with similarity transformed corner points.
        """
        if not super().from_origin:
            center = rect.center
            to_origin = TranslationTransform2D(-center.x, -center.y)
            to_center = TranslationTransform2D(center.x, center.y)
            # Shift to origin, similarity, shift back to object center
            self._M = to_center.M @ self._M @ to_origin.M
        rect = super().apply_to_rectangle(rect)
        self.update_M()
        return rect

    def update_M(self) -> None:
        """
        Update M with instance variables.
        """
        super().reset()
        self._M = self._rigid.M @ self._scale.M

    def get_decomposed(self) -> Tuple[ScaleTransform2D, RigidTransform2D]:
        """
        Decompose the matrix M into it's component scale and rigid matrices.
        Do this as if component matrices are unknown. Do not change M.

        Returns:
            (scale transform, rigid transform)
        """
        s = math.sqrt(self._M[0][0]**2 + self._M[1][0]**2)
        scale = ScaleTransform2D(s, s)
        rotation_m = self._M[:2, :2] / s
        theta = math.atan2(rotation_m[1][0], rotation_m[0][0])
        tx, ty = self._M[0][2], self._M[1][2]
        rigid = RigidTransform2D(theta, tx, ty)
        return scale, rigid


if __name__ == "__main__":
    pass
    