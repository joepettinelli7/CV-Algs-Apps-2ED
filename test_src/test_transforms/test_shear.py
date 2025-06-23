import pytest
import math
from src.transforms.shear import ShearTransform2D


class TestShearTransform2D:

    @pytest.mark.parametrize("theta", (0.79, 0.39))
    def test_theta_from_M(self, theta: float) -> None:
        """
        """
        shear = ShearTransform2D(theta)
        calculated_theta = shear.theta_from_M()
        assert math.isclose(calculated_theta, theta)  # for rounding errors


if __name__ == "__main__":
    pass
    