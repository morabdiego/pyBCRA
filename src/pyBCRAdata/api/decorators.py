from functools import wraps  # Para preservar metadatos de la función decorada
from typing import Callable, Any, Dict, Union
import pandas as pd

from ..config.settings import APISettings

def api_response_handler(func: Callable):
    """Decorador que maneja toda la lógica de las llamadas a la API"""

    @wraps(func)  # Preserva los metadatos de la función original
    def wrapper(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        # Obtener configuración y verificar argumentos requeridos
        endpoint_name = func.__name__.replace('get_', '')
        endpoint_config = APISettings.ENDPOINTS[endpoint_name]

        if missing := endpoint_config.required_args - kwargs.keys():
            raise ValueError(f"Faltan argumentos requeridos: {', '.join(missing)}")

        # Obtener parámetros de path y query
        path_params = getattr(endpoint_config, 'path_params', set())
        query_params = getattr(endpoint_config, 'query_params', set())

        # Para compatibilidad con versiones anteriores
        all_api_params = path_params | query_params
        if not all_api_params and hasattr(endpoint_config, 'params'):
            all_api_params = endpoint_config.params

        # Validar, construir URL y retornar resultado
        api_params, func_params = self._validate_params(kwargs, all_api_params | endpoint_config.required_args)
        url = self.api_connector.build_url(
            endpoint=endpoint_config.endpoint,
            params=api_params,
            path_params=path_params,
            query_params=query_params
        )

        return self.api_connector.connect_to_api(url) if func_params.get("json", False) else \
               self.api_connector.fetch_data(url=url, debug=func_params.get("debug", False))
    return wrapper
