# Currency API

La API de divisas proporciona acceso a cotizaciones y tipos de cambio del BCRA.

## Método `currencies`

```python
client.currency.currencies(
    debug=False,
    json=False
)
```

Obtiene el catálogo maestro de divisas disponibles.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame`.

En caso de error del servidor (status_code != 200), se retornará el JSON de respuesta del servidor con el mensaje de error correspondiente.

### Ejemplos

#### Consulta básica: obtener todas las divisas disponibles

```python
df = client.currency.currencies()
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.currency.currencies(debug=True)
print(api_url)
```

## Método `rates`

```python
client.currency.rates(
    fecha=None,
    debug=False,
    json=False
)
```

Obtiene las cotizaciones de todas las divisas para una fecha específica.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `fecha` | `str` | Fecha en formato YYYY-MM-DD | No |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame`.

En caso de error del servidor (status_code != 200), se retornará el JSON de respuesta del servidor con el mensaje de error correspondiente.

### Ejemplos

#### Consulta básica: obtener cotizaciones del día

```python
df = client.currency.rates(fecha="2024-01-01")
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.currency.rates(fecha="2024-01-01", debug=True)
print(api_url)
```

## Método `series`

```python
client.currency.series(
    moneda=None,
    fechadesde=None,
    fechahasta=None,
    debug=False,
    json=False
)
```

Obtiene la serie histórica de cotizaciones para una divisa específica.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `moneda` | `str` | Código de la divisa (ej: "USD", "EUR") | No |
| `fechadesde` | `str` | Fecha de inicio (YYYY-MM-DD) | No |
| `fechahasta` | `str` | Fecha final (YYYY-MM-DD) | No |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame`.

En caso de error del servidor (status_code != 200), se retornará el JSON de respuesta del servidor con el mensaje de error correspondiente.

### Ejemplos

#### Consulta básica: obtener serie completa

```python
df = client.currency.series(moneda="USD")
print(df.head())
```

#### Con filtros de fecha

```python
df = client.currency.series(
    moneda="USD",
    fechadesde="2023-01-01",
    fechahasta="2023-12-31"
)
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.currency.series(moneda="USD", debug=True)
print(api_url)
```

### Notas

- La validación de parámetros (tipos, formatos, etc.) es gestionada por el paquete.
- Los errores del servidor (status_code != 200) se manejan devolviendo el JSON de respuesta del servidor.
- Las fechas deben estar en formato YYYY-MM-DD.
- El código de moneda debe ser un código válido de divisa.

## Divisas Comunes

Algunas divisas comunes:

| Código | Descripción |
|--------|-------------|
| USD | Dólar Estadounidense |
| EUR | Euro |
| BRL | Real Brasileño |
| GBP | Libra Esterlina |
| JPY | Yen Japonés |
