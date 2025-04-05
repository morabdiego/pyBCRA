from typing import Dict, Any, Set
from urllib.parse import urlencode

class URLBuilder:
    @staticmethod
    def build_url(
        base_url: str,
        endpoint: str,
        params: Dict[str, Any] = None,
        path_params: Set[str] = None,
        query_params: Set[str] = None,
    ) -> str:
        # Normalizar URL base
        url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # Caso especial para endpoint monetario
        if '/monetarias/{id_variable}' in url and (not params or 'id_variable' not in params):
            url = url.replace('/monetarias/{id_variable}', '/monetarias')

        # Sin parámetros, retornar URL directamente
        if not params:
            return url

        # Procesar parámetros de ruta (path)
        if path_params:
            for key in path_params:
                if key in params:
                    placeholder = f"{{{key}}}"
                    if placeholder in url:
                        url = url.replace(placeholder, str(params[key]))

        # Procesar parámetros de consulta (query)
        query_dict = {}

        # Determinar los parámetros de consulta
        effective_query_params = query_params if query_params is not None else (
            set(params.keys()) - (path_params or set())
        )

        # Añadir solo parámetros relevantes a query_dict
        for key in effective_query_params:
            if key in params and params[key] is not None:
                placeholder = f"{{{key}}}"
                if placeholder not in url:
                    query_dict[key] = params[key]

        # Añadir query params si existen
        return f"{url}?{urlencode(query_dict)}" if query_dict else url
