from typing import Dict, Any
from urllib.parse import urlencode

class URLBuilder:
    @staticmethod
    def build_url(
        base_url: str,
        endpoint: str,
        params: Dict[str, Any] = None,
    ) -> str:
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # Caso especial para endpoint monetario
        url = url.replace('/monetarias/{id_variable}', '/monetarias') if '/monetarias/{id_variable}' in url and (not params or 'id_variable' not in params) else url

        # Sin parámetros, retornar URL directamente
        if not params:
            return url

        # Reemplazar placeholders y preparar query params
        query_params = {}
        used_placeholders = set()
        for k, v in params.items():
            placeholder = f"{{{k}}}"
            if placeholder in url:
                url = url.replace(placeholder, str(v))
                used_placeholders.add(k)
            else:
                query_params[k] = v

        # Filtrar None values y añadir query params si existen
        query_params = {k: v for k, v in query_params.items() if v is not None}
        return f"{url}?{urlencode(query_params)}" if query_params else url
