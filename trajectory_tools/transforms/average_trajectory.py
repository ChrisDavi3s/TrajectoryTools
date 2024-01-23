from ast import Dict
from re import S
import re
from typing import Iterable, Optional, List, Union

from click import Option
from traitlets import Bool 
from ..loaders import StructureLoader
from ..writers import StructureWriter
from pymatgen.core import Structure, Site, Species
import numpy as np
import sys


'''

DOES NOT WORK YET
'''

class AverageTrajectoryCreator():
    '''
    Class to create an average trajectory from a set pymatgen structures. The 
    trajectory is a list of structures, that loads LAZILY.

    Args:
        trajectory (StructureLoader| List[Structure]):
            TrajectoryLoader object that loads the trajectories.Contains slice 
            to select subset of structures.
        species_to_average (Optional[list[str]]): 
            List of species to average. None means average over all species.
        average_window (Optional[list[int]]):
            Window size for moving average per species. 
        use_block_average (Optional[bool]):
            If True, will use block averaging instead of moving average.
        remove_uneccessary_frames (Optional[bool]):
            If True, will reduce the trajectory to the least number of distinct frames.
        trajectory_writer (TrajectoryWrtier): 
            Path to save the averaged trajectory to. None means do not save.
    Returns:
        Nothing.
    '''

    def __init__(self, 
                 trajectory: StructureLoader|List[Structure], 
                 species_to_average: Optional[Dict] = None,
                 average_window: Optional[List[int] | int] = 1,
                 use_block_average: bool = False,
                 remove_unnecessary_frames: bool = False,
                 trajectory_writer: Optional[StructureWriter] = None,
                 save_memory: bool = True):
        """
        Constructor for AverageTrajectoryCreator.
        """
        self.trajectory : StructureLoader|Iterable[Structure] = trajectory if isinstance(trajectory, StructureLoader) else iter(trajectory) 
        try:
            self.base_structure = next(self.trajectory)
        except StopIteration:
                raise ValueError("Trajectory is empty.")
        if self.base_structure is None:
            raise ValueError("Trajectory is empty.")
        self.species_to_average : Optional[Dict] = species_to_average if not None else  {site.species_string: None for site in self.base_structure.sites}
        self.use_block_average : bool = use_block_average #not implemented yet
        self.remove_unnecessary_frames : bool  = remove_unnecessary_frames #not implemented yet
        self.trajectory_writer : Optional[StructureWriter] = trajectory_writer
        self.total_number_of_sites : Optional[int] = None
        #if Structureloader use get_total_steps, else use len  
        self.total_number_of_structures : int = trajectory.get_total_steps() if isinstance(trajectory, StructureLoader) else len(trajectory)
        self.position_matrix: List[np.ndarray] = []
        self.save_memory : bool = save_memory
        #type of dictionary is Dict{str: List[int]} 
        self.indeces_to_average : Optional[dict[str, list[int]]] = {}
        # get highest value in average_window
        if self.species_to_average is not None:
            windows = [value for value in self.species_to_average.values() is not None]
            if windows:
                #if even throw error
                if max(windows) % 2 == 0:
                    raise ValueError("Window size must be odd.")
                else:
                    self.max_window_size =  max(windows)
            else:
                self.max_window_size = self.total_number_of_structures
        else:
            self.max_window_size = self.total_number_of_structures

        self.new_structure_list : List[Structure] = []
        self.base_structure : Optional[Structure] = None

    def __add_trajectory_information__(self):
        """
        Populated .
        """
        if current_step == 0:
            try:
                self.base_structure = next(self.trajectory)
            except StopIteration:
                raise ValueError("Trajectory is empty.")
        if self.base_structure is None:
            raise ValueError("Trajectory is empty.")
        if self.species_to_average is not None:
            for species in self.species_to_average:
                self.indeces_to_average[species] = [i for i, site in enumerate(self.base_structure.sites) if site.species_string == species]
        else:
            self.indeces_to_average = [i for i, site in enumerate(self.base_structure.sites)]       
        self.total_number_of_sites = len(self.base_structure.sites)
        #self.new_structure_list = Structure(structure.lattice, structure.species, coords= coords_are_cartesian=True)

    def generate_average_structure(self, current_step: int )-> Structure:
        """
        Generates the average structure for the current step, considering the specific
        block size for averaging for each species. The resulting coordinates are 
        structured as an Nx3 array suitable for Pymatgen.

        Args:
            current_step (int): The current step in the trajectory.
        """
        coords = np.zeros((self.total_number_of_sites, 3))

        # Iterate over each species and their respective block size
        for species, block_size in self.species_to_average.items():
            species_indices = self.indeces_to_average[species]
            half_window = block_size // 2

            # Calculate the start and end indices for the averaging window
            start_idx = max(0, current_step - half_window)
            end_idx = min(len(self.position_matrix), current_step + half_window + 1)

            # Extract and average the coordinates for this species
            species_coords = np.mean([self.position_matrix[i][species_indices, 0, :] for i in range(start_idx, end_idx)], axis=0)
            coords[species_indices, :] = species_coords
        
        return self.generate_new_structure(coords)

    def update_position_matrix(self, current_step: int):
        """
        Updates the position matrix based on the current step, buffer size, and the constraints
        of the trajectory's beginning and end. The buffer is centered around the current step.

        Args:
            current_step (int): The current step in the trajectory.
        """
        # Calculate the half window size (rounded down)
        half_window = self.max_window_size // 2

        # Determine the start and end indices for loading structures
        start_idx = max(0, current_step - half_window)
        end_idx = min(self.total_number_of_structures, current_step + half_window + 1)

        # Update the position matrix with the required structures
        for idx in range(start_idx, end_idx):
            if idx < len(self.position_matrix):
                continue  # Skip loading if already in the position matrix
            try:
                if current_step != 0:
                    try:
                        next_structure = next(self.trajectory)
                        self.position_matrix.append(next_structure.cart_coords.reshape(-1, 1, 3))
                    except StopIteration:
                        break
                else:
                    self.add_trajectory_information(current_step)
                    self.position_matrix.append(self.base_structure.cart_coords.reshape(-1, 1, 3))
            except StopIteration:
                break  # End of trajectory reached

        # Trim the position matrix from the start if it exceeds the buffer size
        while len(self.position_matrix) > self.max_window_size:
            self.position_matrix.pop(0)

    def print_progress(self, current_step: int):
                progress = (current_step / self.total_number_of_structures ) * 100
                bar_length = 30
                filled_length = int(bar_length * current_step // self.total_number_of_structures)
                bar = '#' * filled_length + '-' * (bar_length - filled_length)
                print(f'\rProcessing [{bar}] {current_step}/{self.total_number_of_structures} ({progress:.2f}%)', end='')
                sys.stdout.flush()

    def generate_new_structure(self, coords: np.ndarray) -> Structure:
        """
        Generates a new structure from a set of coordinates and species.
        """
        return Structure(lattice=self.base_structure.lattice,
                         species=self.base_structure.species,
                         coords=coords,
                         coords_are_cartesian=True)

    def process_trajectory(self) -> Optional[List[Structure]]:
        """
        Processes the trajectory, applying averaging and optional frame reduction.
        """
        
        # first, we need to select get trajectory information
        if self.trajectory is not None:
            for step in range(self.total_number_of_structures):
                self.print_progress(step)
                
                # update the position matrix   
                self.update_position_matrix(step)

                # create the average coords for this step for every species
                average_structure = self.generate_average_structure(step)

                if self.trajectory_writer is not None:
                    self.trajectory_writer.write_structure(average_structure, file_name=None)
                else:
                    self.new_structure_list.append(average_structure)
            if self.trajectory_writer is None:
                return self.new_structure_list

        

    


