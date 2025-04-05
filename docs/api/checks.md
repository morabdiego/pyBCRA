# Referencia de API: Datos de Cheques

## Método `get_checks_master`

```python
client.get_checks_master(
    debug=False,
    json=False
)
```

Obtiene el listado de entidades bancarias que operan con cheques.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame` con las siguientes columnas:

- `codigo`: Código de la entidad bancaria
- `nombre`: Nombre completo de la entidad

### Ejemplos

#### Consulta básica: obtener todas las entidades

```python
df = client.get_checks_master()
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.get_checks_master(debug=True)
print(api_url)
```

---

## Método `get_checks_reported`

```python
client.get_checks_reported(
    codigo_entidad=None,
    numero_cheque=None,
    debug=False,
    json=False
)
```

Obtiene información de cheques denunciados.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `codigo_entidad` | `int` | Código de la entidad bancaria | Sí |
| `numero_cheque` | `int` | Número del cheque a consultar | Sí |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame` con información sobre el cheque consultado y su estado.

### Ejemplos

#### Consulta de un cheque específico

```python
df = client.get_checks_reported(
    codigo_entidad=11,
    numero_cheque=20377516
)
print(df)
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.get_checks_reported(
    codigo_entidad=11,
    numero_cheque=20377516,
    debug=True
)
print(api_url)
```

---

# 🌐 API Reference: Check Data

## Method `get_checks_master`

```python
client.get_checks_master(
    debug=False,
    json=False
)
```

Retrieves the list of banking entities that operate with checks.

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns data as JSON instead of DataFrame | No |

### Return

By default, returns a `pandas.DataFrame` with the following columns:

- `codigo`: Banking entity code
- `nombre`: Full name of the entity

### Examples

#### Basic query: get all entities

```python
df = client.get_checks_master()
print(df.head())
```

#### Debug mode: get the API URL

```python
api_url = client.get_checks_master(debug=True)
print(api_url)
```

---

## Method `get_checks_reported`

```python
client.get_checks_reported(
    codigo_entidad=None,
    numero_cheque=None,
    debug=False,
    json=False
)
```

Retrieves information about reported checks.

### Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `codigo_entidad` | `int` | Banking entity code | Yes |
| `numero_cheque` | `int` | Check number to query | Yes |
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns data as JSON instead of DataFrame | No |

### Return

By default, returns a `pandas.DataFrame` with information about the queried check and its status.

### Examples

#### Query for a specific check

```python
df = client.get_checks_reported(
    codigo_entidad=11,
    numero_cheque=20377516
)
print(df)
```

#### Debug mode: get the API URL

```python
api_url = client.get_checks_reported(
    codigo_entidad=11,
    numero_cheque=20377516,
    debug=True
)
print(api_url)
```
