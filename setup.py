from setuptools import setup, find_packages

# Load the requirements.txt file
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='TrajectoryTools',
    version='0.0.2',
    author='Chris Davies',
    author_email='',
    description='A package for loading,saving and manipulating trajectories',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chrisdavi3s/TrajectoryTools',
    project_urls={
        'Bug Tracker': 'https://github.com/TrajectoryTools/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    install_requires = required_packages,
    extras_require={
        'dev': [
            # 'pytest>=6.0',
            # Any other additional dependencies for development (testing, docs, etc.)
        ],
    },
    include_package_data=False,
    package_data={
        # If any package contains data files, include them:
    },
)