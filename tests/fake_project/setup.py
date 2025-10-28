# fake setup.py for test

from setuptools import setup, find_packages

setup(
    name="fake_project",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
)