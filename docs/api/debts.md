# Debtors API

La API de deudores proporciona acceso a información sobre deudores y cheques rechazados.

## Método `debtors`

```python
client.debtors.debtors(
    identificacion=None,
    debug=False,
    json=False
)
```

Obtiene información sobre las deudas actuales de un deudor.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `identificacion` | `str` | CUIT/CUIL del deudor | No |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame`.

En caso de error del servidor (status_code != 200), se retornará el JSON de respuesta del servidor con el mensaje de error correspondiente.

### Ejemplos

#### Consulta básica: obtener deudas actuales

```python
df = client.debtors.debtors(identificacion="12345678")
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.debtors.debtors(identificacion="12345678", debug=True)
print(api_url)
```

## Método `history`

```python
client.debtors.history(
    identificacion=None,
    debug=False,
    json=False
)
```

Obtiene el historial de deudas de un deudor.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `identificacion` | `str` | CUIT/CUIL del deudor | No |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame`.

En caso de error del servidor (status_code != 200), se retornará el JSON de respuesta del servidor con el mensaje de error correspondiente.

### Ejemplos

#### Consulta básica: obtener historial de deudas

```python
df = client.debtors.history(identificacion="12345678")
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.debtors.history(identificacion="12345678", debug=True)
print(api_url)
```

## Método `rejected`

```python
client.debtors.rejected(
    identificacion=None,
    debug=False,
    json=False
)
```

Obtiene información sobre cheques rechazados asociados a un deudor.

### Parámetros

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `identificacion` | `str` | CUIT/CUIL del deudor | No |
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

### Retorno

Por defecto, devuelve un `pandas.DataFrame`.

En caso de error del servidor (status_code != 200), se retornará el JSON de respuesta del servidor con el mensaje de error correspondiente.

### Ejemplos

#### Consulta básica: obtener cheques rechazados

```python
df = client.debtors.rejected(identificacion="12345678")
print(df.head())
```

#### Modo de depuración: obtener la URL de la API

```python
api_url = client.debtors.rejected(identificacion="12345678", debug=True)
print(api_url)
```

### Notas

- La validación de parámetros (tipos, formatos, etc.) es gestionada por el paquete.
- Los errores del servidor (status_code != 200) se manejan devolviendo el JSON de respuesta del servidor.
- La identificación debe ser un CUIT/CUIL válido.
