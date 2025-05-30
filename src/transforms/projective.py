from src.transforms.transform_base import TransformBase2D


class ProjectiveTransform2D(TransformBase2D):
    """
    AKA perspective transform or homography.

    - matrix: [H bar]3x3
    - DoF: 8
    - preserves: straight lines
    """

    def __init__(self) -> None:
        """
        """
        pass

if __name__ == "__main__":
    pass
  