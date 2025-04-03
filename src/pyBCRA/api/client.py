from typing import Dict, Any, Union, Optional, Set, Tuple
import pandas as pd
import warnings
import requests

from ..config.settings import APISettings
from .connector import APIConnector
from .decorators import api_response_handler
from ..utils.validators import ParamValidator
from ..utils.url import URLBuilder

class BCRAclient:
    """Cliente para acceder a los datos de la API del BCRA."""

    def __init__(
        self,
        base_url: str = APISettings.BASE_URL,
        cert_path: Optional[str] = None,
        verify_ssl: bool = True
    ):
        """
        Inicializa el cliente BCRA.

        Args:
            base_url: URL base de la API
            cert_path: Ruta al certificado SSL
            verify_ssl: Si debe verificar SSL
        """
        self._setup_ssl(verify_ssl)
        self.api_connector = self._create_connector(base_url, cert_path, verify_ssl)

    def _setup_ssl(self, verify_ssl: bool) -> None:
        """Configura la verificación SSL."""
        if not verify_ssl:
            warnings.warn(
                "Verificación SSL desactivada - no recomendado para producción",
                UserWarning
            )
            requests.packages.urllib3.disable_warnings()

    def _create_connector(
            self, base_url: str,
            cert_path: Optional[str],
            verify_ssl: bool
            ) -> APIConnector:
        """Crea y configura el conector de API."""
        return APIConnector(
            base_url=base_url,
            cert_path=cert_path or (APISettings.CERT_PATH if verify_ssl else False)
        )

    def _validate_params(self, params: Dict[str, Any], valid_api_params: Set[str]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Valida parámetros usando ParamValidator."""
        return ParamValidator.validate_params(
            params,
            valid_api_params,
            APISettings.COMMON_FUNC_PARAMS
        )

    @api_response_handler
    def get_monetary_data(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Obtiene datos monetarios.

        Args:
            id_variable: ID de la variable monetaria
            desde: Fecha inicio (YYYY-MM-DD)
            hasta: Fecha fin (YYYY-MM-DD)
            limit: Límite de resultados
            offset: Desplazamiento para paginación
        """
        pass

    @api_response_handler
    def get_currency_master(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """Obtiene el maestro de divisas."""
        pass

    @api_response_handler
    def get_currency_quotes(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Obtiene cotizaciones de divisas.

        Args:
            fecha: Fecha de cotización (YYYY-MM-DD)
        """
        pass

    @api_response_handler
    def get_currency_timeseries(
        self,
        moneda: str,
        **kwargs
    ) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Obtiene series temporales de divisas.

        Args:
            moneda: Código de moneda (ej: "USD")
            fechadesde: Fecha inicio (YYYY-MM-DD)
            fechahasta: Fecha fin (YYYY-MM-DD)
            limit: Límite de resultados
            offset: Desplazamiento para paginación
        """
        pass
