import math
from typing import Optional
from src.primitives.point import Point2D


class Rectangle2D:
    """
    The class to represent a 2D rectangle. Only define the rectangle with
    4 corner points, so that the corner points can be calculated with any of the
    transforms and redrawn with lines.
    """

    def __init__(self, left_top: Point2D, right_top: Point2D, right_bottom: Point2D, left_bottom: Point2D) -> None:
        """
        
        """
        self._left_top = left_top
        self._right_top = right_top
        self._right_bottom = right_bottom
        self._left_bottom = left_bottom
        self._width: float = math.dist((left_top.x, left_top.y), (right_top.x, right_top.y))
        self._height: float = math.dist((left_top.x, left_top.y), (left_bottom.x, left_bottom.y))
    
    @property
    def left_top(self) -> Point2D:
        """
        """
        return self._left_top

    @property
    def right_top(self) -> Point2D:
        """
        """
        return self._right_top

    @property
    def right_bottom(self) -> Point2D:
        """
        """
        return self._right_bottom

    @property
    def left_bottom(self) -> Point2D:
        """
        """
        return self._left_bottom

    @property
    def width(self) -> float:
        """
        """
        return self._width

    @property
    def height(self) -> float:
        """
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
        adjacent sides must be at 90 degrees
        """
        raise NotImplementedError

    @property
    def corners(self) -> (Point2D, Point2D, Point2D, Point2D):
        """
        Left top, right top, right bottom, left bottom (clockwise)
        
        Returns:
            Corner points of the rectangle
        """
        return self._left_top, self._right_top, self._right_bottom, self._left_bottom

    @property
    def center(self) -> Point2D:
        """
        Center of rectangle by average of corners

        Returns:
            Rectangle center point
        """
        x_sum: int = 0
        y_sum: int = 0
        w_sum: int = 0
        for p in self.corners:
            x_sum += p.x
            y_sum += p.y
            w_sum += p.w
        return Point2D(x_sum / 4, y_sum / 4, w_sum / 4)
        

if __name__ == "__main__":
    pass
    