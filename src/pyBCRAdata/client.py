from typing import Dict, Any, Union, Optional, Callable, Type
import pandas as pd
import warnings
import requests
import json
from pathlib import Path
from functools import wraps

from .settings import APISettings, ERROR_MESSAGES, EndpointConfig
from .connector import APIConnector, build_url

APIResult = Union[str, pd.DataFrame, Dict[str, Any]]

def load_api_docs() -> Dict[str, Dict[str, str]]:
    """
    Carga la documentación de los endpoints desde un archivo JSON.

    Esta función es clave para mantener la documentación separada del código,
    permitiendo actualizaciones sin modificar el código fuente.

    Estructura del archivo api_docs.json:
    {
        "monetary": {
            "base_monetaria": "Documentación del método base_monetaria...",
            "reservas": "Documentación del método reservas..."
        },
        "currency": {
            "cotizacion": "Documentación del método cotizacion..."
        }
    }

    Returns:
        Dict[str, Dict[str, str]]: Diccionario con la documentación de todos los endpoints
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

    Ejemplo de uso:
    @endpoint('base_monetaria')
    def base_monetaria(self, **kwargs):
        return self._make_api_call('base_monetaria', **kwargs)

    Args:
        method_name: Nombre del método que se está decorando

    Returns:
        Callable: Decorador que crea el wrapper para el método
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, **kwargs) -> APIResult:
            # Redirige la llamada al método _make_api_call con el nombre del método
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
            'base_monetaria': EndpointConfig(...)
        }
    """
    # Configuración de endpoints que debe ser definida por las clases hijas
    _api_config: Dict[str, EndpointConfig] = {}

    def __init__(self, connector: APIConnector):
        """
        Inicializa la API con un conector y genera los métodos dinámicamente.

        Args:
            connector: Instancia de APIConnector para manejar las conexiones HTTP
                        Debe contener:
                        - base_url: URL base de la API
                        - cert_path: Ruta al certificado SSL
                        - Métodos para realizar las llamadas HTTP
        """
        self.api_connector = connector
        self._generate_methods()

    def _generate_methods(self) -> None:
        """
        Genera dinámicamente los métodos de la API basados en la configuración.
        Este método es clave para la flexibilidad de la biblioteca ya que:
        1. Crea automáticamente los métodos para cada endpoint
        2. Asigna la documentación correspondiente
        3. Mantiene la consistencia entre la configuración y los métodos disponibles

        El proceso de generación sigue estos pasos:
        1. Obtener el nombre de la API (monetary, currency, etc.)
        2. Para cada endpoint en la configuración:
            - Obtener su documentación
            - Crear el método dinámicamente
            - Asignar la documentación si existe

        Parámetros de la configuración (_api_config):
        - method_name: Nombre del método a generar (ej: 'base_monetaria')
        - endpoint_config: Configuración del endpoint que contiene:
            * required_args: Conjunto de argumentos requeridos
            * path_params: Parámetros que van en la ruta de la URL
            * query_params: Parámetros que van en la query string
            * endpoint: Ruta base del endpoint

        Ejemplo de configuración:
        {
            'base_monetaria': EndpointConfig(
                required_args={'fecha'},
                path_params=set(),
                query_params={'fecha'},
                endpoint='/estadisticas/v1/principalesvariables'
            )
        }

        Nota:
        Los métodos generados son wrappers alrededor de _make_api_call,
        lo que permite mantener la lógica de llamadas a la API centralizada.
        """
        # Paso 1: Obtener el nombre de la API
        # Convierte el nombre de la clase (ej: MonetaryAPI) en el nombre de la API (monetary)
        # Esto se usa para buscar la documentación correcta en api_docs.json
        # Ejemplo: 'MonetaryAPI' -> 'monetary'
        api_name = self.__class__.__name__.lower().replace('api', '')

        # Paso 2: Generar métodos para cada endpoint
        # Itera sobre todos los endpoints definidos en la configuración
        # method_name: Nombre del método a generar (ej: 'base_monetaria')
        # endpoint_config: Configuración completa del endpoint
        for method_name, endpoint_config in self._api_config.items():
            # Subpaso 2.1: Obtener documentación
            # Busca la documentación en api_docs.json usando:
            # - Nombre de la API (ej: monetary)
            # - Nombre del método (ej: base_monetaria)
            # La estructura de api_docs.json es:
            # {
            #   "monetary": {
            #     "base_monetaria": "Documentación del método..."
            #   }
            # }
            docstring = API_DOCS.get(api_name, {}).get(method_name)

            # Subpaso 2.2: Crear el método dinámicamente
            # Explicación detallada de la creación del método:
            # 1. endpoint(method_name): Aplica el decorador que:
            #    - Captura el nombre del método
            #    - Prepara el wrapper para la llamada a la API
            #
            # 2. lambda self, **kwargs: ... : Crea una función anónima que:
            #    - Recibe self (instancia de la clase)
            #    - Recibe **kwargs (argumentos variables)
            #    - Llama a _make_api_call con:
            #      * method_name: Nombre del método original
            #      * **kwargs: Argumentos pasados al método
            #
            # 3. setattr: Asigna el método a la clase con:
            #    - self.__class__: La clase actual
            #    - method_name: Nombre del método
            #    - El resultado del decorador con la lambda
            #
            # Ejemplo de método generado:
            # def base_monetaria(self, **kwargs):
            #     return self._make_api_call('base_monetaria', **kwargs)
            setattr(self.__class__, method_name,
                   endpoint(method_name)(lambda self, **kwargs:
                       self._make_api_call(method_name, **kwargs)))

            # Subpaso 2.3: Asignar documentación
            # Si existe documentación en api_docs.json, la asigna al método
            # Esto permite tener ayuda en el IDE y generar documentación automática
            # La documentación se asigna usando:
            # - getattr: Obtiene el método recién creado
            # - __doc__: Atributo especial de Python para documentación
            if docstring:
                getattr(self.__class__, method_name).__doc__ = docstring

    def _make_api_call(self, method_name: str, **kwargs) -> APIResult:
        """
        Método principal que maneja todas las llamadas a la API.
        Este método es el corazón de la biblioteca y se encarga de:
        1. Validar los parámetros recibidos
        2. Construir la URL correcta para la llamada
        3. Manejar diferentes tipos de respuesta

        El flujo de ejecución es:
        1. Obtener la configuración del endpoint específico
        2. Validar que todos los parámetros requeridos estén presentes
        3. Separar y validar los parámetros de la API y de la función
        4. Construir la URL final con los parámetros correctos
        5. Decidir el tipo de respuesta según los parámetros de función

        Args:
            method_name: Nombre del método que se está llamando (ej: 'base_monetaria')
            **kwargs: Parámetros para la llamada a la API. Pueden ser:
                    - Parámetros de ruta (path_params)
                    - Parámetros de consulta (query_params)
                    - Parámetros de función (debug, json)

        Returns:
            APIResult: El resultado puede ser:
                    - str: La URL construida (si debug=True)
                    - Dict: Los datos en formato JSON (si json=True)
                    - pd.DataFrame: Los datos en formato DataFrame (por defecto)

        Raises:
            ValueError: Si faltan parámetros requeridos o hay parámetros inválidos
        """
        # Paso 1: Obtener la configuración del endpoint
        # Cada endpoint tiene su propia configuración con:
        # - Parámetros requeridos
        # - Parámetros de ruta
        # - Parámetros de consulta
        endpoint_config = self._api_config[method_name]

        # Paso 2: Validar parámetros requeridos
        # Verifica que todos los parámetros marcados como 'required' en la configuración
        # estén presentes en los kwargs recibidos
        if missing := endpoint_config.required_args - kwargs.keys():
            raise ValueError(f"Faltan argumentos requeridos: {', '.join(missing)}")

        # Paso 3: Definir y validar parámetros válidos
        # Los parámetros válidos son la unión de:
        # - Parámetros de ruta (ej: /api/{parametro})
        # - Parámetros de consulta (ej: ?parametro=valor)
        valid_api_params = endpoint_config.path_params | endpoint_config.query_params

        # Los parámetros de función son comunes a todos los endpoints
        # y controlan el comportamiento de la llamada
        valid_func_params = APISettings.COMMON_FUNC_PARAMS

        # Paso 4: Validar que no haya parámetros inválidos
        # Compara los parámetros recibidos con los válidos
        # y muestra un mensaje de error detallado si hay inválidos
        if invalid := set(kwargs) - valid_api_params - valid_func_params:
            raise ValueError(
                f"Parámetros inválidos: {', '.join(invalid)}.\n\n"
                f"Permitidos API: {', '.join(valid_api_params) or 'Ninguno'}.\n"
                f"Permitidos función: {', '.join(valid_func_params)}."
            )

        # Paso 5: Separar los parámetros
        # Divide los parámetros en dos grupos:
        # - api_params: Parámetros que van en la URL
        # - func_params: Parámetros que controlan el comportamiento
        api_params = {k: v for k, v in kwargs.items() if k in valid_api_params}
        func_params = {k: v for k, v in kwargs.items() if k in valid_func_params}

        # Paso 6: Construir la URL
        # Usa la función build_url para crear la URL final con:
        # - URL base
        # - Endpoint específico
        # - Parámetros de ruta y consulta
        url = build_url(
            base_url=self.api_connector.base_url,
            endpoint=endpoint_config.endpoint,
            params=api_params,
            path_params=endpoint_config.path_params,
            query_params=endpoint_config.query_params
        )

        # Paso 7: Decidir el tipo de respuesta
        # Según los parámetros de función, devuelve:
        # - La URL construida (para debugging)
        # - Los datos en formato JSON
        # - Los datos en formato DataFrame (por defecto)
        if func_params.get("debug", False):
            return url
        elif func_params.get("json", False):
            return self.api_connector.connect_to_api(url)
        return self.api_connector.fetch_data(url)

def create_api_class(name: str, api_config: Dict[str, EndpointConfig]) -> Type[BaseAPI]:
    """
    Factory que crea dinámicamente clases de API específicas.

    Esta función es clave para la flexibilidad del sistema ya que:
    1. Permite crear nuevas APIs sin modificar el código base
    2. Mantiene la consistencia entre todas las APIs
    3. Reduce la duplicación de código

    Funcionamiento:
    1. Recibe el nombre y configuración de la nueva API
    2. Crea una nueva clase que hereda de BaseAPI
    3. Asigna la configuración específica a la clase

    Ejemplo de uso:
    MonetaryAPI = create_api_class('MonetaryAPI', {
        'base_monetaria': EndpointConfig(...)
    })

    Args:
        name: Nombre de la nueva clase (ej: 'MonetaryAPI')
        api_config: Configuración de endpoints para la nueva API

    Returns:
        Type[BaseAPI]: Nueva clase de API lista para usar
    """
    return type(name, (BaseAPI,), {'_api_config': api_config})

# Creación de las clases específicas para cada tipo de dato del BCRA
MonetaryAPI = create_api_class('MonetaryAPI', APISettings.API_CONFIG['monetary'])
CurrencyAPI = create_api_class('CurrencyAPI', APISettings.API_CONFIG['currency'])
ChecksAPI = create_api_class('ChecksAPI', APISettings.API_CONFIG['checks'])
DebtorsAPI = create_api_class('DebtorsAPI', APISettings.API_CONFIG['debtors'])

class BCRAclient:
    """
    Cliente principal para acceder a los datos de la API del BCRA.

    Esta clase es la interfaz principal de la biblioteca y:
    1. Expone todas las APIs específicas de manera organizada
    2. Maneja la configuración de conexión y seguridad
    3. Proporciona una interfaz simple y consistente

    Estructura:
    - monetary: API para variables monetarias
    - currency: API para cotizaciones
    - checks: API para cheques
    - debtors: API para deudores

    Ejemplo de uso:
    client = BCRAclient()
    df = client.monetary.base_monetaria(fecha='2023-01-01')
    """

    def __init__(self, base_url: str = APISettings.BASE_URL,
                cert_path: Optional[str] = None, verify_ssl: bool = True):
        """
        Inicializa el cliente con la configuración de conexión.

        Args:
            base_url: URL base de la API del BCRA
                        Por defecto usa APISettings.BASE_URL

            cert_path: Ruta al certificado SSL para autenticación
                        Si es None y verify_ssl=True, usa APISettings.CERT_PATH
                        Si verify_ssl=False, se ignora

            verify_ssl: Si se debe verificar el certificado SSL
                        Si es False, deshabilita las advertencias SSL
                        No recomendado para producción
        """
        # Manejo de advertencias SSL
        if not verify_ssl:
            warnings.warn(ERROR_MESSAGES['ssl_disabled'], UserWarning)
            requests.packages.urllib3.disable_warnings()

        # Crea el conector con la configuración SSL
        connector = APIConnector(
            base_url=base_url,
            cert_path=cert_path or (APISettings.CERT_PATH if verify_ssl else False)
        )

        # Inicializa todas las APIs específicas
        # Cada API recibe el mismo conector para mantener la consistencia
        self.monetary = MonetaryAPI(connector)
        self.currency = CurrencyAPI(connector)
        self.checks = ChecksAPI(connector)
        self.debtors = DebtorsAPI(connector)
