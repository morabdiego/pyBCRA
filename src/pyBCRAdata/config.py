from dataclasses import dataclass
from importlib.resources import files

@dataclass(frozen=True)
class APIConfig:
    BASE_URL: str = 'https://api.bcra.gob.ar'
    CERT_PATH: str = str(files('pyBCRAdata').joinpath('cert/ca.pem'))
    MONETARY_ENDPOINT: str = '/estadisticas/v3.0/monetarias'
    CURRENCY_BASE_ENDPOINT: str = '/estadisticascambiarias/v1.0'

    @property
    def CURRENCY_MASTER_URL(self) -> str:
        return f"{self.CURRENCY_BASE_ENDPOINT}/Maestros/Divisas"

    @property
    def CURRENCY_QUOTES_URL(self) -> str:
        return f"{self.CURRENCY_BASE_ENDPOINT}/Cotizaciones"
