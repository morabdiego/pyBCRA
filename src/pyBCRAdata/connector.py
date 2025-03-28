import logging
from typing import Optional, Dict, Any, Union, Literal
from urllib.parse import urlencode

import requests
import pandas as pd

from .config import APIConfig

class APIConnector:
    """
    A comprehensive utility class for handling API connections and data fetching.
    Provides robust error handling, logging, and data transformation capabilities.
    """

    def __init__(
        self,
        base_url: str = APIConfig.BASE_URL,
        cert_path: Union[str, bool, None] = APIConfig.CERT_PATH,
        log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'
    ):
        """
        Initialize the APIConnector with base configuration.

        Args:
            base_url (str): Base URL for the API
            cert_path (Union[str, bool, None]): Path to SSL certificate, False to disable verification,
                                                or None to use system certificates
            log_level (Literal): Logging level for the connector
        """
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
        Establish a connection to the API with comprehensive error handling.

        Args:
            endpoint (str): API endpoint
            params (Optional[Dict]): Optional query parameters

        Returns:
            Optional[Dict[str, Any]]: Parsed JSON response or None
        """
        url = self.build_url(endpoint, params)

        try:
            self.logger.debug(f"Connecting to URL: {url}")
            response = requests.get(url, verify=self.cert_path)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()

        except requests.exceptions.SSLError as ssl_error:
            self.logger.error(f"SSL Error: {ssl_error}")
            self.logger.info("Consider providing a valid certificate path or disabling SSL verification")
        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f"HTTP Error: {http_err}")
            self.logger.error(f"Response Content: {http_err.response.text}")
        except requests.exceptions.RequestException as req_err:
            self.logger.error(f"Request Error: {req_err}")

        return None

    @staticmethod
    def build_url(
        endpoint: str,
        params: Optional[Dict[str, Union[str, int]]] = None
    ) -> str:
        """
        Construct a URL with optional query parameters.

        Args:
            endpoint (str): API endpoint
            params (Optional[Dict]): Optional query parameters

        Returns:
            str: Fully constructed URL
        """
        url = endpoint
        if params:
            # Filter out None values and encode parameters
            filtered_params = {k: v for k, v in params.items() if v is not None}
            query_string = urlencode(filtered_params)

            url = f"{url}?{query_string}" if query_string else url

        return url

    def fetch_data(
        self,
        endpoint: str,
        params: Optional[Dict[str, Union[str, int]]] = None,
        results_key: str = 'results',
        debug: bool = False
    ) -> pd.DataFrame:
        """
        Fetch data from the API and transform it into a pandas DataFrame.

        Args:
            endpoint (str): API endpoint
            params (Optional[Dict]): Optional query parameters
            results_key (str): Key containing the data in the response
            debug (bool): Return URL instead of fetching data

        Returns:
            pd.DataFrame: Parsed data or empty DataFrame
        """
        full_url = self.build_url(endpoint, params)

        if debug:
            return pd.DataFrame({'url': [full_url]})

        try:
            data = self.connect_to_api(endpoint, params)

            if not data:
                self.logger.warning("No data received from API")
                return pd.DataFrame()

            results = data.get(results_key, data)

            if not results:
                self.logger.warning(f"No '{results_key}' found in API response")
                return pd.DataFrame()

            return pd.DataFrame(results)

        except Exception as e:
            self.logger.error(f"Error processing API data: {e}")
            return pd.DataFrame()
