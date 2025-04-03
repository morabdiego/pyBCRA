from typing import Optional, Dict, Any, Union
import logging
import requests
import pandas as pd

from ..config.settings import DataFormat
from ..utils.url import URLBuilder
from ..config.constants import COLUMN_TYPES

class APIConnector:
    """Conector base para realizar llamadas a la API."""

    def __init__(self, base_url: str, cert_path: Union[str, bool, None]):
        """
        Inicializa el conector.

        Args:
            base_url: URL base de la API
            cert_path: Ruta al certificado SSL o False para deshabilitar verificación
        """
        self.base_url = base_url.rstrip('/')
        self.cert_path = cert_path
        self.logger = logging.getLogger(self.__class__.__name__)

    def connect_to_api(self, url: str) -> Dict[str, Any]:
        """
        Realiza la conexión a la API.

        Args:
            url: URL completa del endpoint

        Returns:
            Dict con la respuesta de la API
        """
        try:
            response = requests.get(url, verify=self.cert_path)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error(e)
            return {}

    def fetch_data(
            self,
            url: str,
            data_format: DataFormat,
            debug: bool = False
            ) -> Union[str, pd.DataFrame]:
        """
        Obtiene y procesa datos de la API.

        Args:
            url: URL del endpoint
            data_format: Formato de datos esperado
            debug: Si es True, retorna la URL sin hacer la petición
        """
        if debug:
            return url

        data = self.connect_to_api(url)
        if not data:
            return pd.DataFrame()

        df = self._create_dataframe(data.get('results', data), data_format)
        if not df.empty:
            df = self._assign_column_types(df)

        return df

    def build_url(self, endpoint: str, params: Dict[str, Any], currency: Optional[str] = None) -> str:
        """Construye URL usando URLBuilder."""
        return URLBuilder.build_url(self.base_url, endpoint, params, currency)

    def _handle_request_error(self, error: Exception) -> None:
        """Maneja errores de peticiones HTTP."""
        if isinstance(error, requests.exceptions.SSLError):
            self.logger.error(f"Error SSL: {error}")
        elif isinstance(error, requests.exceptions.HTTPError):
            self.logger.error(f"Error HTTP: {error}")
        else:
            self.logger.error(f"Error inesperado: {error}")

    def _create_dataframe(self, data: Any, data_format: DataFormat) -> pd.DataFrame:
        """Crea DataFrame según el formato de datos."""
        try:
            if data_format == DataFormat.CURRENCY and isinstance(data, dict):
                df = pd.DataFrame(data.get('detalle', []))
                if not df.empty:
                    df['fecha'] = data.get('fecha')

            elif data_format == DataFormat.TIMESERIES and isinstance(data, list):
                flattened_data = [
                    {**detalle, 'fecha': entry['fecha']}
                    for entry in data
                    for detalle in entry.get('detalle', [])
                ]
                df = pd.DataFrame(flattened_data)

            elif data_format == DataFormat.MONETARY:
                df = pd.DataFrame(data)

            elif data_format == DataFormat.MASTER:
                df = pd.DataFrame(data)

            else:
                self.logger.warning(f"Formato de datos desconocido: {data_format}")
                df = pd.DataFrame(data)

            return df

        except Exception as e:
            self.logger.error(f"Error creando DataFrame: {e}")
            return pd.DataFrame()

    def _assign_column_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Asigna tipos de columna según configuración."""
        for col, dtype in COLUMN_TYPES.items():
            if col in df.columns:
                try:
                    df[col] = df[col].astype(dtype)
                except Exception as e:
                    self.logger.warning(f"Error convirtiendo columna {col}: {e}")
        return df
