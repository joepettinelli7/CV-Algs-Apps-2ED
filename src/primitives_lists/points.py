from typing import Optional, List, Union, Iterator
import numpy as np
from src.primitives.point import Point2D
from src.primitives.line import Line2D


class Points2D:
    """
    A class that holds multiple Point2D objects and
    performs calculations on those points.
    """

    def __init__(self, points: Optional[List[Point2D]] = None) -> None:
        if points:
            self._points: List[Point2D] = points
        else:
            self._points: List[Point2D] = []
    
    @property
    def points(self) -> List[Point2D]:
        """
        All points belonging to instance.
        
        Returns:
            The list of points
        """
        return self._points
    
    @points.setter
    def points(self, new_points: List[Point2D]) -> None:
        """
        Set new points.

        Args:
            new_points: The new points
        """
        self._points = new_points

    def __repr__(self) -> str:
        """
        Use the points to represent the points list.
        
        Returns:
            The points
        """
        return f"Points2D({self._points})"
    
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
            return np.vstack([p.vector.T for p in self._points])
        else:
            return None
    
    @property
    def cartesian_array_form(self) -> Optional[np.ndarray]:
        """
        Make an array with each row being a point. This
        makes calculations easier with numpy.
        
        Returns:
            nx2 array because (x, y) for each point.
        """
        if self.num_points > 0:
            return np.vstack([p.cartesian_vector.T for p in self._points])
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
    
    def apply_transform(self, M: np.ndarray, inplace: bool = False) -> "Points2D":
        """
        Apply the transform to the points. Use the M property
        which contains the numpy array matrix.

        Args:
            M: The transform matrix.
            inplace: If True, change points of this instance, else return new Points2D instance.
                     * Be careful when True because it can lead to a compounding effect when
                     multiple transformations are applied to the same points inadvertently. *

        Returns:
            Either self or a new Points2D instance.
        """
        transformed_points: List[Point2D] = []
        for p in self._points:
            transformed_point = p.apply_transform(M, inplace=inplace)
            transformed_points.append(transformed_point)
        if inplace:
            self._points = transformed_points
            return self
        else:
            return Points2D(transformed_points)
    
    def __eq__(self, other: "Points2D") -> bool:
        """
        Check whether list of points are equal.
        Equal if all points are equal. Points should
        be normalized to same w first.

        * Very sensitive to small float differences.

        Args:
            other: Other points list.

        Returns:
            True if all points are equal, else False.
        """
        self_points = [p.normalized() for p in self._points]
        other_points = [p.normalized() for p in other.points]
        return set(self_points) == set(other_points)
    
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
    
    def __getitem__(self, idx: Union[int, slice]) -> Union[Point2D, "Points2D"]:
        """
        Get the point from points. Can handle slices.

        Args:
            idx: The index or slice.

        Returns:
            The Point2D or Points2D with Point2D objects at index.
        """
        if isinstance(idx, int):
            return self._points[idx]
        elif isinstance(idx, slice):
            return Points2D(self._points[idx])
        else:
            raise TypeError(f"Need int or slice, not {type(idx)}.")
    
    def __iter__(self) -> Iterator[Point2D]:
        """
        Iterator to iterate list of points. Needed
        to work when unpacking Points2D object with *.

        Returns:
            Iterator for Point2D objects.
        """
        return iter(self._points)


if __name__ == "__main__":
    pass
    