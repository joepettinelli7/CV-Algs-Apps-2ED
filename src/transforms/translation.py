import numpy as np
from src.transforms.transform_base import TransformBase2D


class TranslationTransform2D(TransformBase2D):
    """
    Preserves: orientation, lengths, angles, parallelism, straight lines.
    """

    def __init__(self, tx: int = 0., ty: int = 0.) -> None:
        """
        
        """
        super().__init__()
        self._t_vector = np.vstack([tx, ty])  # Translation vector [x shift, y shift]
        self._M[0][2] = tx
        self._M[1][2] = ty
        self._DoF = 2

    @property
    def t_vector(self) -> np.ndarray[int, int]:
        """
        """
        return self._t_vector

    @t_vector.setter
    def t_vector(self, new_t_vector: np.ndarray) -> None:
        """
        """
        self._t_vector = new_t_vector

    @property
    def tx(self) -> int:
        """
        """
        return self._t_vector[0]

    @tx.setter
    def tx(self, new_tx: int) -> None:
        """
        """
        self._t_vector[0] = new_tx

    @property
    def ty(self) -> int:
        """
        """
        return self._t_vector[1]

    @ty.setter
    def ty(self, new_ty: int) -> None:
        """
        """
        self._t_vector[1] = new_ty

    def update_M(self) -> None:
        """
        Update M with current translation vector
        """
        self._M[0][2] = self._t_vector[0]
        self._M[1][2] = self._t_vector[1]


if __name__ == "__main__":
    pass
    