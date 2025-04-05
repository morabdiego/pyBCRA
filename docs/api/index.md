# Referencia de API pyBCRAdata

Esta sección contiene la documentación detallada de todos los métodos disponibles en el cliente pyBCRAdata.

## Inicialización del Cliente

```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
```

También puede usar directamente los métodos exportados:

```python
from pyBCRAdata import get_monetary_data, get_currency_master

df = get_monetary_data(id_variable=1)
```

## Categorías de Datos

La API provee acceso a las siguientes categorías de datos:

### [Datos Monetarios](monetary.md)
- [`get_monetary_data`](monetary.md#método-get_monetary_data) - Estadísticas monetarias con filtros opcionales

### [Datos de Divisas](currency.md)
- [`get_currency_master`](currency.md#método-get_currency_master) - Catálogo maestro de divisas
- [`get_currency_quotes`](currency.md#método-get_currency_quotes) - Cotizaciones de divisas para una fecha específica
- [`get_currency_timeseries`](currency.md#método-get_currency_timeseries) - Series temporales de cotizaciones para una divisa específica

### [Datos de Cheques](checks.md)
- [`get_checks_master`](checks.md#método-get_checks_master) - Listado de entidades bancarias
- [`get_checks_reported`](checks.md#método-get_checks_reported) - Información de cheques denunciados

### [Datos de Central de Deudores](debts.md)
- [`get_debts`](debts.md#método-get_debts) - Información de deudas registradas por CUIT/CUIL
- [`get_debts_historical`](debts.md#método-get_debts_historical) - Histórico de deudas por CUIT/CUIL
- [`get_debts_rejected_checks`](debts.md#método-get_debts_rejected_checks) - Cheques rechazados asociados a un CUIT/CUIL

## Parámetros Comunes

Todos los métodos de la API aceptan los siguientes parámetros comunes:

| Parámetro | Tipo | Descripción | Requerido |
|-----------|------|-------------|-----------|
| `debug` | `bool` | Devuelve la URL en lugar de los datos | No |
| `json` | `bool` | Devuelve los datos como JSON en lugar de DataFrame | No |

---

# 🌐 pyBCRAdata API Reference

This section contains detailed documentation for all methods available in the pyBCRAdata client.

## Client Initialization

```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
```

You can also use the directly exported methods:

```python
from pyBCRAdata import get_monetary_data, get_currency_master

df = get_monetary_data(id_variable=1)
```

## Data Categories

The API provides access to the following data categories:

### [Monetary Data](monetary.md)
- [`get_monetary_data`](monetary.md#method-get_monetary_data) - Monetary statistics with optional filters

### [Currency Data](currency.md)
- [`get_currency_master`](currency.md#method-get_currency_master) - Currency master catalog
- [`get_currency_quotes`](currency.md#method-get_currency_quotes) - Currency quotes for a specific date
- [`get_currency_timeseries`](currency.md#method-get_currency_timeseries) - Time series of quotes for a specific currency

### [Check Data](checks.md)
- [`get_checks_master`](checks.md#method-get_checks_master) - List of banking entities
- [`get_checks_reported`](checks.md#method-get_checks_reported) - Information on reported checks

### [Debt Data](debts.md)
- [`get_debts`](debts.md#method-get_debts) - Debt information registered by tax ID (CUIT/CUIL)
- [`get_debts_historical`](debts.md#method-get_debts_historical) - Historical debt by tax ID (CUIT/CUIL)
- [`get_debts_rejected_checks`](debts.md#method-get_debts_rejected_checks) - Rejected checks associated with a tax ID (CUIT/CUIL)

## Common Parameters

All API methods accept the following common parameters:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns data as JSON instead of DataFrame | No |
