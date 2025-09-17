"""
ermsf
A package to perform time-dependent RMSF analysis on molecular dynamics data.
"""

# Add imports here
from .ermsf import ermsf

from importlib.metadata import version

__version__ = version("ermsfkit")
