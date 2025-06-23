from typing import Optional
from ipycanvas import Canvas
from ipywidgets import Button, Layout, HBox, VBox
from src.primitives.point import Point2D
from src.primitives.rectangle import Rectangle2D
from src.primitives_lists.rectangles import Rectangles2D
from src.transforms import *


class CanvasHandler:

    def __init__(self, w: int = 850, h: int = 200) -> None:
        """
        """
        # Initialize empty canvas
        self._canvas: Canvas = Canvas(width=w, height=h)
        # Draw border
        self._canvas.stroke_rect(0, 0, w, h)
        # All available transformations
        self._transforms = {}
        # Buttons for user to click
        self._t_buttons = []
        # Transform is updated by user button click
        self._selected_transform: TransformBase2D = TransformBase2D()
        # Start point and end point from user interaction
        self._rect_start_p: Point2D = Point2D()
        # Flag for whether to draw rect and calculate transform or click button
        self._draw_mode: bool = True
        # Toggle mode button
        self._toggle_button = Button(description="Draw mode", layout=Layout(width='130px', height='30px'))
        # All rectangles drawn by user
        self._all_rectangles = Rectangles2D()
    
    def setup(self) -> None:
        """
        Setup canvas and connect signals and slots
        """
        # Mouse up and down
        self._canvas.on_mouse_down(self.handle_mouse_down)
        self._canvas.on_mouse_up(self.handle_mouse_up)
        # Transform buttons
        self._t_buttons = [
            Button(description=t, layout=Layout(width='90px', height='30px')) for t in self._transforms.keys()
        ]
        for t_button in self._t_buttons:
            t_button.on_click(self.handle_t_button_click)
        # Toggle button
        self._toggle_button.on_click(self.handle_toggle_button_click)
        # Display the buttons and canvas
        t_box = HBox(self._t_buttons)
        box = VBox([self._toggle_button, t_box])
        display(box, self._canvas)
    
    def handle_mouse_down(self, x: int, y: int) -> None:
        """
        Handle mouse down by user

        Args:
            x: x position
            y: y position
        """
        if self._draw_mode:
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
        if self._draw_mode:
            left_top = Point2D(self._rect_start_p.x, self._rect_start_p.y)
            right_top = Point2D(x, self._rect_start_p.y)
            right_bottom = Point2D(x, y)
            left_bottom = Point2D(self._rect_start_p.x, y)
            new_rect = Rectangle2D(left_top, right_top, right_bottom, left_bottom)
            self._all_rectangles.append(new_rect)
            rect_w = new_rect.width
            rect_h = new_rect.height
            self._canvas.stroke_style = "black"
            self._canvas.stroke_rect(self._rect_start_p.x, self._rect_start_p.y, rect_w, rect_h)
            if len(self._all_rectangles) > 1:
                transforms = self._all_rectangles.calculate_transforms(self._selected_transform)
                print(transforms)
            
    def handle_t_button_click(self, b) -> None:
        """
        Apply transform and redraw rect when button is clicked.

        Args:
            b: The transform button
        """
        self.reset_buttons_style()
        b.button_style = 'success'
        selected_transform = self._transforms[b.description]
        if not self._draw_mode:
            print(selected_transform)
            new_rect = self.orig_rectangle.apply_transform(selected_transform, inplace=False)
            self.draw_rectangle_with_points(new_rect)
        # Set the selected transform to remember state
        self._selected_transform = selected_transform
    
    def reset_buttons_style(self) -> None:
        """
        Reset all buttons to default style.
        """
        for t_button in self._t_buttons:
            t_button.button_style = ''
    
    def handle_toggle_button_click(self, b) -> None:
        """
        Handle toggle button to determine whether a transformed
        rect should be drawn or the transform matrix should be
        determined based on two rectangles.

        Args:
            b: The toggle button
        """
        self._draw_mode = not self._draw_mode
        self._toggle_button.description = "Draw mode" if self._draw_mode else "Click mode"
    
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
    def orig_rectangle(self) -> Rectangle2D:
        """
        Define a rectangle using 4 corner points.
        Original rectangle with always be parallel with canvas.
        This is read only.

        Returns:
            Custom rectangle object
        """
        return self._all_rectangles[0]
    
    @property
    def transforms(self) -> dict[str, TransformBase2D]:
        """
        Get dictionary with transform names and instances.

        Returns:
            The dictionary
        """
        return self._transforms

    @transforms.setter
    def transforms(self, new_transforms: dict[str, TransformBase2D]) -> None:
        """
        Set transform dictionary with transform names and instances.

        Args:
            new_transforms: The new transform dictionary
        """
        self._transforms = new_transforms
    

if __name__ == "__main__":
    pass
    