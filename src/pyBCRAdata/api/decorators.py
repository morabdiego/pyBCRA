from functools import wraps  # Para preservar metadatos de la función decorada
from typing import Callable, Any, Dict, Set, Union
import pandas as pd

from ..config.settings import APISettings

def api_response_handler(func: Callable):
    """Decorador que maneja toda la lógica de las llamadas a la API"""

    @wraps(func)  # Preserva los metadatos de la función original
    def wrapper(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        endpoint_name = func.__name__.replace('get_', '')
        endpoint_config = APISettings.ENDPOINTS[endpoint_name]

        # Verifica argumentos requeridos en kwargs
        if endpoint_config.required_args:
            missing_args = endpoint_config.required_args - kwargs.keys()
            if missing_args:
                raise ValueError(
                    f"Faltan argumentos requeridos: {', '.join(missing_args)}"
                )

        # Combina parámetros válidos y requeridos
        valid_params = endpoint_config.params | endpoint_config.required_args
        # Valida y separa parámetros de API y función
        api_params, func_params = self._validate_params(kwargs, valid_params)

        # Construye la URL final con todos los parámetros
        url = self.api_connector.build_url(endpoint_config.endpoint, api_params)

        # Si se solicita JSON, retorna la respuesta directa de la API
        if func_params.get("json", False):
            return self.api_connector.connect_to_api(url)

        # Por defecto, procesa y retorna los datos según el formato configurado
        return self.api_connector.fetch_data(
            url=url,
            data_format=endpoint_config.format,
            debug=func_params.get("debug", False)
        )

    return wrapper
