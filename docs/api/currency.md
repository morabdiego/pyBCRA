# Estadísticas Cambiarias / Exchange Rate Statistics

## Español

### Descripción
Acceso a las estadísticas cambiarias publicadas por el BCRA, incluyendo el listado de monedas, cotizaciones diarias y series históricas.

### Métodos Disponibles

#### `get_currencies()`
Obtiene el listado de monedas disponibles.

**Retorna:**
- `pandas.DataFrame`: DataFrame con las monedas disponibles

**Ejemplo:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
monedas = client.get_currencies()
print(monedas.head())
```

#### `get_exchange_rates(fecha=None)`
Obtiene las cotizaciones de todas las monedas para una fecha específica.

**Parámetros:**
- `fecha` (str, opcional): Fecha de consulta (formato YYYY-MM-DD). Si no se especifica, se usa la fecha actual.

**Retorna:**
- `pandas.DataFrame`: DataFrame con las cotizaciones

**Ejemplo:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
cotizaciones = client.get_exchange_rates(fecha="2024-03-21")
print(cotizaciones.head())
```

#### `get_currency_series(moneda, fechadesde=None, fechahasta=None, limit=None, offset=None)`
Obtiene la serie histórica de cotizaciones para una moneda específica.

**Parámetros:**
- `moneda` (str): Código de la moneda (ej: "USD")
- `fechadesde` (str, opcional): Fecha de inicio (formato YYYY-MM-DD)
- `fechahasta` (str, opcional): Fecha de fin (formato YYYY-MM-DD)
- `limit` (int, opcional): Límite de registros
- `offset` (int, opcional): Desplazamiento de registros

**Retorna:**
- `pandas.DataFrame`: DataFrame con la serie histórica

**Ejemplo:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
# Obtener serie histórica del dólar
usd = client.get_currency_series(
    moneda="USD",
    fechadesde="2024-01-01",
    fechahasta="2024-03-21"
)
print(usd.head())
```

---

## English

### Description
Access to exchange rate statistics published by the BCRA, including the list of currencies, daily quotes and historical series.

### Available Methods

#### `get_currencies()`
Gets the list of available currencies.

**Returns:**
- `pandas.DataFrame`: DataFrame with available currencies

**Example:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
currencies = client.get_currencies()
print(currencies.head())
```

#### `get_exchange_rates(fecha=None)`
Gets the exchange rates for all currencies on a specific date.

**Parameters:**
- `fecha` (str, optional): Query date (format YYYY-MM-DD). If not specified, current date is used.

**Returns:**
- `pandas.DataFrame`: DataFrame with exchange rates

**Example:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
rates = client.get_exchange_rates(fecha="2024-03-21")
print(rates.head())
```

#### `get_currency_series(moneda, fechadesde=None, fechahasta=None, limit=None, offset=None)`
Gets the historical series of exchange rates for a specific currency.

**Parameters:**
- `moneda` (str): Currency code (e.g. "USD")
- `fechadesde` (str, optional): Start date (format YYYY-MM-DD)
- `fechahasta` (str, optional): End date (format YYYY-MM-DD)
- `limit` (int, optional): Record limit
- `offset` (int, optional): Record offset

**Returns:**
- `pandas.DataFrame`: DataFrame with the historical series

**Example:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
# Get USD historical series
usd = client.get_currency_series(
    moneda="USD",
    fechadesde="2024-01-01",
    fechahasta="2024-03-21"
)
print(usd.head())
```
