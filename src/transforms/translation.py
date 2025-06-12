import numpy as np
from src.primitives.rectangle import Rectangle2D
from src.transforms.transform_base import TransformBase2D


class TranslationTransform2D(TransformBase2D):
    """
    Preserves: orientation, lengths, angles, parallelism, straight lines.
    """

    def __init__(self, tx: int = 0, ty: int = 0) -> None:
        """
        Default is no translation.

        Args:
            tx: x translation distance
            ty: y translation distance
        """
        super().__init__()
        self._tx = tx
        self._ty = ty
        self._M[0][2] = tx
        self._M[1][2] = ty
        self._DoF = 2

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
        and update M to synchronize.

        Args:
            new_tx: New translation distance
        """
        self._tx = new_tx
        self._M[0][2] = new_tx

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
        and update M to synchronize.

        Args:
            new_ty: New translation distance
        """
        self._ty = new_ty
        self._M[1][2] = new_ty

    def apply_to_rectangle(self, rect: Rectangle2D) -> Rectangle2D:
        """
        Apply translation to the rectangle corners.

        Args:
            rect: Rectangle object

        Returns:
            The rectangle with translated corner points.
        """
        return super().apply_to_rectangle(rect)

    def update_M(self) -> None:
        """
        Update M with current instance variables.
        """
        self._M[0][2] = self._tx
        self._M[1][2] = self._ty


if __name__ == "__main__":
    pass
    