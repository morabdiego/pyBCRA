from dataclasses import dataclass, field
from typing import Dict, Set, Optional, ClassVar
from enum import Enum, auto
from pathlib import Path

class DataFormat(Enum):
    """Formatos de datos soportados por la API."""
    DEFAULT = auto()     # Para get_monetary_data
    CURRENCY = auto()     # Para get_currency_quotes
    TIMESERIES = auto()   # Para get_currency_timeseries
    CHECKS = auto()      # Para get_checks_reported
    DEBTS = auto()       # Para get_debts

@dataclass(frozen=True)
class EndpointConfig:
    """Configuración de un endpoint de la API."""
    endpoint: str
    format: DataFormat
    params: Set[str] = field(default_factory=set)
    required_args: Set[str] = field(default_factory=set)

class APIEndpoints:
    """Endpoints base de la API."""
    BASE = 'api.bcra.gob.ar'
    MONETARY_BASE = 'estadisticas/v3.0'
    CURRENCY_BASE = 'estadisticascambiarias/v1.0'
    CHECKS_BASE = 'cheques/v1.0'

    MONETARY = f"{MONETARY_BASE}/monetarias"
    CURRENCY_MASTER = f"{CURRENCY_BASE}/Maestros/Divisas"
    CURRENCY_QUOTES = f"{CURRENCY_BASE}/Cotizaciones"
    CURRENCY_TIMESERIES = f"{CURRENCY_BASE}/Cotizaciones/{{moneda}}"
    CHECKS_MASTER = f"{CHECKS_BASE}/entidades"
    CHECKS_REPORTED = "cheques/v1.0/denunciados/{codigo_entidad}/{numero_cheque}"
    DEBTS = 'CentralDeDeudores/v1.0/Deudas/{identificacion}'

@dataclass(frozen=True)
class APISettings:
    """Configuración global de la API."""

    # URLs base
    BASE_URL: ClassVar[str] = f'https://{APIEndpoints.BASE}'
    CERT_PATH: ClassVar[str] = str(Path(__file__).parent.parent / 'cert' / 'ca.pem')

    # Parámetros comunes como variable de clase
    COMMON_FUNC_PARAMS: ClassVar[Set[str]] = {"json", "debug"}

    # Configuración de endpoints como variable de clase
    ENDPOINTS: ClassVar[Dict[str, EndpointConfig]] = {
        'monetary_data': EndpointConfig(
            endpoint=APIEndpoints.MONETARY,
            format=DataFormat.DEFAULT,
            params={"id_variable", "desde", "hasta", "limit", "offset"}
        ),
        'currency_master': EndpointConfig(
            endpoint=APIEndpoints.CURRENCY_MASTER,
            format=DataFormat.DEFAULT,
            params=set()
        ),
        'currency_quotes': EndpointConfig(
            endpoint=APIEndpoints.CURRENCY_QUOTES,
            format=DataFormat.CURRENCY,
            params={"fecha"}
        ),
        'currency_timeseries': EndpointConfig(
            endpoint=APIEndpoints.CURRENCY_TIMESERIES,
            format=DataFormat.TIMESERIES,
            params={"fechadesde", "fechahasta", "limit", "offset"},
            required_args={"moneda"}
        ),
        'checks_master': EndpointConfig(
            endpoint=APIEndpoints.CHECKS_MASTER,
            format=DataFormat.DEFAULT,
            params=set()
        ),
        'checks_reported': EndpointConfig(
            endpoint=APIEndpoints.CHECKS_REPORTED,
            format=DataFormat.CHECKS,
            params=set(),
            required_args={'codigo_entidad', 'numero_cheque'}
        ),
        'debts': EndpointConfig(
            endpoint=APIEndpoints.DEBTS,
            format=DataFormat.DEFAULT,
            params=set(),
            required_args={'identificacion'}
        )
    }
