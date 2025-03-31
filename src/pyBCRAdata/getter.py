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

    def get_monetary_data(self, **kwargs) -> Union[pd.DataFrame, dict]:
        """
        Retrieve monetary data from the API.
        """
        valid_params = {"id_variable", "desde", "hasta", "offset", "limit", "debug", "return_json"}
        params = self._validate_and_filter_params(kwargs, valid_params)
        endpoint = self._build_endpoint(APIConfig.MONETARY_ENDPOINT, params.pop("id_variable", ""))
        return self._fetch_and_process(endpoint, params, params.pop("debug", False), params.pop("return_json", False))

    def get_currency_master(self, **kwargs) -> Union[pd.DataFrame, dict]:
        """
        Retrieve master currency data from the API.
        """
        valid_params = {"debug", "return_json"}
        params = self._validate_and_filter_params(kwargs, valid_params)
        endpoint = self._build_endpoint(APIConfig.CURRENCY_MASTER_URL)
        return self._fetch_and_process(endpoint, params, params.pop("debug", False), params.pop("return_json", False), is_currency=True)

    def get_currency_quotes(self, **kwargs) -> Union[pd.DataFrame, dict]:
        """
        Retrieve current currency quotes from the API.
        """
        valid_params = {"debug", "return_json"}
        params = self._validate_and_filter_params(kwargs, valid_params)
        endpoint = self._build_endpoint(APIConfig.CURRENCY_QUOTES_URL)
        return self._fetch_and_process(endpoint, params, params.pop("debug", False), params.pop("return_json", False), is_currency=True)

    def get_currency_timeseries(self, moneda: str, **kwargs) -> Union[pd.DataFrame, dict]:
        """
        Retrieve historical currency data for a specific currency.
        """
        if not moneda:
            raise ValueError("El código de moneda es requerido")

        valid_params = {"fechadesde", "fechahasta", "offset", "limit", "debug", "return_json"}
        params = self._validate_and_filter_params(kwargs, valid_params)
        endpoint = self._build_endpoint(APIConfig.CURRENCY_QUOTES_URL, moneda)
        return self._fetch_and_process(endpoint, params, params.pop("debug", False), params.pop("return_json", False), is_currency=True)

    def _validate_and_filter_params(self, kwargs: Dict[str, Any], valid_params: set) -> Dict[str, Any]:
        """
        Validate and filter input parameters.
        """
        filtered_params = {k: v for k, v in kwargs.items() if k in valid_params and v is not None}
        invalid_params = set(kwargs.keys()) - valid_params
        if invalid_params:
            raise ValueError(f"Invalid parameters: {', '.join(invalid_params)}")
        return filtered_params

    def _build_endpoint(self, endpoint: str, resource: Optional[str] = None) -> str:
        """
        Build a complete API endpoint URL.

        Args:
            endpoint (str): API endpoint.
            resource (Optional[str]): Additional resource to append to the endpoint.

        Returns:
            str: Complete URL.
        """
        full_endpoint = f"{endpoint}/{resource}".rstrip("/") if resource else endpoint
        return self.api_connector.build_url(self.api_connector.base_url, full_endpoint)

    def _fetch_and_process(
        self,
        endpoint: str,
        params: Dict[str, Any],
        debug: bool,
        return_json: bool,
        is_currency: bool = False
    ) -> Union[pd.DataFrame, dict]:
        """
        Fetch data from the API and process the response.
        """
        response = self.api_connector.fetch_data(
            endpoint=endpoint,
            params=params,
            debug=debug,
            is_currency=is_currency
        )
        return self._process_response(response, return_json)

    def _process_response(self, response: Union[dict, pd.DataFrame], return_json: bool) -> Union[pd.DataFrame, dict]:
        """
        Process the API response into the desired format.
        """
        if return_json:
            return response.to_dict("records") if isinstance(response, pd.DataFrame) else response
        return pd.DataFrame(response) if isinstance(response, dict) else response
