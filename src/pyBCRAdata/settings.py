from dataclasses import dataclass, field
from typing import Dict, Set, ClassVar
from pathlib import Path

DATE_FORMAT = "%Y-%m-%d"
ERROR_MESSAGES = {
    'ssl_disabled': "Verificación SSL desactivada - no recomendado para producción",
    'invalid_params': "Parámetros inválidos: {params}",
    'required_args': "Argumentos requeridos: {args}",
    'api_error': "Error en la API: {error}",
    'no_results': "No se encontraron resultados",
    'invalid_date': "Formato de fecha inválido para {field}: {value}. Use YYYY-MM-DD",
    'invalid_int': "Valor entero inválido para {field}: {value}",
    'unknown_format': "Formato de datos desconocido: {format}"
}

COLUMN_TYPES = {
    'fecha': 'datetime64[ns]', 'fechaProcesamiento': 'datetime64[ns]', 'fechaSit1': 'datetime64[ns]',
    'valor': 'float64', 'tipoCotizacion': 'float64', 'tipoPase': 'float64',
    'codigoEntidad': 'int64', 'idVariable': 'int64', 'numeroCheque': 'int64'
}

@dataclass(frozen=True)
class EndpointConfig:
    """Configuración de un endpoint de la API."""
    endpoint: str
    path_params: Set[str] = field(default_factory=set)
    query_params: Set[str] = field(default_factory=set)
    required_args: Set[str] = field(default_factory=set)

class APIEndpoints:
    """Endpoints y configuraciones de la API BCRA."""
    BASE = 'api.bcra.gob.ar'
    MONETARY_BASE = 'estadisticas/v3.0'
    CURRENCY_BASE = 'estadisticascambiarias/v1.0'
    CHECKS_BASE = 'cheques/v1.0'
    DEBTS_BASE = 'CentralDeDeudores/v1.0/Deudas'

    MONETARY = f"{MONETARY_BASE}/monetarias/{{id_variable}}"
    MONETARY_MASTER = f"{MONETARY_BASE}/monetarias"
    CURRENCY_MASTER = f"{CURRENCY_BASE}/Maestros/Divisas"
    CURRENCY_QUOTES = f"{CURRENCY_BASE}/Cotizaciones"
    CURRENCY_TIMESERIES = f"{CURRENCY_BASE}/Cotizaciones/{{moneda}}"
    CHECKS_MASTER = f"{CHECKS_BASE}/entidades"
    CHECKS_REPORTED = f"{CHECKS_BASE}/denunciados/{{codigo_entidad}}/{{numero_cheque}}"
    DEBTS = f"{DEBTS_BASE}/{{identificacion}}"
    DEBTS_HISTORICAL = f"{DEBTS_BASE}/Historicas/{{identificacion}}"
    DEBTS_REJECTED_CHECKS = f"{DEBTS_BASE}/ChequesRechazados/{{identificacion}}"

@dataclass(frozen=True)
class APISettings:
    """Configuración global de la API."""
    BASE_URL: ClassVar[str] = f'https://{APIEndpoints.BASE}'

    CERT_PATH: ClassVar[str] = str(
        Path(__file__).parent / 'cert' / 'ca.pem'
        if (Path(__file__).parent / 'cert' / 'ca.pem').exists()
        else Path(__file__).parent.parent / 'cert' / 'ca.pem'
    )

    COMMON_FUNC_PARAMS: ClassVar[Set[str]] = {"json", "debug"}

    API_CONFIG: ClassVar[Dict[str, Dict[str, EndpointConfig]]] = {
        'monetary': {
            'variables': EndpointConfig(
                endpoint=APIEndpoints.MONETARY_MASTER
            ),
            'series': EndpointConfig(
                endpoint=APIEndpoints.MONETARY,
                path_params={"id_variable"},
                query_params={"desde", "hasta", "limit", "offset"},
                required_args={"id_variable"}
            )
        },
        'currency': {
            'currencies': EndpointConfig(
                endpoint=APIEndpoints.CURRENCY_MASTER
            ),
            'rates': EndpointConfig(
                endpoint=APIEndpoints.CURRENCY_QUOTES,
                query_params={"fecha"}
            ),
            'series': EndpointConfig(
                endpoint=APIEndpoints.CURRENCY_TIMESERIES,
                path_params={"moneda"},
                query_params={"fechadesde", "fechahasta", "limit", "offset"},
                required_args={"moneda"}
            )
        },
        'checks': {
            'banks': EndpointConfig(
                endpoint=APIEndpoints.CHECKS_MASTER
            ),
            'reported': EndpointConfig(
                endpoint=APIEndpoints.CHECKS_REPORTED,
                path_params={'codigo_entidad', 'numero_cheque'},
                required_args={'codigo_entidad', 'numero_cheque'}
            )
        },
        'debtors': {
            'debtors': EndpointConfig(
                endpoint=APIEndpoints.DEBTS,
                path_params={'identificacion'},
                required_args={'identificacion'}
            ),
            'history': EndpointConfig(
                endpoint=APIEndpoints.DEBTS_HISTORICAL,
                path_params={'identificacion'},
                required_args={'identificacion'}
            ),
            'rejected': EndpointConfig(
                endpoint=APIEndpoints.DEBTS_REJECTED_CHECKS,
                path_params={'identificacion'},
                required_args={'identificacion'}
            )
        }
    }
