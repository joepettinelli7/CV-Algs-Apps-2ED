from typing import Optional
import math
import numpy as np
from src.transforms.transform_base import TransformBase2D


class ShearTransform2D(TransformBase2D):
    """
    Upper-triangular shear (not symmetric).
    Preserves: parallelism, straight lines.
    """

    def __init__(self, theta: float = 0.) -> None:
        """
        Default is no shear.

        Args:
            theta: Angle to shear in radians.
        """
        super().__init__()
        self._theta = theta
        self._M[0][1] = np.tan(theta)
        self._DoF = 1

    @property
    def theta(self) -> float:
        """
        Angle to shear lines in radians.

        Returns:
            Theta
        """
        return self._theta

    @theta.setter
    def theta(self, new_theta: float) -> None:
        """
        Set the new theta value.

        Args:
            new_theta: New theta in radians.
        """
        self._theta = new_theta
        self.update_M()

    def update_M(self) -> None:
        """
        Update M with instance variables.
        """
        super().reset()
        self._M[0][1] = np.tan(self._theta)

    def theta_from_M(self, m: Optional[np.ndarray] = None) -> float:
        """
        Use the matrix [0][1] position which is tan(theta),
        and take arctangent of that value to get theta.

        Args:
            m: Any matrix (but should be shear matrix)

        Returns:
            Theta
        """
        if m is None:
            return math.atan(self._M[0][1])
        else:
            return math.atan(m[0][1])


if __name__ == "__main__":
    pass
    