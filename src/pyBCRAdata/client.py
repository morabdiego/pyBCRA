from typing import Optional
import warnings
import requests

from .settings import APISettings, ERROR_MESSAGES
from .connector import APIConnector
from .base_api import create_api_class

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
