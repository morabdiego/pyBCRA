# Estadísticas Monetarias / Monetary Statistics

## Español

### Descripción
Acceso a las estadísticas monetarias y financieras publicadas por el BCRA, incluyendo variables monetarias y sus series históricas.

### Métodos Disponibles

#### `get_monetary_variables()`
Obtiene el listado de variables monetarias disponibles.

**Retorna:**
- `pandas.DataFrame`: DataFrame con las variables monetarias disponibles

**Ejemplo:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
variables = client.get_monetary_variables()
print(variables.head())
```

#### `get_monetary_series(id_variable, desde=None, hasta=None, limit=None, offset=None)`
Obtiene la serie histórica de una variable monetaria específica.

**Parámetros:**
- `id_variable` (str): ID de la variable monetaria
- `desde` (str, opcional): Fecha de inicio (formato YYYY-MM-DD)
- `hasta` (str, opcional): Fecha de fin (formato YYYY-MM-DD)
- `limit` (int, opcional): Límite de registros
- `offset` (int, opcional): Desplazamiento de registros

**Retorna:**
- `pandas.DataFrame`: DataFrame con la serie histórica

**Ejemplo:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
# Obtener tasa de política monetaria (ID: 6)
tpm = client.get_monetary_series(
    id_variable="6",
    desde="2024-01-01",
    hasta="2024-03-21"
)
print(tpm.head())
```

---

## English

### Description
Access to monetary and financial statistics published by the BCRA, including monetary variables and their historical series.

### Available Methods

#### `get_monetary_variables()`
Gets the list of available monetary variables.

**Returns:**
- `pandas.DataFrame`: DataFrame with available monetary variables

**Example:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
variables = client.get_monetary_variables()
print(variables.head())
```

#### `get_monetary_series(id_variable, desde=None, hasta=None, limit=None, offset=None)`
Gets the historical series of a specific monetary variable.

**Parameters:**
- `id_variable` (str): ID of the monetary variable
- `desde` (str, optional): Start date (format YYYY-MM-DD)
- `hasta` (str, optional): End date (format YYYY-MM-DD)
- `limit` (int, optional): Record limit
- `offset` (int, optional): Record offset

**Returns:**
- `pandas.DataFrame`: DataFrame with the historical series

**Example:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
# Get monetary policy rate (ID: 6)
tpm = client.get_monetary_series(
    id_variable="6",
    desde="2024-01-01",
    hasta="2024-03-21"
)
print(tpm.head())
```
