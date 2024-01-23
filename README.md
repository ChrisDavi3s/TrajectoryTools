# TrajectoryTools

TrajectoryTools is a Python library designed for loading and processing trajectory data into pymatgen structures from molecular dynamics simulations. The package is structured into various sub-packages, each with a specific focus on different aspects of trajectory analysis and preparation.

## Sub-packages Overview

- `loaders`: Import trajectory **lazily**  data from different formats and convert them into pymatgen-compatible structures.
  - `base_structure_loader`: Basic loading capabilities for structural data.
  - `lammps_structure_loader`: Specialized loader for LAMMPS simulation output.
  - `xyz_structure_loader`: Loader for XYZ file format.

- `writers`[WIP]: Export pymatgen structures into various file formats suitable for downstream analysis.

- `transforms`[WIP]: Advanced sub-package for smoothing and averaging trajectory data. Also has tools to reshape trajectory.

- `parallel`[WIP]:  A collection of parallel computing utilities for efficient trajectory analysis and processing.
    - `task_runner`: Execute parallel processing tasks on trajectory data for faster data manipulation and transformation
    - `task_que`: 

# Installation

### Prerequisites
Python 3.11 or higher.

### Clone from Git Repository
```bash
git clone https://github.com/ChrisDavi3s/TrajectoryTools.git
cd TrajectoryTools
```
### Install Package
```bash
pip install .
```

Or for a development environment:
```bash
pip install -e .
```

## Dependencies
- numpy==1.26.3
- pandas==2.1.4
- pymatgen==2023.12.18
- scipy==1.11.4
- ase==3.22.1

Note: The exact versions are specified in `requirements.txt` and will be installed automatically.

## Usage

Import the desired sub-package module and utilize its classes and functions in your Python scripts:
```python
from trajectory_tools.loaders import XYZStructureLoader
```

## Contributing
Please refer to `CONTRIBUTING.md` for guidelines on contributing to this project.

## License
The code is available under the terms of the license specified in `LICENCE.md`.

