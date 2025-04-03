from dataclasses import dataclass, field
from typing import Dict, Set, Optional, ClassVar
from enum import Enum, auto
from pathlib import Path

class DataFormat(Enum):
    """Formatos de datos soportados por la API."""
    MONETARY = auto()     # Para get_monetary_data
    MASTER = auto()       # Para get_currency_master
    CURRENCY = auto()     # Para get_currency_quotes
    TIMESERIES = auto()   # Para get_currency_timeseries

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

    MONETARY = f"{MONETARY_BASE}/monetarias"
    CURRENCY_MASTER = f"{CURRENCY_BASE}/Maestros/Divisas"
    CURRENCY_QUOTES = f"{CURRENCY_BASE}/Cotizaciones"

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
            format=DataFormat.MONETARY,
            params={"id_variable", "desde", "hasta", "limit", "offset"}
        ),
        'currency_master': EndpointConfig(
            endpoint=APIEndpoints.CURRENCY_MASTER,
            format=DataFormat.MASTER,
            params=set()
        ),
        'currency_quotes': EndpointConfig(
            endpoint=APIEndpoints.CURRENCY_QUOTES,
            format=DataFormat.CURRENCY,
            params={"fecha"}
        ),
        'currency_timeseries': EndpointConfig(
            endpoint=APIEndpoints.CURRENCY_QUOTES,
            format=DataFormat.TIMESERIES,
            params={"fechadesde", "fechahasta", "limit", "offset"},
            required_args={"moneda"}
        )
    }
