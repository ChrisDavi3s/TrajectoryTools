from abc import ABC, abstractmethod
from pymatgen.core.structure import Structure

class StructureLoader(ABC):
    '''
    Abstract class (interface) to load and store a iterable of structures that lazy load.

    Parameters
    ----------
    filepath: str
        Path to the trajectory file
    steps_to_load: slice
        Slice object to specify which steps to load. None for the end means load all steps in the file

    Returns
    -------
    AseIterable object to iterate over the structures in the trajectory. 
    '''

    @abstractmethod
    def __init__(self, 
                 filepath: str,
                structures_slice: slice):
        self.filepath = filepath
        self.structures_slice = structures_slice

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self) -> Structure:
        '''
        Returns the next structure in the trajectory.
        '''
        pass

    @abstractmethod
    def get_total_steps(self) -> int:
        '''
        Count the number of steps in the trajectory file.
        '''
        pass

