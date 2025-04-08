from typing import Dict, Any, Union, Set, List
import logging
import requests
import pandas as pd
from urllib.parse import urlencode

from .settings import COLUMN_TYPES

def build_url(
    base_url: str,
    endpoint: str,
    params: Dict[str, Any] = None,
    path_params: Set[str] = None,
    query_params: Set[str] = None,
) -> str:
    """
    Construye una URL completa a partir de la URL base, el endpoint y los parámetros.

    Args:
        base_url: URL base del servicio
        endpoint: Endpoint de la API (puede contener placeholders {param})
        params: Diccionario con los valores de los parámetros
        path_params: Conjunto de parámetros que van en la ruta
        query_params: Conjunto de parámetros que van en la query string

    Returns:
        URL completa con todos los parámetros sustituidos
    """
    # Normalizar URL base
    url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    # Caso especial para endpoint monetario
    if '/monetarias/{id_variable}' in url and (not params or 'id_variable' not in params):
        url = url.replace('/monetarias/{id_variable}', '/monetarias')

    # Sin parámetros, retornar URL directamente
    if not params:
        return url

    # Procesar parámetros de ruta (path)
    if path_params:
        for key in path_params:
            if key in params:
                placeholder = f"{{{key}}}"
                if placeholder in url:
                    url = url.replace(placeholder, str(params[key]))

    # Procesar parámetros de consulta (query)
    query_dict = {}

    # Determinar los parámetros de consulta
    effective_query_params = query_params if query_params is not None else (
        set(params.keys()) - (path_params or set())
    )

    # Añadir solo parámetros relevantes a query_dict
    for key in effective_query_params:
        if key in params and params[key] is not None:
            placeholder = f"{{{key}}}"
            if placeholder not in url:
                query_dict[key] = params[key]

    # Añadir query params si existen
    return f"{url}?{urlencode(query_dict)}" if query_dict else url

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

    def fetch_data(self, url: str) -> pd.DataFrame:
        """Obtiene y procesa datos de la API."""
        # Obtener datos y transformarlos a DataFrame
        data = self.connect_to_api(url)
        if not data:
            return pd.DataFrame()

        # Crear DataFrame y asignar tipos de columna
        df = self._create_dataframe(data)
        return self._assign_column_types(df) if not df.empty else df

    def _handle_request_error(self, error: Exception) -> None:
        """Maneja errores de peticiones HTTP categorizándolos por tipo."""
        error_type = "SSL" if isinstance(error, requests.exceptions.SSLError) else \
                    "HTTP" if isinstance(error, requests.exceptions.HTTPError) else \
                    "inesperado"
        self.logger.error(f"Error {error_type}: {error}")

    def _create_dataframe(self, data: Any) -> pd.DataFrame:
        try:
            return self._transform_to_dataframe(data)
        except Exception as e:
            self.logger.error(f"Error creando DataFrame: {e}")
            return pd.DataFrame()

    def _assign_column_types(self, df: pd.DataFrame) -> pd.DataFrame:
        for col, dtype in COLUMN_TYPES.items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)
        return df

    def _transform_to_dataframe(self, data: Any) -> pd.DataFrame:
        """Transforma datos JSON en DataFrame."""
        if isinstance(data, dict) and 'results' in data:
            data = data['results']
        if not data:
            return pd.DataFrame()
        return self._json_to_df(data)

    def _flatten_dict(self, d: dict, parent_key: str = '', sep: str = '_') -> dict:
        """Aplana un diccionario anidado en un diccionario plano."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k

            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list) and all(isinstance(item, dict) for item in v):
                # Si la lista contiene diccionarios, procesar cada uno
                for i, item in enumerate(v):
                    items.extend(self._flatten_dict(
                        item, f"{new_key}{sep}{i}", sep=sep).items())
            else:
                items.append((new_key, v))

        return dict(items)

    def _json_to_df(self, json_data: Union[Dict, List]) -> pd.DataFrame:
        """Convierte datos JSON en DataFrame."""
        if isinstance(json_data, dict):
            flattened_dict = self._flatten_dict(json_data)
            return pd.DataFrame([flattened_dict])
        elif isinstance(json_data, list):
            if all(isinstance(item, dict) for item in json_data):
                flattened_list = [self._flatten_dict(item) for item in json_data]
                return pd.DataFrame(flattened_list)
            else:
                return pd.DataFrame(json_data)
