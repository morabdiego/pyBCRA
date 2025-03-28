from dataclasses import dataclass

@dataclass(frozen=True)
class APIConfig:
    """
    Centralized configuration for API-related constants.
    Provides type safety and immutability for configuration parameters.
    """

    # Base URL configurations
    BASE_URL: str = 'https://api.bcra.gob.ar'

    # Monetary API configurations
    MONETARY_ENDPOINT: str = '/estadisticas/v3.0/monetarias'

    # Currency API configurations
    CURRENCY_BASE_ENDPOINT: str = '/estadisticascambiarias/v1.0'

    # Certificate path
    CERT_PATH: str = 'src/pyBCRAdata/cert/ca.pem'

    # Derived currency-related endpoints
    CURRENCY_MASTER_URL: str = f'{CURRENCY_BASE_ENDPOINT}/Maestros/Divisas'
    CURRENCY_QUOTES_URL: str = f'{CURRENCY_BASE_ENDPOINT}/Cotizaciones'
