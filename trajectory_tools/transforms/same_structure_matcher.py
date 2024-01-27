from click import Option
import numpy as np
from scipy.linalg import svd
from typing import Any, Optional
from pymatgen.core.structure import Structure
from pymatgen.core.operations import SymmOp

class SameStructureMatcher:
    '''
    A class to align two structures with the same number of atoms using the 
    Kabsch algorithm and calculate their RMSE.

    Attributes:
        structure1 (Structure): The structure to be aligned.
        structure2 (Structure): The base structure for alignment.
        symmop (SymmOp): Symmetry operation object representing the alignment.
        aligned_structure (Structure): The aligned structure.
        rmse (float): The root mean square error between the aligned structures.

    Args:
        structure1 (Structure): The structure to be aligned.
        structure2 (Structure): The base structure for alignment.
    '''
    def __init__(self, structure1: Structure, structure2: Structure):
        self.structure1 = structure1.copy()
        self.structure2 = structure2.copy()
        self.symmop: Any|None = None
        self.aligned_structure: Any|Structure = None
        self.rmse = None
        self._align_structures()
        self._calculate_rmse()

    @staticmethod
    def _calculate_centroid(coords: np.ndarray) -> np.ndarray:
        '''Calculate the centroid of a set of coordinates.'''
        return np.mean(coords, axis=0)

    @staticmethod
    def _translate_to_centroid(coords: np.ndarray, centroid: np.ndarray) -> np.ndarray:
        '''Translate a set of coordinates to the origin based on a given centroid.'''
        return coords - centroid

    @staticmethod
    def _kabsch_algorithm(P: np.ndarray, 
                          Q: np.ndarray) -> np.ndarray:
        '''
        Compute the optimal rotation matrix using the Kabsch algorithm.
        
        Steps:
            1. Compute the covariance matrix H using the dot product of P and Q.
            2. Perform Singular Value Decomposition (SVD) on H.
            3. Calculate the rotation matrix R using the product of V, U.T (transpose of U).
               V and U are obtained from the SVD.
            4. Ensure a right-handed coordinate system; if the determinant of R is negative,
               negate the last column of V and recompute R.
        '''
        H = np.dot(P.T, Q)
        U, _, Vt = svd(H)
        R = np.dot(Vt.T, U.T)
        if np.linalg.det(R) < 0:
            Vt[2, :] *= -1
            R = np.dot(Vt.T, U.T)
        return R

    def _align_structures(self):
        '''Align two structures using the Kabsch algorithm.'''
        P_cart = self.structure1.lattice.get_cartesian_coords(self.structure1.frac_coords)
        Q_cart = self.structure2.lattice.get_cartesian_coords(self.structure2.frac_coords)

        P_centroid = self._calculate_centroid(P_cart)
        Q_centroid = self._calculate_centroid(Q_cart)

        P_centered = self._translate_to_centroid(P_cart, P_centroid)
        Q_centered = self._translate_to_centroid(Q_cart, Q_centroid)

        rotation_matrix = self._kabsch_algorithm(P_centered, Q_centered)
        translation_vector = Q_centroid - np.dot(rotation_matrix, P_centroid)
        self.symmop = SymmOp.from_rotation_and_translation(rotation_matrix, translation_vector)

        self.aligned_structure = self.structure1.copy().apply_operation(self.symmop)

    def _calculate_rmse(self):
        '''Calculate the root mean square error between the aligned structures.'''
        if self.aligned_structure is not None:
            coords1 = self.aligned_structure.cart_coords
            coords2 = self.structure2.cart_coords
            if coords1.shape != coords2.shape:
                raise ValueError("Coordinate arrays must have the same shape.")
            differences = coords1 - coords2
            square_diffs = np.square(differences)
            mean_square_diff = np.mean(square_diffs)
            self.rmse = np.sqrt(mean_square_diff)
        else:
            raise ValueError("Alignment must be performed before calculating RMSE.")

    def get_symmetry_operation(self) -> Optional[SymmOp]:
        '''Get the symmetry operation used for alignment.'''
        return self.symmop

    def get_aligned_structure(self) -> Structure:
        '''Get the aligned structure.'''
        return self.aligned_structure

    def get_rmse(self) -> Optional[float]:
        '''Get the root mean square error of the alignment.'''
        return self.rmse
