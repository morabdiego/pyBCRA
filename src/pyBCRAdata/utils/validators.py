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
        # Validar fechas e integers
        for k, v in ((k, v) for k, v in params.items() if k in valid_api_params):
            if k in ParamValidator.DATE_FIELDS and not all(c.isdigit() or c == '-' for c in v) or \
            k in ParamValidator.DATE_FIELDS and len(v.split('-')) != 3:
                raise ValueError(f"Formato de fecha inválido para {k}: {v}")
            elif k in ParamValidator.INT_FIELDS and not str(v).isdigit():
                raise ValueError(f"Valor entero inválido para {k}: {v}")

        # Verificar parámetros inválidos
        if invalid := set(params) - valid_api_params - valid_func_params:
            raise ValueError(f"Parámetros inválidos: {', '.join(invalid)}.\n\nPermitidos API: {', '.join(valid_api_params) or 'Ninguno'}.\nPermitidos función: {', '.join(valid_func_params)}.")

        return {k: v for k, v in params.items() if k in valid_api_params}, {k: v for k, v in params.items() if k in valid_func_params}
