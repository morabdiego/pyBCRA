from typing import Optional
import pandas as pd
import requests
import warnings

from .config import APIConfig
from .connector import APIConnector

class APIGetter:
    """
    A comprehensive class for fetching monetary and currency-related data from an API.

    Provides methods to retrieve monetary and currency data with flexible filtering options.
    """

    def __init__(
        self,
        base_url: str = APIConfig.BASE_URL,
        cert_path: Optional[str] = None,
        verify_ssl: bool = True
    ):
        """
        Initialize the APIGetter with API configuration.

        Args:
            base_url (str): Base URL for the API
            cert_path (Optional[str]): Path to custom SSL certificate. If None, uses system's certificates
            verify_ssl (bool): Whether to verify SSL certificates. Set to False to disable verification
                                (not recommended for production)
        """
        if not verify_ssl:
            warnings.warn(
                "SSL verification is disabled. This is not recommended for production use.",
                UserWarning
            )
            requests.packages.urllib3.disable_warnings()

        # Use custom cert path, fallback to default, or None for system certs
        effective_cert_path = cert_path or APIConfig.CERT_PATH if verify_ssl else False

        self.api_connector = APIConnector(
            base_url=base_url,
            cert_path=effective_cert_path
        )

    def get_monetary_data(
        self,
        id_variable: Optional[str] = None,
        desde: Optional[str] = None,
        hasta: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        debug: bool = False
    ) -> pd.DataFrame:
        """
        Retrieve monetary data from the API with advanced filtering capabilities.

        Args:
            id_variable (Optional[str]): Specific variable ID to fetch
            desde (Optional[str]): Start date (YYYY-MM-DD)
            hasta (Optional[str]): End date (YYYY-MM-DD)
            offset (Optional[int]): Pagination offset
            limit (Optional[int]): Maximum number of records to retrieve
            debug (bool): Return constructed URL instead of data if True

        Returns:
            pd.DataFrame: Monetary data
        """
        endpoint = f"{APIConfig.MONETARY_ENDPOINT}/{id_variable}" if id_variable else APIConfig.MONETARY_ENDPOINT
        params = {
            "desde": desde,
            "hasta": hasta,
            "offset": offset,
            "limit": limit
        }

        return self.api_connector.fetch_data(
            endpoint=f"{self.api_connector.base_url}{endpoint}",
            params={k: v for k, v in params.items() if v is not None},
            debug=debug
        )

    def get_currency_master(self, debug: bool = False) -> pd.DataFrame:
        """
        Retrieve master currency data from the API.

        Args:
            debug (bool): Return constructed URL instead of data if True

        Returns:
            pd.DataFrame: Master currency data
        """
        return self.api_connector.fetch_data(
            endpoint=f"{self.api_connector.base_url}{APIConfig.CURRENCY_MASTER_URL}",
            params={},
            debug=debug
        )

    def get_currency_quotes(
        self,
        fecha: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        debug: bool = False
    ) -> pd.DataFrame:
        """
        Retrieve currency quotes for a specific date.

        Args:
            fecha (Optional[str]): Specific date (YYYY-MM-DD)
            offset (Optional[int]): Pagination offset
            limit (Optional[int]): Maximum number of records to retrieve
            debug (bool): Return constructed URL instead of data if True

        Returns:
            pd.DataFrame: Currency quotes data
        """
        params = {
            'fecha': fecha,
            'offset': offset,
            'limit': limit
        }

        return self.api_connector.fetch_data(
            endpoint=f"{self.api_connector.base_url}{APIConfig.CURRENCY_QUOTES_URL}",
            params={k: v for k, v in params.items() if v is not None},
            debug=debug
        )

    def get_currency_timeseries(
        self,
        moneda: str,
        fechadesde: Optional[str] = None,
        fechahasta: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        debug: bool = False
    ) -> pd.DataFrame:
        """
        Retrieve historical currency data for a specific currency.

        Args:
            moneda (str): Currency ISO code
            fechadesde (Optional[str]): Start date (YYYY-MM-DD)
            fechahasta (Optional[str]): End date (YYYY-MM-DD)
            offset (Optional[int]): Pagination offset
            limit (Optional[int]): Maximum number of records to retrieve
            debug (bool): Return constructed URL instead of data if True

        Returns:
            pd.DataFrame: Historical currency data
        """
        if not moneda:
            raise ValueError("El código de moneda es requerido")

        params = {
            'fechadesde': fechadesde,
            'fechahasta': fechahasta,
            'offset': offset,
            'limit': limit
        }

        return self.api_connector.fetch_data(
            endpoint=f"{self.api_connector.base_url}{APIConfig.CURRENCY_QUOTES_URL}/{moneda}",
            params={k: v for k, v in params.items() if v is not None},
            debug=debug
        )
