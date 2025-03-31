"""
pyBCRAclient - A Python client for accessing BCRA (Banco Central de la República Argentina) data.

This package provides easy access to monetary statistics and foreign exchange data
published by the Central Bank of Argentina.
"""

from .getter import BCRAclient

__version__ = '0.1.3'
__author__ = 'Diego Mora'
__email__ = 'morabdiego@gmail.com'

# Create default instance
_default_client = BCRAclient()

# Expose methods from default instance
get_monetary_data = _default_client.get_monetary_data
get_currency_master = _default_client.get_currency_master
get_currency_quotes = _default_client.get_currency_quotes
get_currency_timeseries = _default_client.get_currency_timeseries

__all__ = [
    'BCRAclient',
    'get_monetary_data',
    'get_currency_master',
    'get_currency_quotes',
    'get_currency_timeseries',
]
