from typing import Dict, Any
from urllib.parse import urlencode

class URLBuilder:
    @staticmethod
    def build_url(
        base_url: str,
        endpoint: str,
        params: Dict[str, Any] = None,
    ) -> str:
        # Combinar base_url y endpoint
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # Caso especial para endpoint monetario
        if '/monetarias/{id_variable}' in url and (params is None or 'id_variable' not in params):
            url = url.replace('/monetarias/{id_variable}', '/monetarias')

        # Manejar los parámetros
        if params:
            # Reemplazar placeholders en la URL
            path_params = {k: v for k, v in params.items() if f"{{{k}}}" in url}
            for key, value in path_params.items():
                url = url.replace(f"{{{key}}}", str(value))

            # Preparar query params (excluyendo los ya usados en path)
            query_params = {k: v for k, v in params.items() if k not in path_params}

            # Añadir query params si existen
            if query_params:
                url = f"{url}?{urlencode(query_params)}"

        return url
