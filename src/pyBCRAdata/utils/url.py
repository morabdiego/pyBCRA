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
            currency: Código de moneda para endpoints de divisas

        Returns:
            URL completa construida
        """
        # Limpiar y combinar base_url y endpoint
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # Agregar moneda al path si existe
        if currency:
            url = f"{url}/{currency}"

        # Agregar parámetros de query si existen (excluyendo moneda)
        if params:
            query_params = {k: v for k, v in params.items() if k != 'moneda'}
            if query_params:
                url = f"{url}?{urlencode(query_params)}"

        return url
