from typing import Optional
import numpy as np
from src.primitives.point import Point2D
from src.primitives.line import Line2D


class Points2D:
    """
    A class that holds multiple Point2D objects and performs
    calculations on those points in their cartesian space.
    """

    def __init__(self, points: Optional[list[Point2D]]) -> None:
        if points:
            self._points: list[Point2D] = points
        else:
            self._points: list[Point2D] = []
    
    @property
    def points(self) -> list[Point2D]:
        """
        All points belonging to instance.
        
        Returns:
            The list of points
        """
        return self._points

    @property
    def num_points(self) -> int:
        """
        Number of points belonging to instance
        
        Returns:
            Number of points
        """
        return len(self._points)

    @property
    def array_form(self) -> Optional[np.ndarray]:
        """
        Make an array with each row being a point. This
        makes calculations easier with numpy.
        
        Returns:
            nx3 array because (x, y, w) for each point.
        """
        if self.num_points > 0:
            arr = np.empty((self.num_points, 3))           
            for idx, p in enumerate(self._points):
                arr[idx] = p.vector.T
            return arr
        else:
            return None
    
    @property
    def centroid(self) -> Optional[np.ndarray]:
        """
        Centroid of points in cartesian space with w equal to 1.
        Numpy array makes calculations easier than using Point2D.

        Returns:
            Centroid
        """
        if self.num_points > 0:
            return np.mean(self.array_form, axis=0)
        else:
            return None
    
    def append(self, new_point: Point2D) -> None:
        """
        Append point to points list

        Args:
            new_point: The new point to append
        """
        assert isinstance(new_point, Point2D)
        self._points.append(new_point)

    def calculate_fit_line(self, verbose: bool = False) -> Line2D:
        """
        Calculate the line that minimizes the distance to all points.

        Args:
            verbose: Whether to print values.

        Returns:
            The best line
        """
        cov_mat: np.ndarray = self.calculate_covariance_matrix(verbose=verbose)
        # Get all eigenvalues and eigenvectors
        eigvals, eigvecs = np.linalg.eig(cov_mat)
        # Get largest eigenvector
        max_eigval_idx = np.argmax(eigvals)
        principal_direction = eigvecs[:, max_eigval_idx]
        dx, dy, _ = principal_direction
        # Get the orthogonal vector
        normal_vector = np.array([-dy, dx])
        # Get point on line (centroid)
        a, b = normal_vector
        c = -a * self.centroid[0] - b * self.centroid[1]
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
            verbose: Whether to print the values.

        Returns:
            A 3x3 matrix
        """
        centered_points: np.ndarray = self.array_form - self.centroid
        cov_mat = np.cov(centered_points.T, bias=True)
        if verbose:
            print(f"centroid: {self.centroid}\n")
            print(f"centered_points: {centered_points}\n")
            print(f"cov_mat: {cov_mat}\n")
        return cov_mat

    def __sub__(self, other: Point2D) -> Optional["Points2D"]:
        """
        Subtract other point from list of points. This will
        result in list of vectors with w equal to 0.

        Args:
            other: The other point to subtract

        Returns:
            A new object with other subtracted
        """
        if isinstance(other, Point2D):
            p_diffs = []
            for p in self._points:
                p_diff = p - other
                p_diffs.append(p_diff)
            return Points2D(p_diffs)
        else:
            raise TypeError(f"Cannot subtract {other.__class__} object from Point2D object.")

    def __isub__(self, other: Point2D) -> Optional["Points2D"]:
        """
        In-place subtract other point from list of points. This will
        result in the instance containing a list of vectors with
        w equal to 0.

        Args:
            other: The other point to subtract

        Returns:
            The same object with other subtracted
        """
        if isinstance(other, Point2D):
            for p in self._points:
                p -= other
            return self
        else:
            raise TypeError(f"Cannot subtract {other.__class__} object from Point2D object.")

    def __getitem__(self, idx: int) -> Point2D:
        """
        Get the point from points

        Args:
            idx: The index

        Returns:
            The point at index
        """
        return self._points[idx]


if __name__ == "__main__":
    pass
    