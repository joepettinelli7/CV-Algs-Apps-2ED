import math
from typing import Optional
import numpy as np
from src.primitives.point import Point2D
from src.primitives_lists.points import Points2D
from src.transforms.transform_base import TransformBase2D
from src.transforms.translation import TranslationTransform2D


class Rectangle2D:
    """
    The class to represent a 2D rectangle. Only define the rectangle with
    4 corner points, so that the corner points can be transformed with any of the
    transforms and redrawn with lines. Currently, all point w should be the same.
    """

    def __init__(self, left_top: Point2D, right_top: Point2D, right_bottom: Point2D, left_bottom: Point2D) -> None:
        """
        """
        self._left_top = left_top
        self._right_top = right_top
        self._right_bottom = right_bottom
        self._left_bottom = left_bottom

    def __repr__(self) -> str:
        """
        Use the corner points to represent the rectangle.
        
        Returns:
            The corners
        """
        return f"Rectangle2D({self.corners})"
    
    @property
    def left_top(self) -> Point2D:
        """

        Returns:
            Rectangle left top
        """
        return self._left_top

    @property
    def right_top(self) -> Point2D:
        """

        Returns:
            Rectangle right top
        """
        return self._right_top

    @property
    def right_bottom(self) -> Point2D:
        """

        Returns:
            Rectangle right bottom
        """
        return self._right_bottom

    @property
    def left_bottom(self) -> Point2D:
        """

        Returns:
            Rectangle left bottom
        """
        return self._left_bottom

    @left_top.setter
    def left_top(self, new_point: Point2D) -> None:
        """
        Set rectangle left top.

        Args:
            new_point: New left top point
        """
        self._left_top = new_point

    @right_top.setter
    def right_top(self, new_point: Point2D) -> None:
        """
        Set rectangle right top.

        Args:
            new_point: New right top point
        """
        self._right_top = new_point

    @right_bottom.setter
    def right_bottom(self, new_point: Point2D) -> None:
        """
        Set rectangle right bottom.

        Args:
            new_point: New right bottom point
        """
        self._right_bottom = new_point

    @left_bottom.setter
    def left_bottom(self, new_point: Point2D) -> None:
        """
        Set rectangle left bottom.

        Args:
            new_point: New left bottom point
        """
        self._left_bottom = new_point
    
    @property
    def width(self) -> int:
        """
        Get rectangle width using left top and right top.
        Use distance because rectangle may not be parallel with
        the canvas.

        Returns:
            The width
        """
        d = math.dist((self._left_top.x, self._left_top.y), (self._right_top.x, self._right_top.y))
        return round(d)
    
    @property
    def height(self) -> int:
        """
        Get rectangle height using left top and left bottom.
        Use distance because rectangle may not be parallel with
        the canvas.

        Returns:
            The height
        """
        d = math.dist((self._left_top.x, self._left_top.y), (self._left_bottom.x, self._left_bottom.y))
        return round(d)

    def to_int(self) -> None:
        """
        Convert the points to integers.
        """
        self._left_top.to_int()
        self._right_top.to_int()
        self._right_bottom.to_int()
        self._left_bottom.to_int()
    
    @property
    def is_true_rectangle(self) -> bool:
        """
        The opposite sides must be parallel and the
        adjacent sides must be at 90 degrees.
        """
        raise NotImplementedError
    
    @property
    def corners(self) -> Points2D:
        """
        Left top, right top, right bottom, left bottom (clockwise).
        
        Returns:
            Corner points of the rectangle.
        """
        return Points2D([self._left_top, self._right_top, self._right_bottom, self._left_bottom])

    @property
    def center(self) -> Point2D:
        """
        Center of rectangle by average of corners.
        This should be normalized to cartesian coords
        with w = 1.

        Returns:
            Rectangle center point.
        """
        p_sum: Point2D = Point2D()
        for p in self.corners:
            p_sum = p_sum + p
        return p_sum / 4

    def copy(self) -> "Rectangle2D":
        """
        Make a copy of rectangle with equal points.

        Returns:
            New rectangle object.
        """
        left_top = self._left_top.copy()
        right_top = self._right_top.copy()
        right_bottom = self._right_bottom.copy()
        left_bottom = self._left_bottom.copy()
        return Rectangle2D(left_top, right_top, right_bottom, left_bottom)
    
    def apply_transform(self, transform: TransformBase2D, inplace: bool = False) -> "Rectangle2D":
        """
        Apply the transform to the rectangle. Use the M property
        which contains the numpy array matrix. Also consider the
        from_origin property.

        Args:
            transform: The transform object (usually a subclass of TransformBase2D).
            inplace: If True return self, else return new Rectangle2D instance.

        Returns:
            Either self or new Rectangle2D instance.
        """
        M = transform.M
        if not transform.from_origin:
            M = self.get_transform_from_center(M)
        transformed_corners: Points2D = self.corners.apply_transform(M, inplace=inplace)
        if inplace:
            for idx, transformed_corner in enumerate(transformed_corners):
                self[idx] = transformed_corner
            return self
        else:
            rect = Rectangle2D(*transformed_corners)
            return rect
    
    def get_transform_from_center(self, M: np.ndarray) -> np.ndarray:
        """
        Get the transform matrix that will transform
        the rectangle around the rectangle center. Need
        to translate to origin, apply transform, then
        translate back to the object center.

        Args:
            M: The M that would apply translation to origin.

        Returns:
            The new transform matrix.
        """
        cx, cy = self.center.x, self.center.y
        to_origin = TranslationTransform2D(-cx, -cy)
        to_center = TranslationTransform2D(cx, cy)
        return to_center.M @ M @ to_origin.M
    
    def __getitem__(self, corner_index: int) -> Point2D:
        """
        Get the corner point based on corner_index. Positions are
        clockwise starting with left_top being 0 index.

        Args:
            corner_index: Corner to get.

        Returns:
            The point object representing the corner.
        """
        if corner_index <= 3:
            return self.corners[corner_index]
        else:
            raise IndexError(f"Corner index must be 0-3, not {corner_index}.")

    def __setitem__(self, corner_index: int, corner_point: Point2D) -> None:
        """
        Set the corner_point based on corner_index. Positions are
        clockwise starting with left_top being 0 index.

        Args:
            corner_index: Corner index to set.
            corner_point: The new corner point.

        Returns:
        
        """
        if corner_index == 0:
            self._left_top = corner_point
        elif corner_index == 1:
            self._right_top = corner_point
        elif corner_index ==2:
            self._right_bottom = corner_point
        elif corner_index == 3:
            self._left_bottom = corner_point
        else:
            raise IndexError(f"Corner index must be 0-3, not {corner_index}.")
    
    def __eq__(self, other: "Rectangle2D") -> bool:
        """
        Check whether two rectangles are equal. Need to account
        for all corners being the same even if not in the same order.

        * Very sensitive to small float differences.

        Args:
            other: The other rectangle object.

        Returns:
            True if all corner points are the same, else False.
        """
        return self.corners == other.corners
        
    
if __name__ == "__main__":
    pass
    