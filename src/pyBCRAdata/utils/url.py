from typing import Dict, Any, Optional
from urllib.parse import urlencode

class URLBuilder:
    """Constructor de URLs para la API."""

    @staticmethod
    def build_url(
        base_url: str,
        endpoint: str,
        params: Dict[str, Any] = None,
        currency: Optional[str] = None
    ) -> str:
        """
        Construye una URL con los parámetros dados.

        Args:
            base_url: URL base de la API
            endpoint: Ruta del endpoint
            params: Parámetros de query
            currency: Código de moneda (opcional)

        Returns:
            URL completa construida
        """
        # Limpiar y combinar base_url y endpoint
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # Agregar código de moneda si existe
        if currency:
            url = f"{url}/{currency}"

        # Agregar parámetros de query si existen
        if params:
            url = f"{url}?{urlencode(params)}"

        return url
