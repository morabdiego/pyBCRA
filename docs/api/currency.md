# Referencia de API: Datos de Divisas

## Método `get_currency_master`

```python
client.get_currency_master(
    debug=False,
    json=False
)
```

Obtiene el maestro de divisas (catálogo de monedas).

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame` con las siguientes columnas:

- `codigo`: Código ISO de la moneda
- `nombre`: Nombre completo de la divisa

### Ejemplos

#### Consulta básica: obtener todas las monedas disponibles

```python
df = client.get_currency_master()
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.get_currency_master(debug=True)
print(api_url)
```

---

## Método `get_currency_quotes`

```python
client.get_currency_quotes(
    fecha=None,
    debug=False,
    json=False
)
```

Obtiene cotizaciones de divisas para una fecha específica.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `fecha` | `str` | Fecha de cotización (YYYY-MM-DD) | No |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame` con las siguientes columnas:

- `moneda`: Código ISO de la moneda
- `fecha`: Fecha de la cotización (YYYY-MM-DD)
- `valor`: Valor de la cotización en pesos argentinos
- `nombre`: Nombre completo de la divisa

### Ejemplos

#### Consulta de cotizaciones para una fecha específica

```python
df = client.get_currency_quotes(fecha="2023-01-15")
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.get_currency_quotes(fecha="2023-01-15", debug=True)
print(api_url)
```

---

## Método `get_currency_timeseries`

```python
client.get_currency_timeseries(
    moneda=None,
    fechadesde=None,
    fechahasta=None,
    offset=None,
    limit=None,
    debug=False,
    json=False
)
```

Obtiene series temporales de cotizaciones para una divisa específica.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `moneda` | `str` | Código de moneda ISO (ej: "USD") | Sí |
| `fechadesde` | `str` | Fecha de inicio (YYYY-MM-DD) | No |
| `fechahasta` | `str` | Fecha final (YYYY-MM-DD) | No |
| `offset` | `int` | Desplazamiento para paginación | No |
| `limit` | `int` | Número máximo de registros | No |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame` con las siguientes columnas:

- `moneda`: Código ISO de la moneda
- `fecha`: Fecha de la cotización (YYYY-MM-DD)
- `valor`: Valor de la cotización en pesos argentinos
- `nombre`: Nombre completo de la divisa

### Ejemplos

#### Consulta de serie temporal para una divisa

```python
df = client.get_currency_timeseries(
    moneda="USD",
    fechadesde="2023-01-01",
    fechahasta="2023-01-31"
)
print(df.head())
```

#### Con filtros y paginación

```python
df = client.get_currency_timeseries(
    moneda="USD",
    fechadesde="2023-01-01",
    fechahasta="2023-02-01",
    limit=12,
    offset=2
)
print(df.head())
```

---

# 🌐 API Reference: Currency Data

## Method `get_currency_master`

```python
client.get_currency_master(
    debug=False,
    json=False
)
```

Retrieves the currency master catalog.

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns data as JSON instead of DataFrame | No |

### Return

By default, returns a `pandas.DataFrame` with the following columns:

- `codigo`: Currency ISO code
- `nombre`: Full name of the currency

### Examples

#### Basic query: get all available currencies

```python
df = client.get_currency_master()
print(df.head())
```

#### Debug mode: get the API URL

```python
api_url = client.get_currency_master(debug=True)
print(api_url)
```

---

## Method `get_currency_quotes`

```python
client.get_currency_quotes(
    fecha=None,
    debug=False,
    json=False
)
```

Retrieves currency quotes for a specific date.

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `fecha` | `str` | Quote date (YYYY-MM-DD) | No |
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns data as JSON instead of DataFrame | No |

### Return

By default, returns a `pandas.DataFrame` with the following columns:

- `moneda`: Currency ISO code
- `fecha`: Quote date (YYYY-MM-DD)
- `valor`: Quote value in Argentine pesos
- `nombre`: Full name of the currency

### Examples

#### Query quotes for a specific date

```python
df = client.get_currency_quotes(fecha="2023-01-15")
print(df.head())
```

#### Debug mode: get the API URL

```python
api_url = client.get_currency_quotes(fecha="2023-01-15", debug=True)
print(api_url)
```

---

## Method `get_currency_timeseries`

```python
client.get_currency_timeseries(
    moneda=None,
    fechadesde=None,
    fechahasta=None,
    offset=None,
    limit=None,
    debug=False,
    json=False
)
```

Retrieves time series of quotes for a specific currency.

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `moneda` | `str` | Currency ISO code (e.g., "USD") | Yes |
| `fechadesde` | `str` | Start date (YYYY-MM-DD) | No |
| `fechahasta` | `str` | End date (YYYY-MM-DD) | No |
| `offset` | `int` | Offset for pagination | No |
| `limit` | `int` | Maximum number of records | No |
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns data as JSON instead of DataFrame | No |

### Return

By default, returns a `pandas.DataFrame` with the following columns:

- `moneda`: Currency ISO code
- `fecha`: Quote date (YYYY-MM-DD)
- `valor`: Quote value in Argentine pesos
- `nombre`: Full name of the currency

### Examples

#### Query time series for a currency

```python
df = client.get_currency_timeseries(
    moneda="USD",
    fechadesde="2023-01-01",
    fechahasta="2023-01-31"
)
print(df.head())
```

#### With filters and pagination

```python
df = client.get_currency_timeseries(
    moneda="USD",
    fechadesde="2023-01-01",
    fechahasta="2023-02-01",
    limit=12,
    offset=2
)
print(df.head())
```
