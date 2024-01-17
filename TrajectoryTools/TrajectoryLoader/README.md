# TrajectoryLoader

TrajectoryLoader is a Python library for loading trajectory data as pymatgen structures from various molecular dynamics simulations.

## Installation

To install TrajectoryLoader, you will need Python installed on your system. Python 3.11 is required.

### Clone from Git repository

You can install the TrajectoryLoader package directly from the Git repository using the following commands:

```bash
# Clone only the TrajectoryLoader folder from the repository
git clone --depth 1 --filter=blob:none --sparse https://github.com/ChrisDavi3s/TrajectoryLoader.git
cd TrajectoryLoader
git sparse-checkout set TrajectoryLoader

```

### Install on your machine

# Change to the TrajectoryLoader directory
```bash
cd TrajectoryLoader
```

# Install the package
```bash
pip install .
```

# Or for an editable install
```bash
pip install -e .
```

### Dependencies

TrajectoryLoader requires the following packages:

- numpy
- pymatgen

These dependencies will be automatically installed when you install the TrajectoryLoader package.

## Usage

After installation, you can start using TrajectoryLoader by importing it into your Python scripts:

    from trajectory_loader import XYZLoader, DatLoader

For more information on how to use TrajectoryLoader, please refer to the documentation and example scripts provided in the `/examples` directory.

## Contributing

See base folder CONTRIBUTING.md

## License

See base folder LICENCE.md

