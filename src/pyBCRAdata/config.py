from dataclasses import dataclass
from importlib.resources import files

@dataclass(frozen=True)
class APIConfig:
    BASE_URL: str = 'https://api.bcra.gob.ar'
    CERT_PATH: str = str(files('pyBCRAdata').joinpath('cert/ca.pem'))
    MONETARY_ENDPOINT: str = 'estadisticas/v3.0/monetarias'
    CURRENCY_BASE_ENDPOINT: str = 'estadisticascambiarias/v1.0'
    CURRENCY_MASTER_URL: str = f"{CURRENCY_BASE_ENDPOINT}/Maestros/Divisas"
    CURRENCY_QUOTES_URL: str = f"{CURRENCY_BASE_ENDPOINT}/Cotizaciones"
