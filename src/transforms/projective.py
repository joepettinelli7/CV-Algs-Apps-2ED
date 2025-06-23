from typing import Tuple
import numpy as np
from scipy.optimize import minimize
from src.transforms.transform_base import TransformBase2D
from src.transforms.affine import AffineTransform2D
from src.transforms.perspective import PerspectiveTransform2D


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
        self._DoF = self._affine.DoF + self._perspective.DoF  # 8 or 9 depending on scale
    
    @property
    def affine(self) -> AffineTransform2D:
        """
        Get the affine transform

        Returns:
            The affine transform
        """
        return self._affine

    @property
    def perspective(self) -> PerspectiveTransform2D:
        """
        Get the perspective transform

        Returns:
            The perspective transform
        """
        return self._perspective

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
        self.update_M()

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
        self.update_M()

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
        self.update_M()

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
        self.update_M()

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
        self.update_M()

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
        self.update_M()

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
        self.update_M()

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
        self.update_M()

    def update_M(self) -> None:
        """
        Reset M with instance variables.
        """
        super().reset()
        self._M = self._perspective.M @ self._affine.M
    
    def get_decomposed(self) -> Tuple[AffineTransform2D, PerspectiveTransform2D]:
        """
        This function acts as a wrapper to get_decomposed_from_M which
        is the static version of this function and does calculations.

        Returns:
            (affine transform, perspective transform)
        """
        return self.get_decomposed_from_M(self._M)
    
    @staticmethod
    def get_decomposed_from_M(M: np.ndarray) -> Tuple[AffineTransform2D, PerspectiveTransform2D]:
        """
        Decompose the matrix M into it's component affine and perspective matrices.
        Do this as if component matrices are unknown. Do not change M.

        Args:
            M: The projective transform matrix.

        Returns:
            (affine transform, perspective transform)
        """
        
        def error(params: Tuple[float, float]) -> float:
            """
            Find the error between estimated affine last row
            and expected last row which is 0, 0, 1 for an affine
            transform matrix because there is no perspective transform.
            
            Args:
                params: Unpacks into perspective x and perspective y.

            Returns:
                The error between estimated affine last row and 0, 0, 1.
            """
            per_x, per_y = params
            temp_per = PerspectiveTransform2D(per_x, per_y)
            affine_est = np.linalg.inv(temp_per.M) @ M
            last_row = affine_est[2]
            return np.linalg.norm(last_row - np.array([0, 0, 1]))
        
        # Initialize optimizer with reasonable estimates.
        per_x0 = M[2, 0] / M[2, 2]
        per_y0 = M[2, 1] / M[2, 2]
        result = minimize(error, x0=[per_x0, per_y0])
        per_x, per_y = result.x
        perspective = PerspectiveTransform2D(per_x, per_y)
        # Extract the affine transform matrix using perspective
        affine_M = np.linalg.inv(perspective.M) @ M
        affine = AffineTransform2D.from_M(affine_M)
        return affine, perspective
    
    @classmethod
    def from_M(cls, M: np.ndarray) -> "ProjectiveTransform2D":
        """
        Construct a ProjectiveTransform2D object
        from a 3x3 affine matrix by decomposing it.

        Args:
            M: A 3x3 matrix.

        Returns:
            A ProjectiveTransform2D instance.
        """
        assert M.shape == (3, 3)
        a, p = cls.get_decomposed_from_M(M)
        return cls(p.per_x, p.per_y, a.sx, a.sy, a.shear_theta, a.theta, a.tx, a.ty)
        

if __name__ == "__main__":
    pass
  