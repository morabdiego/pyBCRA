"""
pyBCRAdata - Cliente Python para la API del Banco Central de la República Argentina
"""

from .api.client import BCRAclient

__version__ = "0.3.4"
__author__ = "Diego Mora"

# Create default client instance
_default_client = BCRAclient()

# Expose get methods from default client
get_monetary_data = _default_client.get_monetary_data
get_currency_master = _default_client.get_currency_master
get_currency_quotes = _default_client.get_currency_quotes
get_currency_timeseries = _default_client.get_currency_timeseries
get_checks_master = _default_client.get_checks_master
get_checks_reported = _default_client.get_checks_reported
get_debts = _default_client.get_debts
get_debts_historical = _default_client.get_debts_historical
get_debts_rejected_checks = _default_client.get_debts_rejected_checks

__all__ = [
    'BCRAclient',
    'get_monetary_data',
    'get_currency_master',
    'get_currency_quotes',
    'get_currency_timeseries',
    'get_checks_master',
    'get_checks_reported',
    'get_debts',
    'get_debts_historical',
    'get_debts_rejected_checks'
]
