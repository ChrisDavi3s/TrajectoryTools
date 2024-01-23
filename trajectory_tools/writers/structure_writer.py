from abc import ABC, abstractmethod
from typing import Optional, Union, List, Dict
from enum import Enum, auto
from pymatgen.core.structure import Structure

class StructureWriter(ABC):
    '''
    Abstract base class to write pymatgen structures to a file or files.
    Keeps the file open for appending until the object is deleted.

    Parameters
    ----------
    is_single_file: bool
        True if writing to a single file, False if writing to multiple files.
    path: str
        File path for single file, or directory path for multiple files.
    filename_template: str (optional)
        Template for filenames when writing to multiple files.
    '''

    @abstractmethod
    def __init__(self, 
                path: str,
                ):
        pass

    @abstractmethod
    def write_structure(self, 
                        structure: Structure, 
                        file_name: Optional[str],
                        extra_properties: Optional[Union[List[str], Dict[str, str]]] = None,
                       ) -> None:
        '''
        Write a single structure to the file or a new file in the directory.

        Parameters
        ----------
        structure: pymatgen structure
            Structure to write
        '''
        pass

    '''
    OOP junk below
    '''

    @abstractmethod
    def open(self):
        '''
        Open the file for appending or writing.
        '''
        pass

    @abstractmethod
    def close(self):
        '''
        Close the file explicitly.
        '''
        pass

    @abstractmethod
    def clear_file(self):
        '''
        Clear the file if it exists
        '''
        pass

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        pass
