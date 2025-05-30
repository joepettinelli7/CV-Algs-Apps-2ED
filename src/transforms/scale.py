from src.transforms.transform_base import TransformBase2D
from src.transforms.translation import TranslationTransform2D
from src.primitives.rectangle import Rectangle2D


class ScaleTransform2D(TransformBase2D):
    """
    Non-uniform scaling. Used in affine transform but not similarity.
    Preserves: orientation, angles, parallelism, straight lines.
    """

    def __init__(self, sx: float = 1., sy: float = 1., from_origin: bool = False) -> None:
        """
        By default, will scale from object center. If from_origin is True,
        then object will appear to scale and translate.
        """
        super().__init__()
        self._sx = sx
        self._sy = sy
        self._from_origin = from_origin
        self._M[0][0] = sx
        self._M[1][1] = sy
        self._DoF = 1

    @property
    def sx(self) -> None:
        """
        """
        return self._sx

    @sx.setter
    def sx(self, new_sx: float) -> None:
        """
        """
        self._sx = new_sx
    
    @property
    def sy(self) -> None:
        """
        """
        return self._sy

    @sy.setter
    def sy(self, new_sy: float) -> None:
        """
        """
        self._sy = new_sy

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
        Apply scale to the rectangle corners

        Args:
            rect: Rectangle object

        Returns:
            The scaled corner points
        """
        if not self._from_origin:
            # Update matrix
            center = rect.center
            translation_to_orig = TranslationTransform2D(tx=-center.x, ty=-center.y)
            translation_to_center = TranslationTransform2D(tx=center.x, ty=center.y)
            # Shift to origin, scale, shift back to object center
            self._M = translation_to_center.M @ self._M @ translation_to_orig.M
        rect = super().apply_to_rectangle(rect=rect)
        return rect

    def update_M(self) -> None:
        """
        Update M with current scale value
        """
        self._M[0][0] = self._sx
        self._M[1][1] = self._sy


if __name__ == "__main__":
    pass
    