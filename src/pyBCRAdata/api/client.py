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

    @api_response_handler
    def get_monetary_data(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Obtiene datos monetarios del BCRA.

        Parameters
        ----------
        id_variable : int
            ID de la variable monetaria
        desde : str
            Fecha inicio (YYYY-MM-DD)
        hasta : str
            Fecha fin (YYYY-MM-DD)
        limit : int, optional
            Límite de resultados
        offset : int, optional
            Desplazamiento para paginación
        json : bool, optional
            Devuelve respuesta JSON sin procesar
        debug : bool, optional
            Devuelve la URL sin hacer la petición

        Returns
        -------
        Union[str, pd.DataFrame, Dict[str, Any]]
            Serie temporal de datos monetarios para la variable solicitada

        Examples
        --------
        >>> client = BCRAclient()
        >>> df = client.get_monetary_data(id_variable=1, desde="2020-01-01", hasta="2020-12-31")
        """
        pass

    @api_response_handler
    def get_currency_master(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Obtiene el maestro de divisas (catálogo de monedas).

        Parameters
        ----------
        json : bool, optional
            Devuelve respuesta JSON sin procesar
        debug : bool, optional
            Devuelve la URL sin hacer la petición

        Returns
        -------
        Union[str, pd.DataFrame, Dict[str, Any]]
            Listado de divisas con sus códigos ISO y descripción

        Examples
        --------
        >>> client = BCRAclient()
        >>> df = client.get_currency_master()
        """
        pass

    @api_response_handler
    def get_currency_quotes(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Obtiene cotizaciones de divisas para una fecha específica.

        Parameters
        ----------
        fecha : str
            Fecha de cotización (YYYY-MM-DD)
        json : bool, optional
            Devuelve respuesta JSON sin procesar
        debug : bool, optional
            Devuelve la URL sin hacer la petición

        Returns
        -------
        Union[str, pd.DataFrame, Dict[str, Any]]
            Cotizaciones de todas las divisas para la fecha especificada

        Examples
        --------
        >>> client = BCRAclient()
        >>> df = client.get_currency_quotes(fecha="2023-01-15")
        """
        pass

    @api_response_handler
    def get_currency_timeseries(
        self,
        **kwargs
    ) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Obtiene series temporales de cotizaciones para una divisa específica.

        Parameters
        ----------
        moneda : str
            Código de moneda ISO (ej: "USD") (obligatorio)
        fechadesde : str, optional
            Fecha inicio (YYYY-MM-DD)
        fechahasta : str, optional
            Fecha fin (YYYY-MM-DD)
        limit : int, optional
            Límite de resultados
        offset : int, optional
            Desplazamiento para paginación
        json : bool, optional
            Devuelve respuesta JSON sin procesar
        debug : bool, optional
            Devuelve la URL sin hacer la petición

        Returns
        -------
        Union[str, pd.DataFrame, Dict[str, Any]]
            Serie temporal de cotizaciones para la divisa solicitada

        Examples
        --------
        >>> client = BCRAclient()
        >>> df = client.get_currency_timeseries(moneda="USD", fechadesde="2023-01-01", fechahasta="2023-12-31")
        """
        pass

    @api_response_handler
    def get_checks_master(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Obtiene el listado de entidades bancarias que operan con cheques.

        Parameters
        ----------
        json : bool, optional
            Devuelve respuesta JSON sin procesar
        debug : bool, optional
            Devuelve la URL sin hacer la petición

        Returns
        -------
        Union[str, pd.DataFrame, Dict[str, Any]]
            DataFrame con:

            - codigoEntidad : Código de la entidad bancaria
            - denominacion : Nombre de la entidad bancaria

        Examples
        --------
        >>> client = BCRAclient()
        >>> df = client.get_checks_master()
        """
        pass

    @api_response_handler
    def get_checks_reported(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Obtiene información de cheques denunciados.

        Parameters
        ----------
        codigo_entidad : int
            Código de la entidad bancaria (obligatorio)
        numero_cheque : int
            Número del cheque a consultar (obligatorio)
        json : bool, optional
            Devuelve respuesta JSON sin procesar
        debug : bool, optional
            Devuelve la URL sin hacer la petición

        Returns
        -------
        Union[str, pd.DataFrame, Dict[str, Any]]
            Información del cheque denunciado, incluyendo detalles de denuncia
            y entidad bancaria

        Examples
        --------
        >>> client = BCRAclient()
        >>> result = client.get_checks_reported(codigo_entidad=123, numero_cheque=456789)
        """
        pass

    @api_response_handler
    def get_debts(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Obtiene información de deudas registradas por CUIT/CUIL.

        Parameters
        ----------
        identificacion : str
            CUIT/CUIL del titular a consultar (obligatorio)
        json : bool, optional
            Devuelve respuesta JSON sin procesar
        debug : bool, optional
            Devuelve la URL sin hacer la petición

        Returns
        -------
        Union[str, pd.DataFrame, Dict[str, Any]]
            Información de deudas registradas con columnas:

            - identificacion : CUIT/CUIL consultado
            - denominacion : Nombre del titular
            - periodo : Periodo informado (YYYYMM)
            - entidad : Nombre de la entidad financiera
            - situacion : Situación deudora (1-6, donde 1 es mejor)
            - monto : Monto de la deuda
            - diversos indicadores booleanos sobre refinanciaciones,
              procesos judiciales, etc.

        Examples
        --------
        >>> client = BCRAclient()
        >>> result = client.get_debts(identificacion="20123456789")
        """
        pass

    @api_response_handler
    def get_debts_historical(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Obtiene información histórica de deudas registradas por CUIT/CUIL.

        Parameters
        ----------
        identificacion : str
            CUIT/CUIL del titular a consultar (obligatorio)
        json : bool, optional
            Devuelve respuesta JSON sin procesar
        debug : bool, optional
            Devuelve la URL sin hacer la petición

        Returns
        -------
        Union[str, pd.DataFrame, Dict[str, Any]]
            Información histórica de deudas registradas con columnas:

            - identificacion : CUIT/CUIL consultado
            - denominacion : Nombre del titular
            - periodo : Periodo informado (YYYYMM)
            - entidad : Nombre de la entidad financiera
            - situacion : Situación deudora (1-6, donde 1 es mejor)
            - monto : Monto de la deuda
            - enRevision : Si está en revisión
            - procesoJud : Si tiene proceso judicial

        Notes
        -----
        Este endpoint devuelve un historial de deudas a través de múltiples períodos,
        a diferencia del endpoint básico que devuelve información del período actual.

        Examples
        --------
        >>> client = BCRAclient()
        >>> result = client.get_debts_historical(identificacion="20123456789")
        """
        pass

    @api_response_handler
    def get_debts_rejected_checks(self, **kwargs) -> Union[str, pd.DataFrame, Dict[str, Any]]:
        """
        Obtiene información sobre cheques rechazados asociados a un CUIT/CUIL.

        Parameters
        ----------
        identificacion : str
            CUIT/CUIL del titular a consultar (obligatorio)
        json : bool, optional
            Devuelve respuesta JSON sin procesar
        debug : bool, optional
            Devuelve la URL sin hacer la petición

        Returns
        -------
        Union[str, pd.DataFrame, Dict[str, Any]]
            Información de cheques rechazados con columnas:

            - identificacion : CUIT/CUIL consultado
            - denominacion : Nombre del titular
            - causal : Motivo del rechazo (ej: "SIN FONDOS")
            - entidad : Código de la entidad bancaria
            - nroCheque : Número del cheque rechazado
            - fechaRechazo : Fecha de rechazo del cheque
            - monto : Monto del cheque
            - fechaPago : Fecha de pago, si fue pagado
            - fechaPagoMulta : Fecha de pago de la multa
            - estadoMulta : Estado de la multa (ej: "IMPAGA")
            - ctaPersonal : Si es cuenta personal
            - denomJuridica : Denominación jurídica
            - enRevision : Si está en revisión
            - procesoJud : Si tiene proceso judicial

        Notes
        -----
        Este endpoint proporciona información detallada sobre los cheques rechazados
        asociados al CUIT/CUIL consultado, agrupados por causal de rechazo y entidad.

        Examples
        --------
        >>> client = BCRAclient()
        >>> result = client.get_debts_rejected_checks(identificacion="20123456789")
        """
        pass

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
