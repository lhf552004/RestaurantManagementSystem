from setuptools import setup, find_packages
import py2exe

setup(
    console=['src/main.py'],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    options={
        'py2exe': {
            'bundle_files': 1,
            'compressed': True
        }
    },
    zipfile=None,
    data_files=[('.', ['.env'])]  # Copy the .env file from the current directory to the dist directory
)
