from typing import Optional, List, Union
import numpy as np
from src.primitives.point import Point2D
from src.primitives.rectangle import Rectangle2D
from src.transforms import *


class Rectangles2D:
    """
    A class that holds multiple Rectangle2D objects and performs calculations
    on those rectangles. Currently this class is primarily used to calculate
    the transform matrices between rectangles.
    """

    def __init__(self, rects: Optional[List[Rectangle2D]] = None) -> None:
        if rects:
            self._rectangles: List[Rectangle2D] = rects
        else:
            self._rectangles: List[Rectangle2D] = []
    
    @property
    def rectangles(self) -> List[Rectangle2D]:
        """
        """
        return self._rectangles

    @rectangles.setter
    def rectangles(self, new_rects: List[Rectangle2D]) -> None:
        """
        """
        self._rectangles = new_rects

    def __repr__(self) -> str:
        """
        Represent the rectangles with rectangles list.

        Returns:
            The string
        """
        return f"Rectangles2D({self._rectangles})"
    
    @property
    def reference(self) -> Optional[Rectangle2D]:
        """
        When calculating transformations, treat the first rectangle
        in the list as the reference rectangle.

        Returns:
            The first rectangle in list.
        """
        if len(self._rectangles) > 0:
            return self._rectangles[0]

    def append(self, new_rect: Rectangle2D) -> None:
        """
        Append new rectangle to the list

        Args:
            new_rect: The rectangle to append
        """
        self._rectangles.append(new_rect)
    
    def calculate_transforms(self, transform: TransformBase2D) -> Union[TransformBase2D, List[TransformBase2D]]:
        """
        Calculate the transform matrices between the reference rectangle and
        the other rectangles. The number of transform matrices that are
        returned is the number of rectangles - 1. The from_origin property
        from each returned transform should be set to True.

        Args:
            transform: The type of transform (a subclass of TransformBase2D).

        Returns:
            The transform matrices.
        """
        transforms: List[TransformBase2D] = []
        ref: Rectangle2D = self.reference
        transform_name = transform.__class__.__name__.lower()
        method_name = f"calculate_{transform_name}"
        method_attr = getattr(self, method_name, None)  # no default
        for rect in self._rectangles[1:]:
            t: TransformBase2D = method_attr(ref, rect)
            t.from_origin = True
            transforms.append(t)
        if len(transforms) == 1:
            return transforms[0]
        return transforms
    
    def calculate_translationtransform2d(self, ref: Rectangle2D, query: Rectangle2D) -> TranslationTransform2D:
        """
        Calculate the translation transform matrix based on two rectangles.
        Rectangle may also be scaled, but only calculate translation based
        on the center point of both rectangles.

        Args:
            ref: The reference rectangle.
            rect: The query rectangle.

        Returns:
            The translation transform.
        """
        tx = query.center.x - ref.center.x
        ty = query.center.y - ref.center.y
        return TranslationTransform2D(tx, ty)
    
    def calculate_rotationtransform2d(self, ref: Rectangle2D, query: Rectangle2D) -> RotationTransform2D:
        """
        Calculate the rotation transform matrix based on two rectangles.

        Args:
            ref: The reference rectangle.
            rect: The query rectangle.

        Returns:
            The rotation transform.
        """
        raise NotImplementedError
    
    def calculate_scaletransform2d(self, ref: Rectangle2D, query: Rectangle2D) -> ScaleTransform2D:
        """
        Calculate the scale transform matrix based on two rectangles. Rectangle may
        also be translated, but only calculate the scale based on width and height.

        Args:
            ref: The reference rectangle.
            rect: The query rectangle.

        Returns:
            The scale transform.
        """
        sx = query.width / ref.width
        sy = query.height / ref.height
        return ScaleTransform2D(sx, sy)
    
    def calculate_perspectivetransform2d(self, ref: Rectangle2D, query: Rectangle2D) -> PerspectiveTransform2D:
        """
        """
        raise NotImplementedError
    
    def calculate_sheartransform2d(self, ref: Rectangle2D, query: Rectangle2D) -> ShearTransform2D:
        """
        """
        raise NotImplementedError
    
    def calculate_rigidtransform2d(self, ref: Rectangle2D, query: Rectangle2D) -> RigidTransform2D:
        """
        """
        raise NotImplementedError
    
    def calculate_similaritytransform2d(self, ref: Rectangle2D, query: Rectangle2D) -> SimilarityTransform2D:
        """
        """
        raise NotImplementedError
    
    def calculate_affinetransform2d(self, ref: Rectangle2D, query: Rectangle2D) -> AffineTransform2D:
        """
        Calculate the affine transform between two rectangles. Only use three
        corresponding points to exactly solve for 6 unknowns. Using all corners
        will cause system to be overdetermined and will need to fit least squares.

        Args:
            ref: The reference rectangle.
            query: The query rectangle.

        Returns:
            The affine transform.
        """
        ref_use_corners: Points2D = ref.corners[:3]
        query_use_corners: Points2D = query.corners[:3]
        ref_arr = ref_use_corners.array_form.T
        query_arr = query_use_corners.array_form.T
        M = query_arr @ np.linalg.inv(ref_arr)
        return AffineTransform2D.from_M(M)
    
    def calculate_projectivetransform2d(self, ref: Rectangle2D, query: Rectangle2D) -> ProjectiveTransform2D:
        """
        Calculate the projective transform between two rectangles.
        Use four corresponding points and SVD. Projective transform
        is defined up to scale, so it is normalized by bottom right value.

        Args:
            ref: The reference rectangle.
            query: The query rectangle.

        Returns:
            The projective transform.
        """
        ref_arr = ref.corners.cartesian_array_form
        query_arr = query.corners.cartesian_array_form
        equation_matrix = []
        for (ref_x, ref_y), (query_x, query_y) in zip(ref_arr, query_arr):
            equation_matrix.append([-ref_x, -ref_y, -1, 0, 0, 0, ref_x * query_x, ref_y * query_x, query_x])
            equation_matrix.append([0, 0, 0, -ref_x, -ref_y, -1, ref_x * query_y, ref_y * query_y, query_y])
        equation_matrix = np.array(equation_matrix)
        _, _, Vt = np.linalg.svd(equation_matrix)
        m = Vt[-1]
        M = m.reshape(3, 3)
        # Normalize
        M = M / M[2, 2]
        return ProjectiveTransform2D.from_M(M)
    
    def __getitem__(self, idx: int) -> Rectangle2D:
        """
        Get the rectangle from rectangles

        Args:
            idx: The index

        Returns:
            The rectangle at index
        """
        return self._rectangles[idx]
    
    def __len__(self) -> int:
        """
        Get number of rectangles.

        Returns:
            Number of rectangles.
        """
        return len(self._rectangles)
        

if __name__ == "__main__":
    pass
    