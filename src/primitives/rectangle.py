import math
from typing import Optional
from src.primitives.point import Point2D


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
        # Rectangle may not be parallel with canvas, so use distance calculation.
        self._width: float = math.dist((left_top.x, left_top.y), (right_top.x, right_top.y))
        self._height: float = math.dist((left_top.x, left_top.y), (left_bottom.x, left_bottom.y))
    
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

    @property
    def width(self) -> float:
        """
        
        Returns:
            The width of rectangle
        """
        return self._width

    @property
    def height(self) -> float:
        """

        Returns:
            The height of rectangle
        """
        return self._height

    @left_top.setter
    def left_top(self, new_point: Point2D) -> None:
        """
        """
        self._left_top = new_point

    @right_top.setter
    def right_top(self, new_point: Point2D) -> None:
        """
        """
        self._right_top = new_point

    @right_bottom.setter
    def right_bottom(self, new_point: Point2D) -> None:
        """
        """
        self._right_bottom = new_point

    @left_bottom.setter
    def left_bottom(self, new_point: Point2D) -> None:
        """
        """
        self._left_bottom = new_point

    @property
    def is_true_rectangle(self) -> bool:
        """
        The opposite sides must be parallel and the
        adjacent sides must be at 90 degrees.
        """
        raise NotImplementedError

    @property
    def corners(self) -> (Point2D, Point2D, Point2D, Point2D):
        """
        Left top, right top, right bottom, left bottom (clockwise).
        
        Returns:
            Corner points of the rectangle.
        """
        return self._left_top, self._right_top, self._right_bottom, self._left_bottom

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
        

if __name__ == "__main__":
    pass
    