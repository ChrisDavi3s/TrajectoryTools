from setuptools import setup, find_packages

setup(
    name='TrajectoryLoaders',
    version='0.0.1',
    author='Chris Davies',
    author_email='',
    description='A package for loading various molecular dynamics trajectory formats',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chrisdavi3s/TrajectoryTools/TrajectoryLoader',
    project_urls={
        'Bug Tracker': 'https://github.com/TrajectoryTools/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.11',
    install_requires=[
        # Add your package dependencies here
        # e.g., 'numpy>=1.18.1', 'pymatgen==2022.0.16', etc.
        'pymatgen'
    ],
    extras_require={
        'dev': [
            # 'pytest>=6.0',
            # Any other additional dependencies for development (testing, docs, etc.)
        ],
    },
    include_package_data=True,
    package_data={
        # If any package contains data files, include them:
    },
)
