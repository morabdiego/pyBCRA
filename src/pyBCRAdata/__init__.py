"""
pyBCRAdata - A Python client for accessing BCRA (Banco Central de la República Argentina) data.

This package provides easy access to monetary statistics and foreign exchange data
published by the Central Bank of Argentina.
"""

from .getter import APIGetter
from .connector import APIConnector
from .config import APIConfig

__version__ = '0.1.1'
__author__ = 'Diego Mora'
__email__ = 'morabdiego@gmail.com'

__all__ = [
    'APIGetter',
    'APIConnector',
    'APIConfig',
]
