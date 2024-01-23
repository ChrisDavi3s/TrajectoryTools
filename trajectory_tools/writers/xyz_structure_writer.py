import os
from typing import Optional
from .structure_writer import StructureWriter
from pymatgen.core.structure import Structure

class XYZStructureWriter(StructureWriter):
    '''
    Class to write a pymatgen structure to an XYZ file, either to a single file 
    or multiple files in a directory.

    I am so sorry for this abomination.

    Parameters
    ----------
    is_single_file : bool
        If True, writes to a single file. If False, writes to multiple files in a directory.
    path : str
        File path for a single file, or directory path for multiple files.
    filename_template : str, optional
        Template for filenames when writing to multiple files.
    '''

    def __init__(self, 
                 path: str
                ): 
        if os.path.isdir(path):
            self.directory = path
            self.is_directory = True
            self.filepath = None
        elif os.path.isfile(path) or not os.path.exists(path):
            if not path.endswith('.xyz'):
                path = path + '.xyz'
            self.filepath = path
            self.is_directory = False
        else:
            raise ValueError("Invalid path provided. Path must be a directory or a file.")

    def open(self):
        if self.file is None or self.file.closed:
            if self.is_directory and self.filepath is not None:
                self.file = open(self.filepath, 'w')
            else:
                if self.filepath is not None:
                        self.file = open(self.filepath, 'a')

    def close(self):
        if self.file and not self.file.closed:
            self.file.close()

    def clear_file(self):
        if self.filepath is not None and os.path.exists(self.filepath):
            os.remove(self.filepath)
        else:
            raise FileNotFoundError("File does not exist.")

    def write_structure(self,
                        structure: Structure,
                        file_name: Optional[str] = None
                        ) -> None:
        if self.is_directory:
            if file_name is None:
                raise ValueError("Filename must be provided when writing to a directory.")
            if not file_name.endswith('.xyz'):
                file_name += '.xyz'
            self.filepath = os.path.join(self.directory, file_name)
            self.open()
            self.write_xyz(structure)
            self.close()
        else:
            if file_name is not None:
                raise ValueError("Filename should not be provided when not writing to a directory.")
            if self.file is None or self.file.closed:
                self.open()
            self.write_xyz(structure)
            
    def write_xyz(self, structure: Structure) -> None:
        '''
        Write a single structure to the file currently open.

        Parameters
        ----------
        structure: pymatgen structure
            Structure to write to the file
        '''
        if self.file is None or self.file.closed:
            raise RuntimeError(
                "File is not opened. Please call the open method first.")

        f = self.file
        f.write(str(len(structure)) + "\n")
        counter = 0
        for site in structure.sites:
            species = site.specie.symbol
            coords = " ".join([str(i) for i in site.coords])
            f.write(f"{species} {coords}\n")
            counter += 1
        print(f"Wrote {counter} atoms to file")

    def __enter__(self):
        if not self.is_directory:
            self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()