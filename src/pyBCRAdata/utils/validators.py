from datetime import datetime
from typing import Any, Dict, Set, Tuple

class ParamValidator:
    # Conjuntos de campos que requieren validación específica
    DATE_FIELDS = {'fecha', 'desde', 'hasta', 'fechadesde', 'fechahasta'}
    INT_FIELDS = {'limit', 'offset', 'codigo_entidad', 'numero_cheque'}

    @staticmethod
    def is_valid_date_format(value: str) -> bool:
        """Valida que un string tenga formato de fecha válido."""
        return all(c.isdigit() or c == '-' for c in value) and len(value.split('-')) == 3

    @staticmethod
    def is_valid_int(value: Any) -> bool:
        """Valida que un valor pueda ser convertido a entero."""
        return str(value).isdigit()

    @staticmethod
    def validate_params(
        params: Dict[str, Any],
        valid_api_params: Set[str],
        valid_func_params: Set[str] = {"json", "debug"}
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        # Validar fechas e integers
        for k, v in ((k, v) for k, v in params.items() if k in valid_api_params):
            if k in ParamValidator.DATE_FIELDS and not ParamValidator.is_valid_date_format(v):
                raise ValueError(f"Formato de fecha inválido para {k}: {v}")
            elif k in ParamValidator.INT_FIELDS and not ParamValidator.is_valid_int(v):
                raise ValueError(f"Valor entero inválido para {k}: {v}")

        # Verificar parámetros inválidos
        if invalid := set(params) - valid_api_params - valid_func_params:
            raise ValueError(f"Parámetros inválidos: {', '.join(invalid)}.\n\nPermitidos API: {', '.join(valid_api_params) or 'Ninguno'}.\nPermitidos función: {', '.join(valid_func_params)}.")

        # Separar parámetros API y de función
        api_params = {k: v for k, v in params.items() if k in valid_api_params}
        func_params = {k: v for k, v in params.items() if k in valid_func_params}

        return api_params, func_params
