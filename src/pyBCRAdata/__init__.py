"""
pyBCRAdata - Cliente Python para la API del Banco Central de la República Argentina
"""

from .client import BCRAclient, MonetaryAPI, CurrencyAPI, ChecksAPI, DebtorsAPI
from .connector import APIConnector
from .settings import APISettings

__version__ = "0.4.0"
__author__ = "Diego Mora"

# Create default client instance
_default_client = BCRAclient()

# Expose the client and its API submodules
__all__ = ['BCRAclient', 'monetary', 'currency', 'checks', 'debtors']

# Crear instancias de las APIs individuales
_connector = APIConnector(
    base_url=APISettings.BASE_URL,
    cert_path=APISettings.CERT_PATH
)

monetary = MonetaryAPI(_connector)
currency = CurrencyAPI(_connector)
checks = ChecksAPI(_connector)
debtors = DebtorsAPI(_connector)
