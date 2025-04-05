from datetime import datetime
from typing import Any, Dict, Set, Tuple

class ParamValidator:
    # Conjuntos de campos que requieren validación específica
    DATE_FIELDS = {'fecha', 'desde', 'hasta', 'fechadesde', 'fechahasta'}
    INT_FIELDS = {'limit', 'offset'}

    @staticmethod
    def validate_params(
        params: Dict[str, Any],
        valid_api_params: Set[str],
        valid_func_params: Set[str] = {"json", "debug"}
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Valida los parámetros de entrada y los separa en parámetros de API y de función.
        Lanza ValueError si encuentra parámetros inválidos o valores incorrectos.
        """
        api_params = {}

        # Procesar parámetros de API
        for k, v in params.items():
            if k in valid_api_params:
                # Validar según el tipo de campo
                if k in ParamValidator.DATE_FIELDS and not ParamValidator.validate_date(v):
                    raise ValueError(f"Formato de fecha inválido para {k}: {v}")
                elif k in ParamValidator.INT_FIELDS and not ParamValidator.validate_int(v):
                    raise ValueError(f"Valor entero inválido para {k}: {v}")

                api_params[k] = v

        # Extraer parámetros de función
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

    @staticmethod
    def validate_date(value: str) -> bool:
        """Valida que el valor sea una fecha en formato YYYY-MM-DD."""
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_int(value: Any) -> bool:
        """Valida que el valor pueda convertirse a entero."""
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False
