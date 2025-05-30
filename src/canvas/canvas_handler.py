from typing import Optional
from ipycanvas import Canvas
from ipywidgets import Button, Layout, HBox
from src.primitives.point import Point2D
from src.primitives.rectangle import Rectangle2D
from src.transforms.transform_base import TransformBase2D
from src.transforms.translation import TranslationTransform2D
from src.transforms.scale import ScaleTransform2D
from src.transforms.rotation import RotationTransform2D
from src.transforms.rigid import RigidTransform2D
from src.transforms.similarity import SimilarityTransform2D
from src.transforms.shear import ShearTransform2D
from src.transforms.affine import AffineTransform2D
from src.transforms.projective import ProjectiveTransform2D


class CanvasHandler:

    def __init__(self, w: int = 800, h: int = 200) -> None:
        """
        """
        # Initialize empty canvas
        self._canvas: Canvas = Canvas(width=w, height=h)
        # Draw border
        self._canvas.stroke_rect(0, 0, w, h)
        # All available transformations
        self._transforms = {}
        # Buttons for user to click
        self._buttons = []
        # Transform is updated by user button click
        self._selected_transform: TransformBase2D = TransformBase2D()
        # Start point and end point from user interaction
        self._rect_start_p: Point2D = Point2D()
        self._rect_end_p: Point2D = Point2D()

    def setup(self) -> None:
        """
        Setup canvas and connect signals and slots
        
        """
        # Mouse up and down
        self._canvas.on_mouse_down(self.handle_mouse_down)
        self._canvas.on_mouse_up(self.handle_mouse_up)
        # Buttons
        self._buttons = [
            Button(description=t, layout=Layout(width='90px', height='30px')) for t in self._transforms.keys()
        ]
        for button in self._buttons:
            button.on_click(self.handle_button_click)
        # Display
        box = HBox(self._buttons)
        display(box, self._canvas)

    def handle_mouse_down(self, x: int, y: int) -> None:
        """
        Handle mouse down by user

        Args:
            x: x position
            y: y position
        """
        self._rect_start_p.x = x
        self._rect_start_p.y = y

    def handle_mouse_up(self, x: int, y: int) -> None:
        """
        Handle mouse release by user. This rectangle will always
        be parallel with canvas, so use built in function to draw
        the rectangle.

        Args:
            x: x position
            y: y position
        """
        self._rect_end_p.x = x
        self._rect_end_p.y = y
        rect_w = x - self._rect_start_p.x
        rect_h = y - self._rect_start_p.y
        self._canvas.stroke_rect(self._rect_start_p.x, self._rect_start_p.y, rect_w, rect_h)

    def handle_button_click(self, b) -> None:
        """
        Apply transform and redraw when button is clicked

        Args:
            b: The button
        """
        selected_transform = self._transforms[b.description]
        print(selected_transform)
        new_rect = selected_transform.apply_to_rectangle(self.user_rectangle)
        self.draw_rectangle_with_points(new_rect)

    def draw_rectangle_with_points(self, rect: Rectangle2D) -> None:
        """
        Draw a rectangle by connected the points. This
        is needed to draw a rotated rectangle based on calculated
        points from the transform classes.

        Args:
            rect: Custom rectangle object

        Returns:
        
        """
        self._canvas.stroke_style = "red"
        p1, p2, p3, p4 = rect.corners
        self._canvas.stroke_lines([(p1.x, p1.y),
                                   (p2.x, p2.y),
                                   (p3.x, p3.y),
                                   (p4.x, p4.y),
                                   (p1.x, p1.y)
                                  ])

    @property
    def user_rectangle(self) -> Rectangle2D:
        """
        Define a rectangle using 4 corner points.
        User rectangle with always be parallel with canvas.

        Returns:
            Custom rectangle object
        """
        left_top = self._rect_start_p
        right_top = Point2D(self._rect_end_p.x, self._rect_start_p.y)
        right_bottom = self._rect_end_p
        left_bottom = Point2D(self._rect_start_p.x, self._rect_end_p.y)
        return Rectangle2D(left_top, right_top, right_bottom, left_bottom)

    @property
    def transforms(self) -> dict[str, TransformBase2D]:
        """
        """
        return self._transforms

    @transforms.setter
    def transforms(self, new_transforms: dict[str, TransformBase2D]) -> None:
        """
        """
        self._transforms = new_transforms
    

if __name__ == "__main__":
    pass
    