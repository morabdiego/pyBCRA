from typing import Dict, Any
from urllib.parse import urlencode

class URLBuilder:
    @staticmethod
    def build_url(
        base_url: str,
        endpoint: str,
        params: Dict[str, Any] = None,
    ) -> str:
        # Limpiar y combinar base_url y endpoint
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # Si el endpoint contiene placeholders, reemplazarlos con los valores
        if "{" in url and "}" in url and params:
            # Extraer los parámetros que son para la URL
            path_params = {k: v for k, v in params.items() if f"{{{k}}}" in url}
            # Reemplazar los placeholders
            for key, value in path_params.items():
                url = url.replace(f"{{{key}}}", str(value))
            # Remover los parámetros usados del diccionario original
            if params:
                params = {k: v for k, v in params.items() if k not in path_params}

        # Agregar parámetros restantes como query params si existen
        if params:
            query_params = {k: v for k, v in params.items() if k != 'moneda'}
            if query_params:
                url = f"{url}?{urlencode(query_params)}"

        return url
