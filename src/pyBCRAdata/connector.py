import logging
import time
from typing import Optional, Dict, Any, Union, Literal
from urllib.parse import urlencode

import requests
import pandas as pd

from .config import APIConfig


class APIConnector:
    """
    A utility class for handling API connections and data fetching.
    Provides robust error handling, logging, and data transformation capabilities.
    """

    def __init__(
        self,
        base_url: str = APIConfig.BASE_URL,
        cert_path: Union[str, bool, None] = APIConfig.CERT_PATH,
        log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'
    ):
        self.base_url = base_url
        self.cert_path = cert_path

        # Configure logging
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def connect_to_api(
        self,
        endpoint: str,
        params: Optional[Dict[str, Union[str, int]]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Connect to the API and fetch data.

        Args:
            endpoint (str): API endpoint to connect to.
            params (Optional[Dict[str, Union[str, int]]]): Query parameters for the request.

        Returns:
            Optional[Dict[str, Any]]: Parsed JSON response from the API, or None if an error occurs.
        """
        url = self.build_url(self.base_url, endpoint, params)
        start_time = time.time()

        try:
            self.logger.debug(f"Connecting to URL: {url}")
            response = requests.get(url, verify=self.cert_path)
            response.raise_for_status()
            elapsed_time = time.time() - start_time
            self.logger.info(f"Request completed in {elapsed_time:.2f} seconds")
            return response.json()

        except Exception as error:
            self._handle_request_error(error)
            return None

    def _handle_request_error(self, error: Exception) -> None:
        """
        Handle errors during API requests.

        Args:
            error (Exception): The exception raised during the request.
        """
        if isinstance(error, requests.exceptions.SSLError):
            self.logger.error(f"SSL Error: {error}")
            self.logger.info("Consider providing a valid certificate path or disabling SSL verification")
        elif isinstance(error, requests.exceptions.HTTPError):
            self.logger.error(f"HTTP Error: {error}")
            if hasattr(error, 'response') and error.response is not None:
                self.logger.error(f"Response Content: {error.response.text}")
        elif isinstance(error, requests.exceptions.RequestException):
            self.logger.error(f"Request Error: {error}")
        else:
            self.logger.error(f"Unexpected Error: {error}")

    @staticmethod
    def build_url(
        base_url: str,
        endpoint: str,
        params: Optional[Dict[str, Union[str, int]]] = None
    ) -> str:
        """
        Build a complete URL with query parameters.

        Args:
            base_url (str): Base URL of the API.
            endpoint (str): API endpoint.
            params (Optional[Dict[str, Union[str, int]]]): Query parameters.

        Returns:
            str: Complete URL with query string.
        """
        # Ensure base_url ends with a slash and endpoint does not start with one
        base_url = base_url.rstrip("/")
        endpoint = endpoint.lstrip("/")
        url = f"{base_url}/{endpoint}"

        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            query_string = urlencode(filtered_params)
            url = f"{url}?{query_string}" if query_string else url

        return url

    def fetch_data(
        self,
        endpoint: str,
        params: Optional[Dict[str, Union[str, int]]] = None,
        results_key: str = 'results',
        debug: bool = False,
        is_currency: bool = False
    ) -> pd.DataFrame:
        """
        Fetch data from the API and process the response.

        Args:
            endpoint (str): API endpoint.
            params (Optional[Dict[str, Union[str, int]]]): Query parameters.
            results_key (str): Key to extract results from the API response.
            debug (bool): If True, returns the constructed URL instead of data.
            is_currency (bool): If True, processes the response as currency data.

        Returns:
            pd.DataFrame: Processed data as a DataFrame.
        """
        if params and not isinstance(params, dict):
            raise ValueError("Params must be a dictionary")

        full_url = self.build_url(self.base_url, endpoint, params)

        if debug:
            return str(full_url)

        try:
            data = self.connect_to_api(endpoint, params)

            if not data:
                self.logger.warning("No data received from API")
                return pd.DataFrame()

            results = data.get(results_key, data)

            if not results:
                self.logger.warning(f"No '{results_key}' found in API response")
                return pd.DataFrame()

            if is_currency:
                return self._process_currency_data(results)

            return pd.DataFrame(results)

        except Exception as e:
            self.logger.error(f"Error processing API data: {e}")
            return pd.DataFrame()

    def _process_currency_data(self, results: Any) -> pd.DataFrame:
        """
        Process currency-specific data from the API response.

        Args:
            results (Any): Raw results from the API.

        Returns:
            pd.DataFrame: Processed currency data as a DataFrame.
        """
        if isinstance(results, dict) and 'detalle' in results:
            df = pd.DataFrame(results['detalle'])
            df['fecha'] = results.get('fecha')
            return df
        else:
            self.logger.warning("Unexpected currency data structure")
            return pd.DataFrame()
