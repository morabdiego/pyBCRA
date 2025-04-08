from typing import Dict, Any, Union, Optional, Callable, Type
import pandas as pd
import json
from pathlib import Path
from functools import wraps

from .settings import APISettings, EndpointConfig
from .connector import APIConnector, build_url

APIResult = Union[str, pd.DataFrame, Dict[str, Any]]

def load_api_docs() -> Dict[str, Dict[str, str]]:
    """
    Carga la documentación de los endpoints desde un archivo JSON.
    Esta función permite mantener la documentación separada del código

    Estructura del archivo api_docs.json:
    {
        "api": {
            "método": "doscstring"
            }
    }
    """
    docs_path = Path(__file__).parent / 'api_docs.json'
    with open(docs_path, 'r', encoding='utf-8') as f:
        return json.load(f)

API_DOCS = load_api_docs()

def endpoint(method_name: str) -> Callable:
    """
    Decorador que simplifica la creación de métodos de API.

    Este decorador es fundamental para la generación dinámica de métodos ya que:
    1. Captura el nombre del método original
    2. Crea un wrapper que redirige a _make_api_call
    3. Mantiene la documentación y metadatos del método original

    Funcionamiento interno:
    1. Recibe el nombre del método (ej: 'base_monetaria')
    2. Crea un decorador que:
        - Recibe la función original
        - Crea un wrapper que llama a _make_api_call
        - Preserva los metadatos con @wraps
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, **kwargs) -> APIResult:
            return self._make_api_call(method_name, **kwargs)
        return wrapper
    return decorator

class BaseAPI:
    """
    Clase base abstracta para todas las APIs específicas.

    Esta clase implementa la lógica común para todas las APIs y es responsable de:
    1. Generar dinámicamente los métodos basados en la configuración
    2. Manejar las llamadas a la API de manera consistente
    3. Validar y procesar los parámetros de los métodos

    Estructura de la clase:
    - _api_config: Configuración de endpoints (debe ser definida por las clases hijas)
    - api_connector: Instancia para manejar las conexiones HTTP
    - Métodos generados dinámicamente para cada endpoint

    Ejemplo de uso:
    class MonetaryAPI(BaseAPI):
        _api_config = {
            'variables': EndpointConfig(...),
            'series': EndpointConfig(...)
        }
    """
    _api_config: Dict[str, EndpointConfig] = {}

    def __init__(self, connector: APIConnector):
        """
        Inicializa la API con un conector y genera los métodos dinámicamente.
        """
        self.api_connector = connector
        self._generate_methods()

    def _generate_methods(self) -> None:
        """
        Genera dinámicamente los métodos de la API basados en la configuración.
        """
        # Obtener el nombre base de la API para la documentación
        api_name = self.__class__.__name__.lower().replace('api', '')

        # Generar cada método definido en la configuración
        for method_name, endpoint_config in self._api_config.items():
            # Crear una función específica para este método
            def create_api_method(name):
                # Definimos el método real que será llamado
                def api_method(self, **kwargs):
                    return self._make_api_call(name, **kwargs)

                # Asignamos el nombre correcto al método
                api_method.__name__ = name

                # Asignamos la documentación desde API_DOCS
                api_method.__doc__ = API_DOCS.get(api_name, {}).get(name, "")

                # Aplicamos el decorador
                return endpoint(name)(api_method)

            # Crear el método y asignarlo a la clase
            api_method = create_api_method(method_name)
            setattr(self.__class__, method_name, api_method)

    def _make_api_call(self, method_name: str, **kwargs) -> APIResult:
        """
        Método principal que maneja todas las llamadas a la API.
        """
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
    """
    Factory que crea dinámicamente clases de API específicas.

    Args:
        name: Nombre de la nueva clase (ej: 'MonetaryAPI')
        api_config: Configuración de endpoints para la nueva API

    Returns:
        Type[BaseAPI]: Nueva clase de API lista para usar
    """
    return type(name, (BaseAPI,), {'_api_config': api_config})
