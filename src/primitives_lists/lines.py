from typing import Optional, List
import numpy as np
from src.primitives.point import Point2D
from src.primitives.line import Line2D


class Lines2D:
    """
    A class that holds multiple Line2D objects in instance variable
    and performs calculations on those lines.
    """

    def __init__(self, lines: Optional[List[Line2D]] = None) -> None:
        if lines:
            self._lines: list[Line2D] = lines
        else:
            self._lines: list[Line2D] = []
    
    @property
    def lines(self) -> list[Line2D]:
        """
        All lines belonging to instance
        
        Returns:
            The list of lines
        """
        return self._lines

    def calculate_closest_point(self, verbose: bool = False) -> Optional[Point2D]:
        """
        Calculate the point that minimizes the sum of squared
        distances to each of the lines.

        Args:
            verbose: Whether to print out values

        Raises:
            LinAlgError: If SVD computation does not converge

        Returns:
            Point2D
        """
        A = self.calculate_A(verbose=verbose)
        U, S, Vt = np.linalg.svd(A)  # Singular Value Decomposition
        lrsv = Vt.T[:, -1]  # The last right singular vector of A (page 735 equation A.37)
        lrsv /= np.linalg.norm(lrsv) # Normalize
        solution = Point2D(round(lrsv[0], 2), round(lrsv[1], 2), round(lrsv[2], 2))
        if verbose:
            print(f"U: {U}\n")
            print(f"S: {S}\n")
            print(f"Vt: {Vt}\n")
            print(f"Last right singular vector of A: {lrsv}\n")
            print(f"Solution point: {solution}\n")
        return solution

    def calculate_A(self, verbose: bool = False) -> np.ndarray:
        """
        Sum of outer products of each line vector with itself.

        Returns:
            The 3x3 matrix
        """
        A: np.ndarray = np.zeros((3, 3))
        for l in self._lines:
            A += np.outer(l.vector, l.vector.T)
        if verbose:
            print(f"A: {A}\n")
        return A

    def append(self, new_line: Line2D) -> None:
        """
        Append line to line list

        Args:
            new_line: The new line to append
        """
        assert isinstance(new_line, Line2D)
        self._lines.append(new_line)

    def __getitem__(self, idx: int) -> Line2D:
        """
        Get the line from lines

        Args:
            idx: The index

        Returns:
            The line at index
        """
        return self._lines[idx]


if __name__ == "__main__":
    pass
    