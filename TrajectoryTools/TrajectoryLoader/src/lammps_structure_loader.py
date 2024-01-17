import os
from .base_structure_loader import StructureLoader
from ase.io import read
from ase.io.trajectory import Trajectory
from ase.atoms import Atoms
from typing import cast, Optional
from pymatgen.io.ase import AseAtomsAdaptor 
from pymatgen.core.structure import Structure

class LammpsDumpDirectoryLoader(StructureLoader):
    '''
    Implementation of StructureLoader for a directory of LAMMPS dump files.
    
    Args:
        dump_dir (str): Path to directory containing LAMMPS dump files.
        structures_slice (slice): Slice object to select a subset of structures.
    
    Returns:
        Iterator over pymatgen structures in the dump files.
    '''
    def __init__(self, dump_dir:str, structures_slice: Optional[slice] = None):
        # Get the list of all .dat files
        all_files = [f for f in os.listdir(dump_dir) if f.endswith('.dat')]
        
        # Define a custom sort function that extracts the number from the file name
        def sort_key(file_name):
            number_part = file_name.split('.')[-2]
            return int(number_part)

        # Sort the files based on the custom sort function
        sorted_files = sorted(all_files, key=sort_key)
        # Apply the slice to the sorted files
        if structures_slice is not None:
            self.files = sorted_files[structures_slice]
        else:
            self.files = sorted_files

        self.file_index = 0
        self.dump_dir = dump_dir
        self.structures_slice = structures_slice

        print(f'Loading slice {self.structures_slice} from {len(self.files)} files')

    def __iter__(self) -> StructureLoader:
        return self

    def __next__(self) -> Structure:
        if self.file_index < len(self.files):
            file_path = os.path.join(self.dump_dir, self.files[self.file_index])
            # Any here as we *should* only get one structure
            atoms : Atoms = cast(Atoms,read(file_path, format='lammps-dump-text'))
            self.file_index += 1
            return AseAtomsAdaptor.get_structure(atoms)
        else:
            raise StopIteration()
        
    def get_total_steps(self) -> int:
        return len(self.files)