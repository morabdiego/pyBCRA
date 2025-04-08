from typing import Optional
import warnings
import requests
from .settings import APISettings, ERROR_MESSAGES
from .connector import APIConnector
from .base_api import create_api_class

MonetaryAPI = create_api_class('MonetaryAPI', APISettings.API_CONFIG['monetary'])
CurrencyAPI = create_api_class('CurrencyAPI', APISettings.API_CONFIG['currency'])
ChecksAPI = create_api_class('ChecksAPI', APISettings.API_CONFIG['checks'])
DebtorsAPI = create_api_class('DebtorsAPI', APISettings.API_CONFIG['debtors'])

class BCRAclient:
    """
    Cliente principal para acceder a los datos de la API del BCRA.

    Esta clase es la interfaz principal de la biblioteca y expone todas
    las APIs específicas de manera organizada, maneja la configuración
    de conexión y seguridad, y proporciona una interfaz simple y consistente.

    Attributes
    ----------
    monetary : MonetaryAPI
        API para variables monetarias
    currency : CurrencyAPI
        API para cotizaciones
    checks : ChecksAPI
        API para cheques
    debtors : DebtorsAPI
        API para deudores
    """

    def __init__(self, base_url: str = APISettings.BASE_URL,
                cert_path: Optional[str] = None, verify_ssl: bool = True):
        """
        Inicializa el cliente con la configuración de conexión.

        Parameters
        ----------
        base_url : str, optional
            URL base de la API del BCRA. Por defecto usa APISettings.BASE_URL
        cert_path : str, optional
            Ruta al certificado SSL para autenticación. Si es None y
            verify_ssl=True, usa APISettings.CERT_PATH. Si verify_ssl=False,
            se ignora
        verify_ssl : bool, default=True
            Si se debe verificar el certificado SSL. Si es False, deshabilita
            las advertencias SSL (no recomendado para producción)

        Notes
        -----
        Si verify_ssl se establece en False, se mostrará una advertencia sobre
        los riesgos de seguridad asociados.
        """

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
