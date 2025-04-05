# Referencia de API: Datos Monetarios

## Método `get_monetary_data`

```python
client.get_monetary_data(
    id_variable=None,
    desde=None,
    hasta=None,
    offset=None,
    limit=None,
    debug=False,
    json=False
)
```

Obtiene estadísticas monetarias con filtros opcionales.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `id_variable` | `str` | ID de la variable monetaria específica | No |
| `desde` | `str` | Fecha de inicio (YYYY-MM-DD) | No |
| `hasta` | `str` | Fecha final (YYYY-MM-DD) | No |
| `offset` | `int` | Desplazamiento para paginación | No |
| `limit` | `int` | Número máximo de registros | No |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame` con las siguientes columnas:

- `id`: ID de la serie
- `fecha`: Fecha del dato (YYYY-MM-DD)
- `valor`: Valor numérico
- `descripcion`: Descripción del dato monetario

### Ejemplos

#### Consulta básica: obtener todas las variables disponibles

```python
df = client.get_monetary_data()
print(df.head())
```

#### Con filtros y paginación

```python
df = client.get_monetary_data(
    id_variable="6",  # Tasa de Política Monetaria (en % n.a.)
    desde="2024-01-01",
    hasta="2024-03-21",
    limit=100
)
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.get_monetary_data(debug=True)
print(api_url)
```

---

# 🌐 API Reference: Monetary Data

## Method `get_monetary_data`

```python
client.get_monetary_data(
    id_variable=None,
    desde=None,
    hasta=None,
    offset=None,
    limit=None,
    debug=False,
    json=False
)
```

Retrieves monetary statistics with optional filters.

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `id_variable` | `str` | ID of the specific monetary variable | No |
| `desde` | `str` | Start date (YYYY-MM-DD) | No |
| `hasta` | `str` | End date (YYYY-MM-DD) | No |
| `offset` | `int` | Offset for pagination | No |
| `limit` | `int` | Maximum number of records | No |
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns data as JSON instead of DataFrame | No |

### Return

By default, returns a `pandas.DataFrame` with the following columns:

- `id`: ID of the series
- `fecha`: Date of the data point (YYYY-MM-DD)
- `valor`: Numeric value
- `descripcion`: Description of the monetary data

### Examples

#### Basic query: get all available variables

```python
df = client.get_monetary_data()
print(df.head())
```

#### With filters and pagination

```python
df = client.get_monetary_data(
    id_variable="6",  # Monetary Policy Rate (in % n.a.)
    desde="2024-01-01",
    hasta="2024-03-21",
    limit=100
)
print(df.head())
```

#### Debug mode: get the API URL

```python
api_url = client.get_monetary_data(debug=True)
print(api_url)
```
