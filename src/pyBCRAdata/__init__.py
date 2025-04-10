"""
pyBCRAdata - Cliente Python para la API del Banco Central de la República Argentina
"""

from .client import BCRAclient, MonetaryAPI, CurrencyAPI, ChecksAPI, DebtorsAPI
from .connector import APIConnector
from .settings import APISettings

__version__ = "0.4.1"
__author__ = "Diego Mora"

_default_client = BCRAclient()

__all__ = ['BCRAclient', 'monetary', 'currency', 'checks', 'debtors', '__version__']

_connector = APIConnector(
    base_url=APISettings.BASE_URL,
    cert_path=APISettings.CERT_PATH
)

monetary = MonetaryAPI(_connector)
currency = CurrencyAPI(_connector)
checks = ChecksAPI(_connector)
debtors = DebtorsAPI(_connector)
