# Referencia de API: Datos de Central de Deudores

## Método `get_debts`

```python
client.get_debts(
    identificacion=None,
    debug=False,
    json=False
)
```

Obtiene información de deudas registradas por CUIT/CUIL.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `identificacion` | `str` | CUIT/CUIL del titular a consultar | Sí |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame` con información sobre las deudas registradas del titular.

### Ejemplos

#### Consulta de deudas para un CUIT/CUIL específico

```python
df = client.get_debts(identificacion="23409233449")
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.get_debts(identificacion="23409233449", debug=True)
print(api_url)
```

---

## Método `get_debts_historical`

```python
client.get_debts_historical(
    identificacion=None,
    debug=False,
    json=False
)
```

Obtiene información histórica de deudas registradas por CUIT/CUIL.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `identificacion` | `str` | CUIT/CUIL del titular a consultar | Sí |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame` con el histórico de deudas a través de múltiples períodos.

### Ejemplos

#### Consulta del historial de deudas para un CUIT/CUIL específico

```python
df = client.get_debts_historical(identificacion="23409233449")
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.get_debts_historical(identificacion="23409233449", debug=True)
print(api_url)
```

---

## Método `get_debts_rejected_checks`

```python
client.get_debts_rejected_checks(
    identificacion=None,
    debug=False,
    json=False
)
```

Obtiene información sobre cheques rechazados asociados a un CUIT/CUIL.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `identificacion` | `str` | CUIT/CUIL del titular a consultar | Sí |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame` con información detallada de cheques rechazados.

### Ejemplos

#### Consulta de cheques rechazados para un CUIT/CUIL específico

```python
df = client.get_debts_rejected_checks(identificacion="23409233449")
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.get_debts_rejected_checks(identificacion="23409233449", debug=True)
print(api_url)
```

---

# 🌐 API Reference: Debt Data

## Method `get_debts`

```python
client.get_debts(
    identificacion=None,
    debug=False,
    json=False
)
```

Retrieves debt information registered by tax ID (CUIT/CUIL).

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `identificacion` | `str` | Tax ID (CUIT/CUIL) to query | Yes |
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns data as JSON instead of DataFrame | No |

### Return

By default, returns a `pandas.DataFrame` with information about registered debts for the tax ID.

### Examples

#### Query debts for a specific tax ID

```python
df = client.get_debts(identificacion="23409233449")
print(df.head())
```

#### Debug mode: get the API URL

```python
api_url = client.get_debts(identificacion="23409233449", debug=True)
print(api_url)
```

---

## Method `get_debts_historical`

```python
client.get_debts_historical(
    identificacion=None,
    debug=False,
    json=False
)
```

Retrieves historical debt information registered by tax ID (CUIT/CUIL).

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `identificacion` | `str` | Tax ID (CUIT/CUIL) to query | Yes |
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns data as JSON instead of DataFrame | No |

### Return

By default, returns a `pandas.DataFrame` with historical debt information across multiple periods.

### Examples

#### Query debt history for a specific tax ID

```python
df = client.get_debts_historical(identificacion="23409233449")
print(df.head())
```

#### Debug mode: get the API URL

```python
api_url = client.get_debts_historical(identificacion="23409233449", debug=True)
print(api_url)
```

---

## Method `get_debts_rejected_checks`

```python
client.get_debts_rejected_checks(
    identificacion=None,
    debug=False,
    json=False
)
```

Retrieves information about rejected checks associated with a tax ID (CUIT/CUIL).

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `identificacion` | `str` | Tax ID (CUIT/CUIL) to query | Yes |
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns data as JSON instead of DataFrame | No |

### Return

By default, returns a `pandas.DataFrame` with detailed information about rejected checks.

### Examples

#### Query rejected checks for a specific tax ID

```python
df = client.get_debts_rejected_checks(identificacion="23409233449")
print(df.head())
```

#### Debug mode: get the API URL

```python
api_url = client.get_debts_rejected_checks(identificacion="23409233449", debug=True)
print(api_url)
```
