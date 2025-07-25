from src.transforms.transform_base import TransformBase2D


class PerspectiveTransform2D(TransformBase2D):
    """
    PURE perspective transform used to COMPOSE THE 
    PROJECTIVE transform along with the affine transform.
    Preserves: straight lines.
    """

    def __init__(self, per_x: float = 0., per_y: float = 0.) -> None:
        """
        Default is no change.

        Args:
            per_x: Perspective x value
            per_y: Perspective y value
        """
        super().__init__()
        self._per_x = per_x
        self._per_y = per_y
        self._M[2][0] = per_x
        self._M[2][1] = per_y
        self._DoF = 2

    @property
    def per_x(self) -> float:
        """
        Get the perspective x value.

        Returns:
            Perspective x value
        """
        return self._per_x

    @per_x.setter
    def per_x(self, new_per_x: float) -> None:
        """
        Set the perspective x value.

        Args:
            new_per_x: New perspective x
        """
        self._per_x = new_per_x
        self.update_M()

    @property
    def per_y(self) -> float:
        """
        Get the perspective y value.

        Returns:
            Perspective y value
        """
        return self._per_y

    @per_y.setter
    def per_y(self, new_per_y: float) -> None:
        """
        Set the perspective y value.

        Args:
            new_per_y: New perspective y
        """
        self._per_y = new_per_y
        self.update_M()

    def update_M(self) -> None:
        """
        Reset M with instance variables.
        """
        super().reset()
        self._M[2][0] = self._per_x
        self._M[2][1] = self._per_y


if __name__ == "__main__":
    pass
    