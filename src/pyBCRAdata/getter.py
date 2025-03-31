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

    def _validate_params(self, kwargs: Dict[str, Any], valid_api_params: set, valid_func_params: set) -> Dict[str, Any]:
        """
        Validate and separate API parameters and function control parameters.

        Args:
            kwargs (Dict[str, Any]): Input parameters.
            valid_api_params (set): Set of valid API parameters.
            valid_func_params (set): Set of valid function control parameters.

        Returns:
            Dict[str, Any]: Filtered API parameters.

        Raises:
            ValueError: If invalid parameters are provided.
        """
        api_params = {k: v for k, v in kwargs.items() if k in valid_api_params}
        func_params = {k: v for k, v in kwargs.items() if k in valid_func_params}

        # Check for invalid parameters
        invalid_params = set(kwargs.keys()) - valid_api_params - valid_func_params
        if invalid_params:
            raise ValueError(
                f"Invalid parameters: {', '.join(invalid_params)}.\n\n"
                f"Allowed API parameters: {', '.join(valid_api_params) or 'None'}.\n"
                f"Allowed function parameters: {', '.join(valid_func_params)}.\n\n"
                f"Usage:\n"
                f"- Use 'json=True' to return the raw JSON response from the API.\n"
                f"- Use 'debug=True' to return the constructed URL instead of fetching data."
            )

        return api_params, func_params

    def get_monetary_data(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Retrieve monetary data from the API.

        Parameters:
            id_variable (str, optional): The ID of the monetary variable to fetch.
            desde (str, optional): Start date in 'YYYY-MM-DD' format.
            hasta (str, optional): End date in 'YYYY-MM-DD' format.
            limit (int, optional): Maximum number of results to fetch.
            offset (int, optional): Offset for pagination.
            json (bool, optional): If True, returns the raw JSON response from the API. Defaults to False.
            debug (bool, optional): If True, returns the constructed URL instead of fetching data. Defaults to False.

        Returns:
            Union[str, pd.DataFrame, Dict[str, Any]]:
                - If `debug=True`, returns the constructed URL as a string.
                - If `json=True`, returns the raw JSON response as a dictionary.
                - Otherwise, returns the processed data as a pandas DataFrame.

        Raises:
            ValueError: If invalid parameters are provided.

        Example:
            >>> client = BCRAclient()
            >>> data = client.get_monetary_data(id_variable="123", desde="2025-01-01", hasta="2025-03-31")
        """
        valid_api_params = {"id_variable", "desde", "hasta", "limit", "offset"}
        valid_func_params = {"json", "debug"}

        api_params, func_params = self._validate_params(kwargs, valid_api_params, valid_func_params)

        endpoint = APIConfig.MONETARY_ENDPOINT
        url = self.api_connector.build_url(self.api_connector.base_url, endpoint, api_params)
        debug = func_params.get("debug", False)
        json_response = func_params.get("json", False)

        if json_response:
            return self.api_connector.connect_to_api(url)  # Return raw JSON response
        return self.api_connector.fetch_data(url=url, debug=debug)

    def get_currency_master(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Retrieve master currency data from the API.

        Parameters:
            json (bool, optional): If True, returns the raw JSON response from the API. Defaults to False.
            debug (bool, optional): If True, returns the constructed URL instead of fetching data. Defaults to False.

        Returns:
            Union[str, pd.DataFrame, Dict[str, Any]]:
                - If `debug=True`, returns the constructed URL as a string.
                - If `json=True`, returns the raw JSON response as a dictionary.
                - Otherwise, returns the processed data as a pandas DataFrame.

        Raises:
            ValueError: If invalid parameters are provided.

        Example:
            >>> client = BCRAclient()
            >>> data = client.get_currency_master()
        """
        valid_api_params = set()  # No API parameters allowed
        valid_func_params = {"json", "debug"}

        _, func_params = self._validate_params(kwargs, valid_api_params, valid_func_params)

        endpoint = APIConfig.CURRENCY_MASTER_URL
        url = self.api_connector.build_url(self.api_connector.base_url, endpoint)
        debug = func_params.get("debug", False)
        json_response = func_params.get("json", False)

        if json_response:
            return self.api_connector.connect_to_api(url)  # Return raw JSON response
        return self.api_connector.fetch_data(url=url, debug=debug)

    def get_currency_quotes(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Retrieve current currency quotes from the API.

        Parameters:
            fecha (str, optional): Date in 'YYYY-MM-DD' format. If not provided, fetches the latest data.
            json (bool, optional): If True, returns the raw JSON response from the API. Defaults to False.
            debug (bool, optional): If True, returns the constructed URL instead of fetching data. Defaults to False.

        Returns:
            Union[str, pd.DataFrame, Dict[str, Any]]:
                - If `debug=True`, returns the constructed URL as a string.
                - If `json=True`, returns the raw JSON response as a dictionary.
                - Otherwise, returns the processed data as a pandas DataFrame.

        Raises:
            ValueError: If invalid parameters are provided.

        Example:
            >>> client = BCRAclient()
            >>> data = client.get_currency_quotes(fecha="2025-01-01")
        """
        valid_api_params = {"fecha"}
        valid_func_params = {"json", "debug"}

        api_params, func_params = self._validate_params(kwargs, valid_api_params, valid_func_params)

        endpoint = APIConfig.CURRENCY_QUOTES_URL
        url = self.api_connector.build_url(self.api_connector.base_url, endpoint, api_params)
        debug = func_params.get("debug", False)
        json_response = func_params.get("json", False)

        if json_response:
            return self.api_connector.connect_to_api(url)  # Return raw JSON response
        return self.api_connector.fetch_data(url=url, debug=debug, is_currency=True)

    def get_currency_timeseries(self, moneda: str, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Retrieve historical currency data for a specific currency.

        Parameters:
            moneda (str): Currency code (e.g., "USD").
            fechadesde (str, optional): Start date in 'YYYY-MM-DD' format.
            fechahasta (str, optional): End date in 'YYYY-MM-DD' format.
            limit (int, optional): Maximum number of results to fetch.
            offset (int, optional): Offset for pagination.
            json (bool, optional): If True, returns the raw JSON response from the API. Defaults to False.
            debug (bool, optional): If True, returns the constructed URL instead of fetching data. Defaults to False.

        Returns:
            Union[str, pd.DataFrame, Dict[str, Any]]:
                - If `debug=True`, returns the constructed URL as a string.
                - If `json=True`, returns the raw JSON response as a dictionary.
                - Otherwise, returns the processed data as a pandas DataFrame.

        Raises:
            ValueError: If invalid parameters are provided or if `moneda` is not specified.

        Example:
            >>> client = BCRAclient()
            >>> data = client.get_currency_timeseries(moneda="USD", fechadesde="2025-01-01", fechahasta="2025-03-31")
        """
        if not moneda:
            raise ValueError("El código de moneda es requerido")

        valid_api_params = {"fechadesde", "fechahasta", "limit", "offset"}
        valid_func_params = {"json", "debug"}

        api_params, func_params = self._validate_params(kwargs, valid_api_params, valid_func_params)

        endpoint = f"{APIConfig.CURRENCY_QUOTES_URL}/{moneda}"
        url = self.api_connector.build_url(self.api_connector.base_url, endpoint, api_params)
        debug = func_params.get("debug", False)
        json_response = func_params.get("json", False)

        if json_response:
            return self.api_connector.connect_to_api(url)  # Return raw JSON response
        return self.api_connector.fetch_data(url=url, debug=debug, is_timeseries=True)
