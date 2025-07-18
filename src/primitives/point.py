import math
import logging
from typing import Optional, Union, List
import numpy as np


class Point2D:
    """
    The class to represent a 2D point. Point2D is currently always
    homogenous (x, y, w) for simplicity. If w equals 1.0 this is equivalent
    to the cartesian coordinate, and if w equals 0.0 this is a point at infinity
    which has a direction with no fixed location. See page 30.
    """
    
    def __init__(self, x: float = 0.0, y: float = 0.0, w: float = 1.0) -> None:
        """
        """
        assert isinstance(x, float), f"Can't have {x.__class__}"
        assert isinstance(y, float), f"Can't have {y.__class__}"
        assert isinstance(w, float), f"Can't have {w.__class__}"
        self._x = x
        self._y = y
        if w == 0.0:
            logging.warning(" Created a point at infinity.")
        self._w = w

    def __repr__(self) -> str:
        """
        Use the vector / coordinates to represent the point.
        
        Returns:
            The column vector x, y, w.
        """
        return f"Point2D({self.vector})"

    @property
    def vector(self) -> np.ndarray:
        """
        Make a numpy array to represent a column vector.
        In the book, all point vectors are column vectors
        that post-multiply matrices unless specified.
        
        Returns:
            The (3, 1) shape column vector
        """
        return np.vstack([self._x, self._y, self._w])

    @property
    def cartesian_vector(self) -> Optional[np.ndarray]:
        """
        First need to normalize. Do not change instance
        variables, create new variables to return.

        Returns:
            The vector with only x and y (no w) with shape (2, 1)
        """
        cartesian_x = self._x / self._w
        cartesian_y = self._y / self._w
        return np.vstack([cartesian_x, cartesian_y])

    @property
    def x(self) -> float:
        """
        
        Returns:
            The x coordinate
        """
        return self._x

    @property
    def y(self) -> float:
        """

        Returns:
            The y coordinate
        """
        return self._y

    @property
    def w(self) -> float:
        """
        A homogenous coordinate with w = 1.0 
        is equivalent to cartesian (x, y). When w = 0.0,
        this is a point at infinity.
        
        Returns:
            The w coordinate
        """
        return self._w

    @x.setter
    def x(self, new_x: float) -> None:
        """
        Set x value
        
        Args:
            new_x: New x value
        """
        self._x = new_x

    @y.setter
    def y(self, new_y: float) -> None:
        """
        Set y value

        Args:
            new_y: New y value
        """
        self._y = new_y

    @w.setter
    def w(self, new_w: float) -> None:
        """
        Set w value

        Args:
            new_w: New w value
        """
        if new_w == 0.0:
            logging.warning(" Created a point at infinity.")
        self._w = new_w
    
    def homogenize(self, w: Union[int, float] = 1.0) -> None:
        """
        In-place scale all values by w.

        Args:
            w: The scaling factor.
        """
        if isinstance(w, int):
            w = float(w)
        self._x *= w
        self._y *= w
        self._w *= w
    
    def to_int(self, inplace: bool = True) -> Optional["Point2D"]:
        """
        Convert x, y to integer inplace and maintain w.
        """
        new_x = int(round(self._x / self._w) * self._w)
        new_y = int(round(self._y / self._w) * self._w)
        if inplace:
            self._x = new_x
            self._y = new_y
        else:
            return Point2D(new_x, new_y, self._w)
    
    def normalize(self) -> None:
        """
        In-place normalize homogenous point so that w = 1.
        """
        if self._w != 0.0:
            self._x /= self._w
            self._y /= self._w
            self._w /= self._w
        else:
            logging.warning(" Point was at infinity, so aborted normalize.")

    def normalized(self) -> Optional["Point2D"]:
        """
        Normalize homogenous point so that w = 1.

        Returns:
            New instance of point that is normalized
        """
        if self._w != 0.0:
            norm_x = self._x / self._w
            norm_y = self._y / self._w
            norm_w = self._w / self._w
            return Point2D(norm_x, norm_y, norm_w)
        else:
            logging.warning(" Point was at infinity, so aborted normalize.")

    def copy(self) -> "Point2D":
        """
        Make a copy of point with equal x, y, w.

        Returns:
            New point object.
        """
        x, y, w = self._x, self._y, self._w
        return Point2D(x, y, w)
    
    def apply_transform(self, M: np.ndarray, inplace: bool = False) -> "Point2D":
        """
        Apply the transform to the point. Use the M property
        which contains the numpy array matrix.

        Args:
            M: The transform matrix.
            inplace: If True, change x, y, z of this instance, else return new point instance.
                     * Be careful when True because it can lead to a compounding effect when
                     multiple transformations are applied to the same point inadvertently. *

        Returns:
            Either self or a new Point2D instance.
        """
        transformed = np.dot(M, self.vector)
        x, y, w = transformed[0][0].item(), transformed[1][0].item(), transformed[2][0].item()
        if inplace:
            self._x, self._y, self._w = x, y, w
            return self
        else:
            return Point2D(x, y, w)
    
    def __eq__(self, other: "Point2D") -> bool:
        """
        Determine whether the points are equivalent.
        
        For points to be equivalent, x and y are equivalent (For homogenous points,
        vectors that differ only by w are still considered to be equivalent).

        Args:
            other: The other point

        Returns:
            True if points are equivalent
        """
        if self._w == 0.0 or other.w == 0.0:
            x_eq = math.isclose(self._x, other.x, abs_tol=1e-8)
            y_eq = math.isclose(self._y, other.y, abs_tol=1e-8)
        else:
            x_eq = math.isclose(self._x / self._w, other.x / other.w, abs_tol=1e-8)
            y_eq = math.isclose(self._y / self._w, other.y / other.w, abs_tol=1e-8)
        return x_eq and y_eq

    def __hash__(self) -> int:
        """
        Get the hash value for the point. If two points are
        __eq__  then the hash value must be the same. Round to 8
        decimal places to match __eq__. Very small chance of collision.

        Returns:
            An integer hash value.
        """
        if self._w == 0:
            return hash((round(self._x, 8), round(self._y, 8), 0))
        else:
            norm_x = self._x / self._w
            norm_y = self._y / self._w
            return hash((round(norm_x, 8), round(norm_y, 8), 1))
    
    def __add__(self, other: "Point2D") -> "Point2D":
        """
        Add point with point
            - point + point = point (in cartesian space)*
            - point + vector = translated point
            - vector + vector = vector

        Args:
            other: The other point or vector

        Returns:
            New instance that is sum of both points
        """
        assert isinstance(other, Point2D), f"Other point is type {other.__class__}."
        if self._w == 0.0 or other.w == 0.0:
            x_sum = self._x + other.x
            y_sum = self._y + other.y
            w_sum = self._w + other.w
        else:
            # point + point (normalize to w=1 then add x, y)
            # currently only used to find rectangle center.
            self_norm = self.normalized()
            other_norm = other.normalized()
            x_sum = (self_norm.x + other_norm.x)
            y_sum = (self_norm.y + other_norm.y)
            w_sum = 1.0
        return Point2D(x_sum, y_sum, w_sum)

    def __iadd__(self, other: "Point2D") -> "Point2D":
        """
        In-place add points with same logic as __add__.

        Args:
            other: The other point

        Returns:
            The same instance that is sum of both points
        """
        assert isinstance(other, Point2D), f"Other point is type {other.__class__}."
        if self._w == 0.0 or other.w == 0.0:
            self._x += other.x
            self._y += other.y
            self._w += other.w
            return self
        else:
            # point + point
            raise NotImplementedError

    def __sub__(self, other: "Point2D") -> "Point2D":
        """
        Subtract other from point
            - point - point = vector
            - point - vector = translated point
            - vector - vector = vector

        Args:
            other: The other point

        Returns:
            New instance that is difference of the points
        """
        assert isinstance(other, Point2D), f"Other point is type {other.__class__}."
        if self._w == 0.0 or other.w == 0.0:
            x_diff = self._x - other.x
            y_diff = self._y - other.y
            w_diff = self._w - other.w
        else:
            # point - point
            assert self._w == 1.0 and other.w == 1.0, "Not implemented yet."
            x_diff = self._x - other.x
            y_diff = self._y - other.y
            w_diff = 0.0
        return Point2D(x_diff, y_diff, w_diff)

    def __isub__(self, other: "Point2D") -> Optional["Point2D"]:
        """
        In-place subtract points with same logic as __sub__.

        Args:
            other: The other point

        Returns:
            The same instance that is difference of the points
        """
        assert isinstance(other, Point2D), f"Other point is type {other.__class__}."
        if self._w == 0.0 or other.w == 0.0:
            self._x -= other.x
            self._y -= other.y
            self._w -= other.w
        else:
            # point - point
            assert self._w == 1.0 and other.w == 1.0, "Not implemented yet."
            self._x -= other.x
            self._y -= other.y
            self._w = 0.0
        return self

    def __truediv__(self, other: int) -> "Point2D":
        """
        Only implemented to be used when finding center point of points
        like in the Rectangle2D class.

        Args:
            other: Number to divide by

        Returns:
            A new object of point
        """
        assert other != 0
        assert self._w == 1.0
        new_x = self._x / other
        new_y = self._y / other
        return Point2D(new_x, new_y, self._w)


class Point3D(Point2D):

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 1.0) -> None:
        super().__init__(x=x, y=y, w=w)
        assert isinstance(z, float), f"Can't have {z.__class__}"
        self._z = z

    @property
    def z(self) -> float:
        """
        """
        return self._z
        

if __name__ == "__main__":
    pass
    