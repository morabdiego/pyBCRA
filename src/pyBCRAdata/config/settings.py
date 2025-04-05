from dataclasses import dataclass, field
from typing import Dict, Set, ClassVar
from enum import Enum, auto
from pathlib import Path

class DataFormat(Enum):
    """Formatos de datos soportados por la API."""
    DEFAULT, CURRENCY, TIMESERIES, CHECKS, DEBTS, REJECTED_CHECKS = auto(), auto(), auto(), auto(), auto(), auto()

@dataclass(frozen=True)
class EndpointConfig:
    """Configuración de un endpoint de la API."""
    endpoint: str
    format: DataFormat
    path_params: Set[str] = field(default_factory=set)  # Parámetros que van en la ruta
    query_params: Set[str] = field(default_factory=set)  # Parámetros que van como query string
    required_args: Set[str] = field(default_factory=set)  # Argumentos requeridos (pueden ser path o query)

class APIEndpoints:
    """Endpoints y configuraciones de la API BCRA."""
    # Bases
    BASE = 'api.bcra.gob.ar'
    MONETARY_BASE = 'estadisticas/v3.0'
    CURRENCY_BASE = 'estadisticascambiarias/v1.0'
    CHECKS_BASE = 'cheques/v1.0'
    DEBTS_BASE = 'CentralDeDeudores/v1.0/Deudas'

    # Endpoints específicos
    MONETARY = f"{MONETARY_BASE}/monetarias/{{id_variable}}"
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
    # URLs base y parámetros comunes
    BASE_URL: ClassVar[str] = f'https://{APIEndpoints.BASE}'
    CERT_PATH: ClassVar[str] = str(Path(__file__).parent.parent / 'cert' / 'ca.pem')
    COMMON_FUNC_PARAMS: ClassVar[Set[str]] = {"json", "debug"}

    # Configuración de endpoints
    ENDPOINTS: ClassVar[Dict[str, EndpointConfig]] = {
        'monetary_data': EndpointConfig(
            endpoint=APIEndpoints.MONETARY,
            format=DataFormat.DEFAULT,
            path_params={"id_variable"},
            query_params={"desde", "hasta", "limit", "offset"},
        ),
        'currency_master': EndpointConfig(
            endpoint=APIEndpoints.CURRENCY_MASTER,
            format=DataFormat.DEFAULT
        ),
        'currency_quotes': EndpointConfig(
            endpoint=APIEndpoints.CURRENCY_QUOTES,
            format=DataFormat.CURRENCY,
            query_params={"fecha"}
        ),
        'currency_timeseries': EndpointConfig(
            endpoint=APIEndpoints.CURRENCY_TIMESERIES,
            format=DataFormat.TIMESERIES,
            path_params={"moneda"},
            query_params={"fechadesde", "fechahasta", "limit", "offset"},
            required_args={"moneda"}
        ),
        'checks_master': EndpointConfig(
            endpoint=APIEndpoints.CHECKS_MASTER,
            format=DataFormat.DEFAULT
        ),
        'checks_reported': EndpointConfig(
            endpoint=APIEndpoints.CHECKS_REPORTED,
            format=DataFormat.CHECKS,
            path_params={'codigo_entidad', 'numero_cheque'},
            required_args={'codigo_entidad', 'numero_cheque'}
        ),
        'debts': EndpointConfig(
            endpoint=APIEndpoints.DEBTS,
            format=DataFormat.DEBTS,
            path_params={'identificacion'},
            required_args={'identificacion'}
        ),
        'debts_historical': EndpointConfig(
            endpoint=APIEndpoints.DEBTS_HISTORICAL,
            format=DataFormat.DEBTS,
            path_params={'identificacion'},
            required_args={'identificacion'}
        ),
        'debts_rejected_checks': EndpointConfig(
            endpoint=APIEndpoints.DEBTS_REJECTED_CHECKS,
            format=DataFormat.REJECTED_CHECKS,
            path_params={'identificacion'},
            required_args={'identificacion'}
        )
    }
