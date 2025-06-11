from src.transforms.transform_base import TransformBase2D
from src.transforms.translation import TranslationTransform2D
from src.primitives.rectangle import Rectangle2D


class ScaleTransform2D(TransformBase2D):
    """
    Non-uniform scaling (can scale differently in x and y directions),
    and is used in affine transform but not similarity transform.
    Preserves: orientation, angles, parallelism, straight lines.
    """

    def __init__(self, sx: float = 1., sy: float = 1.) -> None:
        """
        Default is no scaling.

        Args:
            sx: Scale in x direction
            sy: Scale in y direction
        """
        super().__init__()
        self._sx = sx
        self._sy = sy
        self._M[0][0] = sx
        self._M[1][1] = sy
        if sx == sy:
            self._DoF = 1  # uniform
        else:
            self._DoF = 2  # non-uniform

    @property
    def sx(self) -> float:
        """
        Scale factor in x direction

        Returns:
            Scale factor
        """
        return self._sx

    @sx.setter
    def sx(self, new_sx: float) -> None:
        """
        Set the new scale factor in x direction

        Args:
            new_sx: New scale factor
        """
        self._sx = new_sx
    
    @property
    def sy(self) -> None:
        """
        Scale factor in y direction

        Returns:
            Scale factor
        """
        return self._sy

    @sy.setter
    def sy(self, new_sy: float) -> None:
        """
        Set the new scale factor in y direction

        Args:
            new_sy: New scale factor
        """
        self._sy = new_sy

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply scale to the rectangle corners.

        Args:
            rect: Rectangle object

        Returns:
            The rectangle with scaled corner points.
        """
        if not super().from_origin:
            center = rect.center
            to_origin = TranslationTransform2D(-center.x, -center.y)
            to_center = TranslationTransform2D(center.x, center.y)
            # Shift to origin, scale, shift back to object center
            self._M = to_center.M @ self._M @ to_origin.M
        rect = super().apply_to_rectangle(rect)
        self.reset()
        return rect

    def reset(self) -> None:
        """
        Reset M with instance variables.
        """
        super().reset()
        self._M[0][0] = self._sx
        self._M[1][1] = self._sy


if __name__ == "__main__":
    pass
    