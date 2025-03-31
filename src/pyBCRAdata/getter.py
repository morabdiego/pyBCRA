from typing import Optional, Union, Dict, Any
import pandas as pd
import requests
import warnings

from .config import APIConfig
from .connector import APIConnector


class BCRAclient:
    """
    A comprehensive class for fetching monetary and currency-related data from an API.
    """

    def __init__(
        self,
        base_url: str = APIConfig.BASE_URL,
        cert_path: Optional[str] = None,
        verify_ssl: bool = True
    ):
        """
        Initialize the BCRAclient.

        Args:
            base_url (str): Base URL for the API. Defaults to APIConfig.BASE_URL.
            cert_path (Optional[str]): Path to the SSL certificate. Defaults to APIConfig.CERT_PATH.
            verify_ssl (bool): Whether to verify SSL certificates. Defaults to True.
        """
        if not verify_ssl:
            warnings.warn(
                "SSL verification is disabled. This is not recommended for production use.",
                UserWarning
            )
            requests.packages.urllib3.disable_warnings()

        self.api_connector = APIConnector(
            base_url=base_url,
            cert_path=cert_path or (APIConfig.CERT_PATH if verify_ssl else False)
        )

    def get_monetary_data(self, **kwargs) -> Union[str, pd.DataFrame]:
        """
        Retrieve monetary data from the API.
        """
        endpoint = APIConfig.MONETARY_ENDPOINT
        debug = kwargs.pop("debug", False)
        return self.api_connector.fetch_data(endpoint=endpoint, params=kwargs, debug=debug)

    def get_currency_master(self, **kwargs) -> Union[str, pd.DataFrame]:
        """
        Retrieve master currency data from the API.
        """
        endpoint = APIConfig.CURRENCY_MASTER_URL
        debug = kwargs.pop("debug", False)
        return self.api_connector.fetch_data(endpoint=endpoint, params=None, debug=debug)

    def get_currency_quotes(self, **kwargs) -> Union[str, pd.DataFrame]:
        """
        Retrieve current currency quotes from the API.
        """
        endpoint = APIConfig.CURRENCY_QUOTES_URL
        debug = kwargs.pop("debug", False)
        return self.api_connector.fetch_data(endpoint=endpoint, params=kwargs, debug=debug, is_currency=True)

    def get_currency_timeseries(self, moneda: str, **kwargs) -> Union[str, pd.DataFrame]:
        """
        Retrieve historical currency data for a specific currency.
        """
        if not moneda:
            raise ValueError("El código de moneda es requerido")

        endpoint = f"{APIConfig.CURRENCY_QUOTES_URL}/{moneda}"
        debug = kwargs.pop("debug", False)
        return self.api_connector.fetch_data(endpoint=endpoint, params=kwargs, debug=debug, is_timeseries=True)
