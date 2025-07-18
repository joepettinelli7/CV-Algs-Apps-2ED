from typing import Optional
import math
import numpy as np
from src.transforms.transform_base import TransformBase2D


class RotationTransform2D(TransformBase2D):
    """
    Preserves: lengths, angles, parallelism, straight lines.
    """

    def __init__(self, theta: float = 0.) -> None:
        """
        Default is no rotation.

        Args:
            Theta: Rotation angle in radians
        """
        super().__init__()
        self._theta = theta
        self._M[0][0] = math.cos(theta)
        self._M[0][1] = -math.sin(theta)
        self._M[1][0] = math.sin(theta)
        self._M[1][1] = math.cos(theta)
        self._DoF = 1

    @property
    def theta(self) -> float:
        """
        The rotion angle in radians

        Returns:
            Theta
        """
        return self._theta

    @theta.setter
    def theta(self, new_theta: float) -> None:
        """
        Set the rotation angle in radians. Also update
        the matrix with new theta to synchronize.

        Args:
            new_theta: New theta
        """
        self._theta = new_theta
        self.update_M()

    def update_M(self) -> None:
        """
        Update M with instance variables.
        """
        super().reset()
        self._M[0][0] = math.cos(self._theta)
        self._M[0][1] = -math.sin(self._theta)
        self._M[1][0] = math.sin(self._theta)
        self._M[1][1] = math.cos(self._theta)

    def theta_from_M(self, m: Optional[np.ndarray] = None) -> float:
        """
        Use the matrix [1][0] position which is sin(theta), and
        [0][0] position which is cos(theta). Take arctangent2 of
        those values to get theta.

        Args:
            m: Any matrix (but should be rotation matrix)

        Returns:
            Theta
        """
        if m is None:
            return math.atan2(self._M[1][0], self._M[0][0])
        else:
            return math.atan2(m[1][0], m[0][0])
        
        
if __name__ == "__main__":
    pass
    