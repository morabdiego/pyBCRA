"""
pyBCRAdata - Cliente Python para la API del Banco Central de la República Argentina
"""

from .client import BCRAclient

__version__ = "0.3.5"
__author__ = "Diego Mora"

# Create default client instance and expose its methods
_default_client = BCRAclient()
for method in [
    'get_monetary_series', 'get_monetary_variables', 'get_currencies', 'get_exchange_rates',
    'get_currency_series', 'get_banks', 'get_reported_checks', 'get_debtors',
    'get_debtors_history', 'get_rejected_checks'
]:
    globals()[method] = getattr(_default_client, method)

__all__ = ['BCRAclient'] + [method for method in globals() if method.startswith('get_')]
