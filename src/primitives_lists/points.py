from typing import Optional
import numpy as np
from src.primitives.point import Point2D
from src.primitives.line import Line2D


class Points2D:
    """
    A class that holds multiple Point2D objects in instance variable
    and performs calculations on those points.
    """

    def __init__(self, points: Optional[list[Point2D]]) -> None:
        if points:
            self._points: list[Point2D] = points
        else:
            self._points: list[Point2D] = []
    
    @property
    def points(self) -> list[Point2D]:
        """
        All points belonging to instance
        
        Returns:
            The list of points
        """
        return self._points

    @property
    def array_form(self) -> np.ndarray:
        """
        Make an array to represent all points to be used
        with numpy for calculations.
        
        Returns:
            Nx2 array because cartesian points currently.
        """
        arr = np.empty((len(self._points), 2))             
        for idx, p in enumerate(self._points):
            arr[idx] = p.vector.T
        return arr

    def append(self, new_point: Point2D) -> None:
        """
        Append point to point list

        Args:
            new_point: The new point to append
        """
        assert isinstance(new_point, Point2D)
        self._point.append(new_poiont)

    def calculate_fit_line(self, verbose: bool = False) -> Line2D:
        """
        Calculate the line that minimizes the distance to all points.

        Args:
            verbose: Whether to print values.

        Returns:
            The best line
        """
        centroid: np.ndarray = np.mean(self.array_form, axis=0)
        centered_points: np.ndarray = self.array_form - centroid
        cov_mat: np.ndarray = np.cov(centered_points.T, bias=True)
        # cov_mat: np.ndarray = self.calculate_covariance_matrix(verbose=verbose)
        eigvals, eigvecs = np.linalg.eig(cov_mat)
        max_eigval_idx = np.argmax(eigvals)
        principal_direction = eigvecs[:, max_eigval_idx]
        dx, dy = principal_direction
        normal_vector = np.array([-dy, dx])  # rotate to be orthogonal
        a, b = normal_vector  # Get point on line (centroid)
        c = -a * centroid[0] - b * centroid[1]
        fit_line = Line2D(coeffs=(float(a), float(b), float(c)))
        if verbose:
            print(f"eigvals: {eigvals}\n")
            print(f"eigvecs: {eigvecs}\n")
            print(f"max_eigval_idx: {max_eigval_idx}\n")
            print(f"principal_direction: {principal_direction}\n")
            print(f"dx, dy: {dx}, {dy}\n")
            print(f"normal_vector: {normal_vector}\n")
            print(f"fit_line: {fit_line}\n")
        return fit_line

    def calculate_covariance_matrix(self, verbose: bool = False) -> np.ndarray:
        """
        Calculate the covariance matrix of all points.

        Args:
            verbose: Whether to print the values

        Returns:
            A 2x2 matrix
        """
        centroid: np.ndarray = self.calculate_centroid(verbose=verbose)
        centered_points: np.ndarray = self.array_form - centroid
        cov_mat: np.ndarray = np.cov(centered_points.T, bias=True)
        if verbose:
            print(f"centered_points: {centered_points}\n")
            print(f"cov_mat: {cov_mat}\n")
        return cov_mat

    def calculate_centroid(self, verbose: bool = False) -> np.ndarray:
        """
        Calculate the centroid of all points

        Args:
            verbose: Whether to print the values

        Returns:
            The centroid / mean of all points as cartesian
        """
        # mean of each column [x mean, y mean].
        centroid: np.ndarray = np.mean(self.array_form, axis=0)
        if verbose:
            print(f"centroid: {centroid}\n")
        return centroid

    def __sub__(self, other: Point2D) -> "Points2D":
        """
        Subtract other point from list of points.

        Args:
            other: The other point to subtract

        Returns:
            The list of points with other subtracted
        """
        if isinstance(other, Point2D):
            assert not other.is_homogenous
            for p in self._points:
                assert not p.is_homogenous
                p = p - other
            return self
        else:
            raise TypeError(f"Cannot subtract {other.__class__} object from Point2D object.")
        