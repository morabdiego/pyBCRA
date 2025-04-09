from typing import Dict, Any, Union, Set, List
import logging
import requests
import pandas as pd
from urllib.parse import urlencode

from .settings import COLUMN_TYPES

SPECIAL_EXPLODE_ENDPOINTS = {
    "currency.rates",
    "debtors.debtors",
    "debtors.history",
    "checks.reported"
}

def build_url(
        base_url: str,
        endpoint: str, params: Dict[str, Any] = None,
        path_params: Set[str] = None,
        query_params: Set[str] = None
        ) -> str:

    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    if not params:
        return url

    if path_params:
        for key in path_params:
            if key in params:
                url = url.replace(f"{{{key}}}", str(params[key]))

    query_dict = {
        k: v for k, v in params.items()
        if k in (query_params or set()) and v is not None
    }

    return f"{url}?{urlencode(query_dict)}" if query_dict else url

class APIConnector:
    def __init__(self, base_url: str, cert_path: Union[str, bool, None]):
        self.base_url = base_url.rstrip('/')
        self.cert_path = cert_path
        self.logger = logging.getLogger(self.__class__.__name__)

    def connect_to_api(self, url: str) -> tuple[int, Dict[str, Any]]:
        try:
            response = requests.get(url, verify=self.cert_path)
            return response.status_code, response.json()
        except Exception as e:
            self._handle_request_error(e)
            return 0, {}

    def fetch_data(self, url: str, endpoint_key: str = "") -> pd.DataFrame:
        status_code, data = self.connect_to_api(url)

        if status_code != 200:
            return data

        if not data:
            return pd.DataFrame()

        try:
            df = self._transform_to_dataframe(data, endpoint_key)
            return self._assign_column_types(df) if not df.empty else df
        except Exception as e:
            self.logger.error(f"Error procesando datos: {e}")
            return pd.DataFrame()

    def _handle_request_error(self, error: Exception) -> None:
        error_type = "SSL" if isinstance(error, requests.exceptions.SSLError) else \
                    "HTTP" if isinstance(error, requests.exceptions.HTTPError) else "inesperado"
        self.logger.error(f"Error {error_type}: {error}")

    def _assign_column_types(self, df: pd.DataFrame) -> pd.DataFrame:
        for col, dtype in COLUMN_TYPES.items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)
        return df

    def _flatten_dict(self, d: dict, parent_key: str = '', sep: str = '_') -> dict:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                if all(isinstance(i, dict) for i in v):
                    items.append((new_key, v))
                else:
                    items.append((new_key, ";".join(map(str, v))))
            else:
                items.append((new_key, v))
        return dict(items)

    def _transform_to_dataframe(self, data: Any, endpoint_key: str = "") -> pd.DataFrame:
        if isinstance(data, dict) and 'results' in data:
            data = data['results']
        if not data:
            return pd.DataFrame()
        return self._json_to_df(data, endpoint_key)

    def _json_to_df(self, json_data: Union[Dict, List], endpoint_key: str = "") -> pd.DataFrame:
        should_explode = endpoint_key in SPECIAL_EXPLODE_ENDPOINTS

        if isinstance(json_data, dict):
            json_data = [json_data]
        elif not isinstance(json_data, list):
            return pd.DataFrame()

        flattened = [self._flatten_dict(item) for item in json_data]

        if not flattened:
            return pd.DataFrame()

        df = pd.DataFrame(flattened)

        if not should_explode:
            # Expandir listas de un solo dict en columnas
            for col in df.columns:
                if df[col].apply(lambda x: isinstance(x, list) and len(x) == 1 and isinstance(x[0], dict)).all():
                    expanded = pd.json_normalize(df[col].apply(lambda x: x[0]))
                    expanded.columns = [f"{col}_{subcol}" for subcol in expanded.columns]
                    df = pd.concat([df.drop(columns=[col]), expanded], axis=1)
            return df

        while True:
            list_columns = [col for col in df.columns if df[col].apply(lambda x: isinstance(x, list)).any()]
            if not list_columns:
                break

            col_to_explode = list_columns[0]
            df = df.explode(col_to_explode).reset_index(drop=True)

            if df[col_to_explode].apply(lambda x: isinstance(x, dict)).all():
                expanded_cols = pd.json_normalize(df[col_to_explode])
                expanded_cols.columns = [f"{col_to_explode}_{subcol}" for subcol in expanded_cols.columns]
                df = pd.concat([df.drop(columns=[col_to_explode]), expanded_cols], axis=1)

        return df
