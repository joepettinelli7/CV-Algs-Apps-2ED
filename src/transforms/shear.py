import numpy as np
from src.transforms.transform_base import TransformBase2D
from src.transforms.translation import TranslationTransform2D
from src.primitives.rectangle import Rectangle2D


class ShearTransform2D(TransformBase2D):
    """
    Preserves: parallelism, straight lines.
    """

    def __init__(self, theta: float = 0., from_origin: bool = False) -> None:
        """
        By default, will shear from object center. If from_origin is True,
        then object will appear to shear and translate.

        Args:
            theta: Radians
        """
        super().__init__()
        self._shear_val = np.tan(theta)
        self._from_origin = from_origin
        self._M[0][1] = np.tan(theta)
        self._DoF = 1

    @property
    def shear_val(self) -> None:
        """
        """
        return self._shear_val

    @shear_val.setter
    def shear_val(self, new_shear_val: float) -> None:
        """
        """
        self._shear_val = new_shear_val

    @property
    def from_origin(self) -> bool:
        """
        """
        return self._from_origin

    @from_origin.setter
    def from_origin(self, new_from_origin: bool) -> None:
        """
        """
        self._from_origin = new_from_origin

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply shear to the rectangle corners

        Args:
            rect: Rectangle object

        Returns:
            The sheared corner points
        """
        if not self._from_origin:
            # Update matrix
            center = rect.center
            translation_to_orig = TranslationTransform2D(tx=-center.x, ty=-center.y)
            translation_to_center = TranslationTransform2D(tx=center.x, ty=center.y)
            # Shift to origin, shear, shift back to object center
            self._M = translation_to_center.M @ self._M @ translation_to_orig.M
        rect = super().apply_to_rectangle(rect=rect)
        return rect

    def update_M(self) -> None:
        """
        Update M with current shear scalar
        """
        self._M[0][1] = self._shear_val


if __name__ == "__main__":
    pass
    