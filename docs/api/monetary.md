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
| `id_variable` | `int` | ID de la variable a consultar | No |
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
