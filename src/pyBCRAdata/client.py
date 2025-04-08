from typing import Dict, Any, Union, Optional
import pandas as pd
import warnings
import requests

from .settings import APISettings, ERROR_MESSAGES
from .connector import APIConnector
from .api_call import api_call

# Tipo para resultados de API
APIResult = Union[str, pd.DataFrame, Dict[str, Any]]

# Parámetros comunes en todos los métodos
COMMON_PARAMS_DOC = """
        json : bool, optional
            Devuelve respuesta JSON sin procesar
        debug : bool, optional
            Devuelve la URL sin hacer la petición
"""

class BCRAclient:
    """Cliente para acceder a los datos de la API del BCRA."""

    def __init__(
        self,
        base_url: str = APISettings.BASE_URL,
        cert_path: Optional[str] = None,
        verify_ssl: bool = True
    ):
        """Inicializa el cliente BCRA con opciones de conexión."""
        if not verify_ssl:
            warnings.warn(ERROR_MESSAGES['ssl_disabled'], UserWarning)
            requests.packages.urllib3.disable_warnings()

        # Crear conector de API
        final_cert_path = cert_path or (APISettings.CERT_PATH if verify_ssl else False)
        self.api_connector = APIConnector(base_url=base_url, cert_path=final_cert_path)

    @api_call
    def get_monetary_data(self, **kwargs) -> APIResult:
        """
        Obtiene datos monetarios del BCRA.

        Parameters
        ----------
        id_variable : int
            ID de la variable monetaria (parámetro de ruta)
        desde : str, optional
            Fecha inicio (YYYY-MM-DD) (parámetro de consulta)
        hasta : str, optional
            Fecha fin (YYYY-MM-DD) (parámetro de consulta)
        limit, offset : int, optional
            Paginación de resultados (parámetros de consulta)
        """ + COMMON_PARAMS_DOC + """
        Returns
        -------
        DataFrame con serie temporal de datos monetarios

        Examples
        --------
        >>> df = client.get_monetary_data(id_variable=1, desde="2020-01-01", hasta="2020-12-31")
        """
        pass

    @api_call
    def get_currency_master(self, **kwargs) -> APIResult:
        """
        Obtiene el maestro de divisas (catálogo de monedas).
        """ + COMMON_PARAMS_DOC + """
        Returns
        -------
        DataFrame con listado de divisas y sus códigos ISO

        Examples
        --------
        >>> df = client.get_currency_master()
        """
        pass

    @api_call
    def get_currency_quotes(self, **kwargs) -> APIResult:
        """
        Obtiene cotizaciones de divisas para una fecha específica.

        Parameters
        ----------
        fecha : str, optional
            Fecha de cotización (YYYY-MM-DD) (parámetro de consulta)
        """ + COMMON_PARAMS_DOC + """
        Returns
        -------
        DataFrame con cotizaciones de todas las divisas para la fecha

        Examples
        --------
        >>> df = client.get_currency_quotes(fecha="2023-01-15")
        """
        pass

    @api_call
    def get_currency_timeseries(self, **kwargs) -> APIResult:
        """
        Obtiene series temporales de cotizaciones para una divisa específica.

        Parameters
        ----------
        moneda : str
            Código de moneda ISO (ej: "USD") (parámetro de ruta, obligatorio)
        fechadesde, fechahasta : str, optional
            Rango de fechas (YYYY-MM-DD) (parámetros de consulta)
        limit, offset : int, optional
            Paginación de resultados (parámetros de consulta)
        """ + COMMON_PARAMS_DOC + """
        Returns
        -------
        DataFrame con serie temporal de cotizaciones para la divisa

        Examples
        --------
        >>> df = client.get_currency_timeseries(moneda="USD", fechadesde="2023-01-01", fechahasta="2023-12-31")
        """
        pass

    @api_call
    def get_checks_master(self, **kwargs) -> APIResult:
        """
        Obtiene el listado de entidades bancarias que operan con cheques.
        """ + COMMON_PARAMS_DOC + """
        Returns
        -------
        DataFrame con códigos y nombres de entidades bancarias

        Examples
        --------
        >>> df = client.get_checks_master()
        """
        pass

    @api_call
    def get_checks_reported(self, **kwargs) -> APIResult:
        """
        Obtiene información de cheques denunciados.

        Parameters
        ----------
        codigo_entidad : int
            Código de la entidad bancaria (parámetro de ruta, obligatorio)
        numero_cheque : int
            Número del cheque a consultar (parámetro de ruta, obligatorio)
        """ + COMMON_PARAMS_DOC + """
        Returns
        -------
        DataFrame con información del cheque denunciado

        Examples
        --------
        >>> df = client.get_checks_reported(codigo_entidad=123, numero_cheque=456789)
        """
        pass

    @api_call
    def get_debts(self, **kwargs) -> APIResult:
        """
        Obtiene información de deudas registradas por CUIT/CUIL.

        Parameters
        ----------
        identificacion : str
            CUIT/CUIL del titular a consultar (parámetro de ruta, obligatorio)
        """ + COMMON_PARAMS_DOC + """
        Returns
        -------
        DataFrame con información de deudas registradas

        Examples
        --------
        >>> df = client.get_debts(identificacion="20123456789")
        """
        pass

    @api_call
    def get_debts_historical(self, **kwargs) -> APIResult:
        """
        Obtiene información histórica de deudas registradas por CUIT/CUIL.

        Parameters
        ----------
        identificacion : str
            CUIT/CUIL del titular a consultar (parámetro de ruta, obligatorio)
        """ + COMMON_PARAMS_DOC + """
        Returns
        -------
        DataFrame con histórico de deudas a través de múltiples períodos

        Examples
        --------
        >>> df = client.get_debts_historical(identificacion="20123456789")
        """
        pass

    @api_call
    def get_debts_rejected_checks(self, **kwargs) -> APIResult:
        """
        Obtiene información sobre cheques rechazados asociados a un CUIT/CUIL.

        Parameters
        ----------
        identificacion : str
            CUIT/CUIL del titular a consultar (parámetro de ruta, obligatorio)
        """ + COMMON_PARAMS_DOC + """
        Returns
        -------
        DataFrame con información detallada de cheques rechazados

        Examples
        --------
        >>> df = client.get_debts_rejected_checks(identificacion="20123456789")
        """
        pass
