from typing import Any, Dict, Set, Tuple

class ParamValidator:
    @staticmethod
    def validate_params(
        params: Dict[str, Any],
        valid_api_params: Set[str],
        valid_func_params: Set[str] = {"json", "debug"}
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        # Verificar parámetros inválidos
        if invalid := set(params) - valid_api_params - valid_func_params:
            raise ValueError(f"Parámetros inválidos: {', '.join(invalid)}.\n\nPermitidos API: {', '.join(valid_api_params) or 'Ninguno'}.\nPermitidos función: {', '.join(valid_func_params)}.")

        # Separar parámetros API y de función
        api_params = {k: v for k, v in params.items() if k in valid_api_params}
        func_params = {k: v for k, v in params.items() if k in valid_func_params}

        return api_params, func_params
