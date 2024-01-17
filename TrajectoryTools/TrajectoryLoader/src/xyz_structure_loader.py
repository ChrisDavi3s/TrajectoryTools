from .base_structure_loader import StructureLoader
from ase.io import iread
from ase.io.trajectory import Trajectory
from pymatgen.io.ase import AseAtomsAdaptor 
from pymatgen.core.structure import Structure

class XYZStructureLoader(StructureLoader):
    '''
    Implementation of the StructureLoader interface to wrap a lazy loader iterable of structures from a xyz file. 

    Args:
    filepath: str
        Path to the trajectory file
    steps_to_load: slice
        Slice object to specify which steps to load. None for the end means load all steps in the file

    Returns:
    AseIterable object to iterate over the structures in the trajectory. 
    '''

    def __init__(self, filepath: str, structures_slice: slice):
        self.filepath = filepath
        self.structures_slice = structures_slice
        self._iterator = iter(
            iread(self.filepath, index=self.structures_slice))

    def __iter__(self):
        return self

    def __next__(self) -> Structure:
        return AseAtomsAdaptor.get_structure(next(self._iterator))

    def get_total_steps(self) -> int:
        '''
        Count the number of steps in a .xyz file. Adds around 0.3s for 10k steps.
        '''
        with open(self.filepath, 'r') as file:
            first_line = file.readline().strip()
            number_of_atoms = int(first_line) if first_line.isdigit() else None

            if number_of_atoms is None:
                raise ValueError(
                    "The file does not seem to be in the correct .xyz format.")

            return sum(1 for line in file if line.strip() == str(number_of_atoms))
