# Checks API

La API de cheques proporciona acceso a información sobre cheques y entidades bancarias.

## Método `banks`

```python
from pyBCRAdata import BCRAclient

client = BCRAclient()

client.checks.banks(
    debug=False,
    json=False
)
```

Obtiene el listado de entidades bancarias.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame`.

En caso de error del servidor (status_code != 200), se retornará el JSON de respuesta del servidor con el mensaje de error correspondiente.

### Ejemplos

#### Consulta básica: obtener todas las entidades bancarias

```python
df = client.checks.banks()
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.checks.banks(debug=True)
print(api_url)
```

## Método `reported`

```python
client.checks.reported(
    codigo_entidad=None,
    numero_cheque=None,
    debug=False,
    json=False
)
```

Obtiene información sobre un cheque denunciado.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `codigo_entidad` | `int` | Código de la entidad bancaria | Si |
| `numero_cheque` | `int` | Número de cheque | Si |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame`.

En caso de error del servidor (status_code != 200), se retornará el JSON de respuesta del servidor con el mensaje de error correspondiente.

### Ejemplos

#### Consulta básica: obtener información de un cheque

```python
df = client.checks.reported(
    codigo_entidad=123,
    numero_cheque=456789
)
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.checks.reported(
    codigo_entidad=123,
    numero_cheque=456789,
    debug=True
)
print(api_url)
```

### Notas

- La validación de parámetros (tipos, formatos, etc.) es gestionada por el paquete.
- Los errores del servidor (status_code != 200) se manejan devolviendo el JSON de respuesta del servidor.
- El código de entidad debe ser un número entero válido.
- El número de cheque debe ser un número entero válido.

## Ejemplos de Uso

### Obtener entidades bancarias
```python
from pyBCRAdata import checks

# Obtener todas las entidades
bancos = checks.banks()
```

### Consultar cheques denunciados
```python
from pyBCRAdata import checks

# Consultar cheque específico
cheque = checks.reported(
    codigo_entidad=123,
    numero_cheque=456789
)

# Obtener datos en formato JSON
cheque_json = checks.reported(
    codigo_entidad=123,
    numero_cheque=456789,
    json=True
)
```

### Usar con el cliente completo
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
bancos = client.checks.banks()
cheque = client.checks.reported(
    codigo_entidad=123,
    numero_cheque=456789
)
```
# Checks API (English Version)

The Checks API provides access to information about checks and banking entities.

## Method `banks`

```python
from pyBCRAdata import BCRAclient

client = BCRAclient()

client.checks.banks(
    debug=False,
    json=False
)
```

Retrieves the list of banking entities.

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|-----------|
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns the data as JSON instead of a DataFrame | No |

### Return

By default, returns a `pandas.DataFrame`.

If a server error occurs (status_code != 200), the returned value will be the server's JSON response with the corresponding error message.

### Examples

#### Basic query: retrieve all banking entities

```python
df = client.checks.banks()
print(df.head())
```

#### Debug mode: get the API URL

```python
api_url = client.checks.banks(debug=True)
print(api_url)
```

## Method `reported`

```python
client.checks.reported(
    codigo_entidad=None,
    numero_cheque=None,
    debug=False,
    json=False
)
```

Retrieves information about a reported check.

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|-----------|
| `codigo_entidad` | `int` | Banking entity code | Yes |
| `numero_cheque` | `int` | Check number | Yes |
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns the data as JSON instead of a DataFrame | No |

### Return

By default, returns a `pandas.DataFrame`.

If a server error occurs (status_code != 200), the returned value will be the server's JSON response with the corresponding error message.

### Examples

#### Basic query: retrieve check information

```python
df = client.checks.reported(
    codigo_entidad=123,
    numero_cheque=456789
)
print(df.head())
```

#### Debug mode: get the API URL

```python
api_url = client.checks.reported(
    codigo_entidad=123,
    numero_cheque=456789,
    debug=True
)
print(api_url)
```

### Notes

- Parameter validation (types, formats, etc.) is handled by the package.
- Server errors (status_code != 200) are handled by returning the server's JSON response.
- `codigo_entidad` must be a valid integer.
- `numero_cheque` must be a valid integer.

## Usage Examples

### Retrieve banking entities

```python
from pyBCRAdata import checks

# Get all entities
bancos = checks.banks()
```

### Query reported checks

```python
from pyBCRAdata import checks

# Query a specific check
cheque = checks.reported(
    codigo_entidad=123,
    numero_cheque=456789
)

# Retrieve data in JSON format
cheque_json = checks.reported(
    codigo_entidad=123,
    numero_cheque=456789,
    json=True
)
```

### Using with the complete client

```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
bancos = client.checks.banks()
cheque = client.checks.reported(
    codigo_entidad=123,
    numero_cheque=456789
)
```
