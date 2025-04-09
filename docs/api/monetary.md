# Monetary API

La API monetaria proporciona acceso a datos monetarios y financieros del BCRA.

## Método `variables`

```python
client.monetary.variables(
    debug=False,
    json=False
)
```

Obtiene el listado de variables monetarias disponibles.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame` con las siguientes columnas:

En caso de error del servidor (status_code != 200), se retornará el JSON de respuesta del servidor con el mensaje de error correspondiente.

### Ejemplos

#### Consulta básica: obtener todas las variables disponibles

```python
df = client.monetary.variables()
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.monetary.variables(debug=True)
print(api_url)
```

## Método `series`

```python
client.monetary.series(
    id_variable=None,
    desde=None,
    hasta=None,
    debug=False,
    json=False
)
```

Obtiene la serie histórica de una variable monetaria específica.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `id_variable` | `int` | ID de la variable a consultar | Si |
| `desde` | `str` | Fecha de inicio (YYYY-MM-DD) | No |
| `hasta` | `str` | Fecha final (YYYY-MM-DD) | No |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame`

En caso de error del servidor (status_code != 200), se retornará el JSON de respuesta del servidor con el mensaje de error correspondiente.

### Ejemplos

#### Consulta básica: obtener serie completa

```python
df = client.monetary.series(id_variable=1)
print(df.head())
```

#### Con filtros de fecha

```python
df = client.monetary.series(
    id_variable=1,
    desde="2023-01-01",
    hasta="2023-12-31"
)
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.monetary.series(id_variable=1, debug=True)
print(api_url)
```

### Notas

- La validación de parámetros (tipos, formatos, etc.) es gestionada por el paquete.
- Los errores del servidor (status_code != 200) se manejan devolviendo el JSON de respuesta del servidor.
- Las fechas deben estar en formato YYYY-MM-DD.
- El ID de variable debe ser un número entero válido.

## Ejemplos de Uso

### Obtener variables disponibles
```python
from pyBCRAdata import monetary

# Obtener todas las variables
variables = monetary.variables()
```

### Obtener serie histórica
```python
from pyBCRAdata import monetary

# Obtener serie completa
serie = monetary.series(id_variable=1)

# Obtener serie con rango de fechas
serie = monetary.series(
    id_variable=1,
    desde="2023-01-01",
    hasta="2023-12-31"
)

# Obtener datos en formato JSON
serie_json = monetary.series(id_variable=1, json=True)
```

### Usar con el cliente completo
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
variables = client.monetary.variables()
serie = client.monetary.series(id_variable=1)
```

# Monetary API (English Version)

The Monetary API provides access to monetary and financial data from the BCRA.

## Method `variables`

```python
client.monetary.variables(
    debug=False,
    json=False
)
```

Retrieves the list of available monetary variables.

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|-----------|
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns the data as JSON instead of a DataFrame | No |

### Return

By default, returns a `pandas.DataFrame`.

If a server error occurs (status_code != 200), the returned value will be the server's JSON response with the corresponding error message.

### Examples

#### Basic query: retrieve all available variables

```python
df = client.monetary.variables()
print(df.head())
```

#### Debug mode: get the API URL

```python
api_url = client.monetary.variables(debug=True)
print(api_url)
```

## Method `series`

```python
client.monetary.series(
    id_variable=None,
    desde=None,
    hasta=None,
    debug=False,
    json=False
)
```

Retrieves the historical series for a specific monetary variable.

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|-----------|
| `id_variable` | `int` | ID of the variable to query | Yes |
| `desde` | `str` | Start date (YYYY-MM-DD) | No |
| `hasta` | `str` | End date (YYYY-MM-DD) | No |
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns the data as JSON instead of a DataFrame | No |

### Return

By default, returns a `pandas.DataFrame`.

If a server error occurs (status_code != 200), the returned value will be the server's JSON response with the corresponding error message.

### Examples

#### Basic query: retrieve the complete series

```python
df = client.monetary.series(id_variable=1)
print(df.head())
```

#### With date filters

```python
df = client.monetary.series(
    id_variable=1,
    desde="2023-01-01",
    hasta="2023-12-31"
)
print(df.head())
```

#### Debug mode: get the API URL

```python
api_url = client.monetary.series(id_variable=1, debug=True)
print(api_url)
```

### Notes

- Parameter validation (types, formats, etc.) is handled by the package.
- Server errors (status_code != 200) are handled by returning the server's JSON response.
- Dates must be in YYYY-MM-DD format.
- The variable ID must be a valid integer.

## Usage Examples

### Retrieve available variables

```python
from pyBCRAdata import monetary

# Retrieve all variables
variables = monetary.variables()
```

### Retrieve historical series

```python
from pyBCRAdata import monetary

# Retrieve complete series
serie = monetary.series(id_variable=1)

# Retrieve series with date range
serie = monetary.series(
    id_variable=1,
    desde="2023-01-01",
    hasta="2023-12-31"
)

# Retrieve data in JSON format
serie_json = monetary.series(id_variable=1, json=True)
```

### Using with the complete client

```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
variables = client.monetary.variables()
serie = client.monetary.series(id_variable=1)
```
