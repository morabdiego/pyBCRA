from typing import Dict

# Formatos de fecha
DATE_FORMAT = "%Y-%m-%d"

# Mensajes de error
ERROR_MESSAGES = {
    'ssl_disabled': "Verificación SSL desactivada - no recomendado para producción",
    'invalid_params': "Parámetros inválidos: {params}",
    'required_args': "Argumentos requeridos: {args}",
    'api_error': "Error en la API: {error}",
    'no_results': "No se encontraron resultados",
    'invalid_date': "Formato de fecha inválido para {field}: {value}. Use YYYY-MM-DD",
    'invalid_int': "Valor entero inválido para {field}: {value}",
    'unknown_format': "Formato de datos desconocido: {format}"
}

# Tipos de columnas agrupados por tipo de dato
COLUMN_TYPES = {
    # Fechas
    'fecha': 'datetime64[ns]', 'fechaProcesamiento': 'datetime64[ns]', 'fechaSit1': 'datetime64[ns]',

    # Valores numéricos de punto flotante
    'valor': 'float64', 'tipoCotizacion': 'float64', 'tipoPase': 'float64',

    # Valores enteros
    'codigoEntidad': 'int64', 'idVariable': 'int64', 'numeroCheque': 'int64'
}
