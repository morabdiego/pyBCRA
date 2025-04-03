from datetime import datetime
from typing import Any, Dict, Set, Tuple

class ParamValidator:
    """Validador de parámetros de la API."""

    @staticmethod
    def validate_date(value: str) -> bool:
        """
        Valida formato de fecha YYYY-MM-DD.

        Args:
            value: Fecha a validar
        """
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_int(value: Any) -> bool:
        """
        Valida si un valor puede convertirse a entero.

        Args:
            value: Valor a validar
        """
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_params(
        params: Dict[str, Any],
        valid_api_params: Set[str],
        valid_func_params: Set[str] = {"json", "debug"}
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Valida y separa parámetros de API y función."""
        api_params = {}
        for k, v in params.items():
            if k in valid_api_params:
                # Validar fechas
                if k in {'fecha', 'desde', 'hasta', 'fechadesde', 'fechahasta'}:
                    if not ParamValidator.validate_date(v):
                        raise ValueError(f"Formato de fecha inválido para {k}: {v}. Use YYYY-MM-DD")
                # Validar enteros
                elif k in {'limit', 'offset'}:
                    if not ParamValidator.validate_int(v):
                        raise ValueError(f"Valor entero inválido para {k}: {v}")
                api_params[k] = v

        func_params = {k: v for k, v in params.items() if k in valid_func_params}

        # Verificar parámetros inválidos
        invalid_params = set(params.keys()) - valid_api_params - valid_func_params
        if invalid_params:
            raise ValueError(
                f"Parámetros inválidos: {', '.join(invalid_params)}.\n\n"
                f"Parámetros API permitidos: {', '.join(valid_api_params) or 'Ninguno'}.\n"
                f"Parámetros función permitidos: {', '.join(valid_func_params)}."
            )

        return api_params, func_params
