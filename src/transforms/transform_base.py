from typing import Optional, List, Any
import numpy as np
import math


class TransformBase2D:
    """
    Base class for all other transforms. Currently implemented
    for 2D homogenous coordinates. In subclasses of this class,
    use the names from all_components when naming instance variables.
    """
    
    all_components = ["_translation", "_rotation", "_scale", "_shear",
                      "_perspective", "_rigid", "_similarity", "_affine"]

    def __init__(self) -> None:
        """
        Initialize with 3x3 identity matrix and set degrees of
        freedom to -1. By default, objects will be transformed
        from their center (not from the canvas origin).
        """
        self._M: np.ndarray = np.array([
            [1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]], dtype=float)
        self._DoF: int = -1
        self._from_origin: bool = False
    
    def __repr__(self) -> str:
        """
        Use the matrix to represent transform.
    
        Returns:
            The transform name and the matrix along with
            the transforms that compose the transform.
        """
        formatter = {'float_kind': lambda x: "%.4f" % x}
        matrix_str = np.array2string(self._M, formatter=formatter, prefix='    ', separator='  ')
        rep = f"{self.__class__.__name__}:\n    {matrix_str}"
        components = self.get_components()
        if components:
            rep += "\ncomposed of:"
            for comp in components:
                comp_matrix = np.array2string(comp.M, formatter=formatter, prefix='    ', separator='  ')
                rep += f"\n{comp.__class__.__name__}:\n    {comp_matrix}"
        rep += "\n"
        return rep
    
    @property
    def M(self) -> np.ndarray:
        """
        The transformation matrix.

        Returns:
            3x3 numpy array
        """
        return self._M

    @M.setter
    def M(self, new_M: np.ndarray) -> None:
        """
        Set the matrix M.

        Args:
            new_M: The new matrix to set.
        """
        self._M = new_M

    @property
    def DoF(self) -> int:
        """
        Degrees of freedom (number of values needed
        to constuct the transform matrix).
        
        Returns:
            Degrees of freedom
        """
        return self._DoF

    @DoF.setter
    def DoF(self, new_DoF: int) -> None:
        """
        Set the degrees of freedom.
        
        Args:
            new_DoF: New degrees of freedom
        """
        self._DoF = new_DoF

    @property
    def from_origin(self) -> bool:
        """
        Whether to apply the transform from origin
        or from the object center.

        Returns:
            True if transform should be applied from
            the canvas origin. False for object center.
        """
        return self._from_origin

    @from_origin.setter
    def from_origin(self, new_from_origin: bool) -> None:
        """
        Set new value.

        Args:
            new_from_origin: Whether to transform object from
                             canvas origin or object center.
        """
        self._from_origin = new_from_origin

    def reset(self) -> None:
        """
        Reset M to the same 3x3 identity matrix that
        the instance was initialized with.
        """
        self._M = np.identity(3, dtype=float)
    
    def get_components(self) -> List["TransformBase2D"]:
        """
        Get the transforms (subclasses of TransformBase2D) that
        compose the transform. For example, rigid is composed
        of rotation + translation. This is when transforms are
        built using the components (NOT when started with M).

        Returns:
            The transform component transforms.
        """
        instance_vars = vars(self)
        components = [value for key, value in instance_vars.items() if key in self.all_components]
        return components

    def to_degrees(self, radians: float) -> float:
        """
        Convert radians to degrees. Needed for rotation
        and shear transformations which both have a theta parameter.

        Args:
            radians: Radians

        Returns:
            Degrees
        """
        return radians * (180 / math.pi)

    def to_radians(self, degrees: float) -> float:
        """
        Convert degrees to radians. Needed for rotation
        and shear transformations which both have a theta parameter.

        Args:
            degrees: Degrees

        Returns:
            Radians
        """
        return degrees * (math.pi / 180)

    def get_T_inv_M(self) -> np.ndarray:
        """
        Get the transposed inverse of M. This matrix
        represents the transformation on a co-vector such
        as a 2D line or 3D normal (page 34).

        Returns:
            The transposed inverse (M^-1)^T.
        """
        return np.linalg.inv(self._M).T

    def get_inv_M(self) -> np.ndarray:
        """
        Get the inverse of M, which can be used to
        reverse the transformation applied with M.

        Returns:
            The inverse (M^-1).
        """
        return np.linalg.inv(self._M)

    def get_decomposed(self) -> Any:
        """
        Implemented for rigid, similarity, affine,
        and projective transformation subclasses.
        """
        raise NotImplementedError

    def __eq__(self, other: "TransformBase2D") -> bool:
        """
        Determine whether two transform matrices are equal.

        Args:
            other: Another transform matrix of TransformBase2D or subclass.
        
        Returns:
            True if equal, False if not equal.
        """
        return np.allclose(self._M, other.M)

    def normalize_M(self) -> None:
        """
        Normalize by dividing M by bottom right value.
        This will only change M if it is a projective
        transform because the bottom row will not be 0, 0, 1.
        Change M inplace.
        """
        self._M / self._M[2, 2]
    
    @property
    def normalized_M(self) -> np.ndarray:
        """
        Normalize M and return new numpy array.

        Returns:
            The transform matrix with bottom right value equal to 1.
        """
        return self._M / self._M[2, 2]
        
        
if __name__ == "__main__":
    pass
