from typing import Dict, Any, Union, Optional, Callable, Type
import pandas as pd
import warnings
import requests
from functools import wraps

from .settings import APISettings, ERROR_MESSAGES, EndpointConfig
from .connector import APIConnector, build_url

APIResult = Union[str, pd.DataFrame, Dict[str, Any]]

def endpoint(method_name: str) -> Callable:
    """Decorador para métodos que usan un endpoint específico."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, **kwargs) -> APIResult:
            return self._make_api_call(method_name, **kwargs)
        return wrapper
    return decorator

class BaseAPI:
    """Clase base para APIs específicas."""
    _api_config: Dict[str, EndpointConfig] = {}

    def __init__(self, connector: APIConnector):
        self.api_connector = connector
        self._generate_methods()

    def _generate_methods(self) -> None:
        """Genera los métodos dinámicamente basados en los endpoints configurados."""
        for method_name, endpoint_config in self._api_config.items():
            docstring = f"Obtiene {method_name.replace('_', ' ')}."
            setattr(self.__class__, method_name,
                   endpoint(method_name)(lambda self, **kwargs: self._make_api_call(method_name, **kwargs)))
            getattr(self.__class__, method_name).__doc__ = docstring

    def _make_api_call(self, method_name: str, **kwargs) -> APIResult:
        endpoint_config = self._api_config[method_name]

        if missing := endpoint_config.required_args - kwargs.keys():
            raise ValueError(f"Faltan argumentos requeridos: {', '.join(missing)}")

        valid_api_params = endpoint_config.path_params | endpoint_config.query_params
        valid_func_params = APISettings.COMMON_FUNC_PARAMS

        if invalid := set(kwargs) - valid_api_params - valid_func_params:
            raise ValueError(
                f"Parámetros inválidos: {', '.join(invalid)}.\n\n"
                f"Permitidos API: {', '.join(valid_api_params) or 'Ninguno'}.\n"
                f"Permitidos función: {', '.join(valid_func_params)}."
            )

        api_params = {k: v for k, v in kwargs.items() if k in valid_api_params}
        func_params = {k: v for k, v in kwargs.items() if k in valid_func_params}
        url = build_url(
            base_url=self.api_connector.base_url,
            endpoint=endpoint_config.endpoint,
            params=api_params,
            path_params=endpoint_config.path_params,
            query_params=endpoint_config.query_params
        )

        if func_params.get("debug", False):
            return url
        elif func_params.get("json", False):
            return self.api_connector.connect_to_api(url)
        return self.api_connector.fetch_data(url)

def create_api_class(name: str, api_config: Dict[str, EndpointConfig]) -> Type[BaseAPI]:
    """Crea una clase de API con la configuración especificada."""
    return type(name, (BaseAPI,), {'_api_config': api_config})

# Crear clases de API específicas usando la configuración unificada
MonetaryAPI = create_api_class('MonetaryAPI', APISettings.API_CONFIG['monetary'])
CurrencyAPI = create_api_class('CurrencyAPI', APISettings.API_CONFIG['currency'])
ChecksAPI = create_api_class('ChecksAPI', APISettings.API_CONFIG['checks'])
DebtorsAPI = create_api_class('DebtorsAPI', APISettings.API_CONFIG['debtors'])

class BCRAclient:
    """Cliente para acceder a los datos de la API del BCRA."""

    def __init__(self, base_url: str = APISettings.BASE_URL,
                cert_path: Optional[str] = None, verify_ssl: bool = True):
        if not verify_ssl:
            warnings.warn(ERROR_MESSAGES['ssl_disabled'], UserWarning)
            requests.packages.urllib3.disable_warnings()

        connector = APIConnector(
            base_url=base_url,
            cert_path=cert_path or (APISettings.CERT_PATH if verify_ssl else False)
        )

        self.monetary = MonetaryAPI(connector)
        self.currency = CurrencyAPI(connector)
        self.checks = ChecksAPI(connector)
        self.debtors = DebtorsAPI(connector)
