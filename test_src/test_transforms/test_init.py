import pytest
from src.transforms import *


def test_import() -> None:
    """
    """
    affine = AffineTransform2D()
    perspective = PerspectiveTransform2D()
    projective = ProjectiveTransform2D()
    rigid = RigidTransform2D()
    rotation = RotationTransform2D()
    scale = ScaleTransform2D()
    shear = ShearTransform2D()
    similarity = SimilarityTransform2D()
    transform_base = TransformBase2D()
    translation = TranslationTransform2D()


if __name__ == "__main__":
    pass
    