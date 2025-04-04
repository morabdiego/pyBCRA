from datetime import datetime
from typing import Any, Dict, Set, Tuple

class ParamValidator:
    @staticmethod
    def validate_params(
        params: Dict[str, Any],  # Diccionario de parámetros a validar
        valid_api_params: Set[str],  # Conjunto de parámetros válidos de API
        valid_func_params: Set[str] = {"json", "debug"}  # Parámetros de función por defecto
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:

        api_params = {}  # Diccionario para almacenar parámetros de API válidos

        # Itera sobre los parámetros recibidos
        for k, v in params.items():
            if k in valid_api_params:
                # Valida fechas para campos específicos
                if k in {'fecha', 'desde', 'hasta', 'fechadesde', 'fechahasta'}:
                    if not ParamValidator.validate_date(v):
                        raise ValueError(f"Formato de fecha inválido para {k}: {v}")

                # Valida enteros para campos específicos
                elif k in {'limit', 'offset'}:
                    if not ParamValidator.validate_int(v):
                        raise ValueError(f"Valor entero inválido para {k}: {v}")

                api_params[k] = v  # Almacena el parámetro válido

        # Filtra y almacena los parámetros de función válidos
        func_params = {k: v for k, v in params.items() if k in valid_func_params}

        # Verifica si hay parámetros inválidos
        invalid_params = set(params.keys()) - valid_api_params - valid_func_params
        if invalid_params:
            raise ValueError(  # Lanza error con mensaje detallado
                f"Parámetros inválidos: {', '.join(invalid_params)}.\n\n"
                f"Parámetros API permitidos: {', '.join(valid_api_params) or 'Ninguno'}.\n"
                f"Parámetros función permitidos: {', '.join(valid_func_params)}."
            )

        return api_params, func_params  # Retorna tupla con parámetros validados

    @staticmethod  # Decorator para método estático (no requiere instancia)
    def validate_date(value: str) -> bool:
        try:
            datetime.strptime(value, "%Y-%m-%d")  # Intenta parsear la fecha en formato YYYY-MM-DD
            return True  # Retorna True si el formato es válido
        except ValueError:
            return False  # Retorna False si hay error en el formato

    @staticmethod
    def validate_int(value: Any) -> bool:
        try:
            int(value)  # Intenta convertir el valor a entero
            return True  # Retorna True si la conversión es exitosa
        except (ValueError, TypeError):
            return False  # Retorna False si hay error en la conversión
