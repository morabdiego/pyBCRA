from typing import Dict, Any, Union, Optional, Callable
import pandas as pd
import warnings
import requests
from functools import wraps

from .settings import APISettings, ERROR_MESSAGES
from .connector import APIConnector, build_url

# Tipo para resultados de API
APIResult = Union[str, pd.DataFrame, Dict[str, Any]]

def endpoint(endpoint_name: str) -> Callable:
    """Decorador para métodos que usan un endpoint específico."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, **kwargs) -> APIResult:
            self._current_endpoint = endpoint_name
            return self._make_api_call(**kwargs)
        return wrapper
    return decorator

class BCRAclient:
    """Cliente para acceder a los datos de la API del BCRA."""

    def __init__(self, base_url: str = APISettings.BASE_URL,
                cert_path: Optional[str] = None, verify_ssl: bool = True):
        """Inicializa el cliente BCRA con opciones de conexión."""
        if not verify_ssl:
            warnings.warn(ERROR_MESSAGES['ssl_disabled'], UserWarning)
            requests.packages.urllib3.disable_warnings()

        self.api_connector = APIConnector(
            base_url=base_url,
            cert_path=cert_path or (APISettings.CERT_PATH if verify_ssl else False)
        )

        # Generar métodos dinámicamente
        self._generate_methods()

    def _generate_methods(self) -> None:
        """Genera los métodos get_* dinámicamente basados en los endpoints configurados."""
        # Generar todos los métodos incluyendo los monetarios
        for endpoint_name in APISettings.ENDPOINTS:
            method_name = f"get_{endpoint_name}"
            docstring = f"Obtiene {endpoint_name.replace('_', ' ')}."

            def create_method(name: str, doc: str):
                @endpoint(name)
                def method(self, **kwargs) -> APIResult:
                    return self._make_api_call(**kwargs)
                method.__doc__ = doc
                return method

            setattr(self.__class__, method_name, create_method(endpoint_name, docstring))

    def _make_api_call(self, **kwargs) -> APIResult:
        """Realiza la llamada a la API con los parámetros dados."""
        endpoint_config = APISettings.ENDPOINTS[self._current_endpoint]

        # Validar argumentos requeridos
        if missing := endpoint_config.required_args - kwargs.keys():
            raise ValueError(f"Faltan argumentos requeridos: {', '.join(missing)}")

        # Validar parámetros
        valid_api_params = endpoint_config.path_params | endpoint_config.query_params
        valid_func_params = APISettings.COMMON_FUNC_PARAMS

        if invalid := set(kwargs) - valid_api_params - valid_func_params:
            raise ValueError(
                f"Parámetros inválidos: {', '.join(invalid)}.\n\n"
                f"Permitidos API: {', '.join(valid_api_params) or 'Ninguno'}.\n"
                f"Permitidos función: {', '.join(valid_func_params)}."
            )

        # Separar parámetros
        api_params = {k: v for k, v in kwargs.items() if k in valid_api_params}
        func_params = {k: v for k, v in kwargs.items() if k in valid_func_params}

        # Construir URL
        url = build_url(
            base_url=self.api_connector.base_url,
            endpoint=endpoint_config.endpoint,
            params=api_params,
            path_params=endpoint_config.path_params,
            query_params=endpoint_config.query_params
        )

        # Realizar petición
        if func_params.get("debug", False):
            return url
        elif func_params.get("json", False):
            return self.api_connector.connect_to_api(url)
        return self.api_connector.fetch_data(url)
