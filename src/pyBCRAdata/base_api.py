from typing import Dict, Any, Union, Optional, Callable, Type
import pandas as pd
import json
from pathlib import Path
from functools import wraps

from .settings import APISettings, EndpointConfig
from .connector import APIConnector, build_url

APIResult = Union[str, pd.DataFrame, Dict[str, Any]]

def load_api_docs() -> Dict[str, Dict[str, str]]:
    docs_path = Path(__file__).parent / 'api_docs.json'
    with open(docs_path, 'r', encoding='utf-8') as f:
        return json.load(f)

API_DOCS = load_api_docs()

def endpoint(method_name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, **kwargs) -> APIResult:
            return self._make_api_call(method_name, **kwargs)
        return wrapper
    return decorator

class BaseAPI:
    _api_config: Dict[str, EndpointConfig] = {}

    def __init__(self, connector: APIConnector):
        self.api_connector = connector
        self._generate_methods()

    def _generate_methods(self) -> None:
        api_name = self.__class__.__name__.lower().replace('api', '')

        for method_name, endpoint_config in self._api_config.items():
            def create_api_method(name):
                def api_method(self, **kwargs):
                    return self._make_api_call(name, **kwargs)

                api_method.__name__ = name
                api_method.__doc__ = API_DOCS.get(api_name, {}).get(name, "")
                return endpoint(name)(api_method)

            api_method = create_api_method(method_name)
            setattr(self.__class__, method_name, api_method)

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

        # 🔥 Construimos el endpoint_key para pasarlo
        api_name = self.__class__.__name__.lower().replace('api', '')
        endpoint_key = f"{api_name}.{method_name}"

        if func_params.get("debug", False):
            return url
        elif func_params.get("json", False):
            return self.api_connector.connect_to_api(url)
        return self.api_connector.fetch_data(url, endpoint_key=endpoint_key)

def create_api_class(name: str, api_config: Dict[str, EndpointConfig]) -> Type[BaseAPI]:
    return type(name, (BaseAPI,), {'_api_config': api_config})
