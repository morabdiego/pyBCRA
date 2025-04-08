"""
pyBCRAdata - Cliente Python para la API del Banco Central de la República Argentina
"""

from .client import BCRAclient

__version__ = "0.3.4"
__author__ = "Diego Mora"

# Create default client instance and expose its methods
_default_client = BCRAclient()
for method in [
    'get_monetary_data', 'get_currency_master', 'get_currency_quotes',
    'get_currency_timeseries', 'get_checks_master', 'get_checks_reported',
    'get_debts', 'get_debts_historical', 'get_debts_rejected_checks'
]:
    globals()[method] = getattr(_default_client, method)

__all__ = ['BCRAclient'] + [method for method in globals() if method.startswith('get_')]
