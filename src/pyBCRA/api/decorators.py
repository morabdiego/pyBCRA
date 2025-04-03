from functools import wraps
from typing import Callable, Any, Dict, Set, Union
import pandas as pd

from ..config.settings import APISettings

def api_response_handler(func: Callable):
    """
    Decorador para manejar las respuestas de la API.

    Maneja:
    - Validación de parámetros
    - Construcción de URL
    - Procesamiento de respuesta
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        endpoint_name = func.__name__.replace('get_', '')
        endpoint_config = APISettings.ENDPOINTS[endpoint_name]

        # Validar argumentos posicionales
        if args and endpoint_config.required_args:
            if len(args) != len(endpoint_config.required_args):
                raise ValueError(
                    f"Argumentos requeridos: {', '.join(endpoint_config.required_args)}"
                )
            kwargs.update(dict(zip(endpoint_config.required_args, args)))

        # Validar y procesar parámetros
        valid_params = endpoint_config.params | endpoint_config.required_args
        api_params, func_params = self._validate_params(kwargs, valid_params)

        # Extraer parámetros especiales
        currency = api_params.pop('moneda', None) if 'moneda' in endpoint_config.required_args else None

        # Construir URL y obtener respuesta
        url = self.api_connector.build_url(endpoint_config.endpoint, api_params, currency)

        if func_params.get("json", False):
            return self.api_connector.connect_to_api(url)

        return self.api_connector.fetch_data(
            url=url,
            data_format=endpoint_config.format,
            debug=func_params.get("debug", False)
        )

    return wrapper
