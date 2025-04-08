from functools import wraps  # Para preservar metadatos de la función decorada
from typing import Callable, Any, Dict, Union, Set
import pandas as pd

from .settings import APISettings
from .connector import build_url

def api_call(func: Callable):
    """Decorador que maneja toda la lógica de las llamadas a la API"""

    @wraps(func)  # Preserva los metadatos de la función original
    def wrapper(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        # Obtener configuración del endpoint
        endpoint_name = func.__name__.replace('get_', '')
        endpoint_config = APISettings.ENDPOINTS[endpoint_name]

        # 1. Validar argumentos requeridos
        if missing := endpoint_config.required_args - kwargs.keys():
            raise ValueError(f"Faltan argumentos requeridos: {', '.join(missing)}")

        # 2. Validar que los parámetros sean válidos (unificado)
        path_params = endpoint_config.path_params
        query_params = endpoint_config.query_params
        valid_api_params = path_params | query_params
        valid_func_params = APISettings.COMMON_FUNC_PARAMS

        # Detectar parámetros inválidos
        if invalid := set(kwargs) - valid_api_params - valid_func_params:
            raise ValueError(
                f"Parámetros inválidos: {', '.join(invalid)}.\n\n"
                f"Permitidos API: {', '.join(valid_api_params) or 'Ninguno'}.\n"
                f"Permitidos función: {', '.join(valid_func_params)}."
            )

        # 3. Separar parámetros de API y de función (una sola vez)
        api_params = {k: v for k, v in kwargs.items() if k in valid_api_params}
        func_params = {k: v for k, v in kwargs.items() if k in valid_func_params}

        # 4. Construir URL directamente aquí (evitando llamada adicional)
        url = build_url(
            base_url=self.api_connector.base_url,
            endpoint=endpoint_config.endpoint,
            params=api_params,
            path_params=path_params,
            query_params=query_params
        )

        # 5. Realizar la petición según los parámetros de función
        if func_params.get("debug", False):
            return url
        elif func_params.get("json", False):
            return self.api_connector.connect_to_api(url)
        else:
            return self.api_connector.fetch_data(url)

    return wrapper
