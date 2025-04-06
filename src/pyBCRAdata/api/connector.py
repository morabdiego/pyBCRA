from typing import Dict, Any, Union, Set
import logging
import requests
import pandas as pd

from ..utils.url import URLBuilder
from ..config.constants import COLUMN_TYPES
from ..utils.transformers import DataFrameTransformer

class APIConnector:
    """Conector base para realizar llamadas a la API."""

    def __init__(self, base_url: str, cert_path: Union[str, bool, None]):
        """Inicializa el conector con URL base y configuración SSL."""
        self.base_url = base_url.rstrip('/')
        self.cert_path = cert_path
        self.logger = logging.getLogger(self.__class__.__name__)

    def connect_to_api(self, url: str) -> Dict[str, Any]:
        """Realiza la conexión a la API y retorna la respuesta JSON."""
        try:
            response = requests.get(url, verify=self.cert_path)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e)
            return {}

    def fetch_data(self, url: str, debug: bool = False) -> Union[str, pd.DataFrame]:
        """Obtiene y procesa datos de la API."""
        if debug:
            return url

        # Obtener datos y transformarlos a DataFrame
        data = self.connect_to_api(url)
        if not data:
            return pd.DataFrame()

        # Crear DataFrame y asignar tipos de columna
        df = self._create_dataframe(data)
        return self._assign_column_types(df) if not df.empty else df

    def build_url(self, endpoint: str, params: Dict[str, Any], path_params: Set[str] = None, query_params: Set[str] = None) -> str:
        """Construye URL usando URLBuilder."""
        return URLBuilder.build_url(
            base_url=self.base_url,
            endpoint=endpoint,
            params=params,
            path_params=path_params,
            query_params=query_params
        )

    def _handle_request_error(self, error: Exception) -> None:
        """Maneja errores de peticiones HTTP categorizándolos por tipo."""
        error_type = "SSL" if isinstance(error, requests.exceptions.SSLError) else \
                    "HTTP" if isinstance(error, requests.exceptions.HTTPError) else \
                    "inesperado"
        self.logger.error(f"Error {error_type}: {error}")

    def _create_dataframe(self, data: Any) -> pd.DataFrame:
        """Crea DataFrame usando el transformador."""
        try:
            return DataFrameTransformer.transform(data)
        except Exception as e:
            self.logger.error(f"Error creando DataFrame: {e}")
            return pd.DataFrame()

    def _assign_column_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Asigna tipos de columna según configuración global."""
        for col, dtype in COLUMN_TYPES.items():
            if col in df.columns:
                try:
                    df[col] = df[col].astype(dtype)
                except Exception as e:
                    self.logger.warning(f"Error convirtiendo columna {col}: {e}")
        return df
