import numpy as np
from src.transforms.transform_base import TransformBase2D
from src.transforms.affine import AffineTransform2D
from src.transforms.perspective import PerspectiveTransform2D
from src.transforms.translation import TranslationTransform2D
from src.primitives.rectangle import Rectangle2D


class ProjectiveTransform2D(TransformBase2D):
    """
    AKA perspective transform or homography. Contains a pure perspective
    transform + an affine transform. Preserves: straight lines.
    """

    def __init__(self, per_x: float = 0., per_y: float = 0., sx: float = 1., sy: float = 1.,
                 shear_theta: float = 0., theta: float = 0., tx: int = 0, ty: int = 0) -> None:
        """
        Default is no change.
        
        Args:
            per_x: Perspective x
            per_y: Perspective y
            sx: Scale x
            sy: Scale y
            shear_theta: Shear angle radians
            theta: Rotation angle radians
            tx: Translate x distance
            ty: Translate y distance
        """
        super().__init__()
        self._affine = AffineTransform2D(sx, sy, shear_theta, theta, tx, ty)
        self._perspective = PerspectiveTransform2D(per_x, per_y)
        self._M = self._perspective.M @ self._affine.M   # affine then perspective
        self._DoF = self._affine.DoF + self._perspective.DoF  # 8

    @property
    def per_x(self) -> float:
        """
        Get the perspective x value.

        Returns:
            Perspective x value
        """
        return self._perspective.per_x

    @per_x.setter
    def per_x(self, new_per_x: float) -> None:
        """
        Set the perspective x value.

        Args:
            new_per_x: New perspective x
        """
        self._perspective.per_x = new_per_x

    @property
    def per_y(self) -> float:
        """
        Get the perspective y value.

        Returns:
            Perspective y value
        """
        return self._perspective.per_y

    @per_y.setter
    def per_y(self, new_per_y: float) -> None:
        """
        Set the perspective y value.

        Args:
            new_per_y: New perspective y
        """
        self._perspective.per_y = new_per_y

    @property
    def sx(self) -> float:
        """
        Get the scale x value from ScaleTransform2D instance.

        Returns:
            Scale x factor
        """
        return self._affine.sx

    @sx.setter
    def sx(self, new_scale_x: float) -> None:
        """
        Set the scale x value in ScaleTransform2D instance.

        Args:
            new_scale_x: New scale factor
        """
        self._affine.sx = new_scale_x

    @property
    def sy(self) -> float:
        """
        Get the scale y value from ScaleTransform2D instance.

        Returns:
            Scale y factor
        """
        return self._affine.sy

    @sy.setter
    def sy(self, new_scale_y: float) -> None:
        """
        Set the scale y value in ScaleTransform2D instance.

        Args:
            new_scale_y: New scale factor
        """
        self._affine.sy = new_scale_y

    @property
    def shear_theta(self) -> float:
        """
        Get shear theta from the ShearTransform2D instance.

        Returns:
            The shear theta
        """
        return self._affine.theta

    @shear_theta.setter
    def shear_theta(self, new_shear_theta: float) -> None:
        """
        Set shear theta in the ShearTransform2D instance.

        Args:
            new_shear_theta: New shear theta
        """
        self._affine.theta = new_shear_theta

    @property
    def theta(self) -> float:
        """
        Get rotation theta from the RigidTransform2D instance.

        Returns:
            Theta in radians.
        """
        return self._affine.theta

    @theta.setter
    def theta(self, new_theta: float) -> None:
        """
        Set rotation theta in the RigidTransform2D instance.

        Args:
            theta: New theta in radians.
        """
        self._affine.theta = new_theta

    @property
    def tx(self) -> int:
        """
        Translation in x direction

        Returns:
            Translation distance
        """
        return self._affine.tx

    @tx.setter
    def tx(self, new_tx: int) -> None:
        """
        Set new translation in x direction

        Args:
            new_tx: New translation distance
        """
        self._affine.tx = new_tx

    @property
    def ty(self) -> int:
        """
        Translation in y direction

        Returns:
            Translation distance
        """
        return self._affine.ty

    @ty.setter
    def ty(self, new_ty: int) -> None:
        """
        Set new translation in y direction

        Args:
            new_ty: New translation distance
        """
        self._affine.ty = new_ty

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply perspective transform (affine + perspective) to the rectangle corners.

        Args:
            rect: Rectangle object

        Returns:
            The rectangle object with perspective transformed corner points.
        """
        if not super().from_origin:
            center = rect.center
            to_origin = TranslationTransform2D(-center.x, -center.y)
            to_center = TranslationTransform2D(center.x, center.y)
            # Shift to origin, projective, shift back to object center
            self._M = to_center.M @ self._M @ to_origin.M
        rect = super().apply_to_rectangle(rect)
        self.reset()
        return rect

    def reset(self) -> None:
        """
        Reset M with instance variables.
        """
        super().reset()
        self._M = self._perspective.M @ self._affine.M
        
        
if __name__ == "__main__":
    pass
  