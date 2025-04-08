# Referencia de API pyBCRAdata

Esta sección contiene la documentación detallada de todos los métodos disponibles en el cliente pyBCRAdata.

## Inicialización del Cliente

```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
```

También puede usar directamente los métodos exportados:

```python
from pyBCRAdata import get_monetary_series, get_currencies

df = get_monetary_series(id_variable=1)
```

## Categorías de Datos

La API provee acceso a las siguientes categorías de datos:

### [Datos Monetarios](monetary.md)
- [`get_monetary_variables`](monetary.md#método-get_monetary_variables) - Listado de variables monetarias disponibles
- [`get_monetary_series`](monetary.md#método-get_monetary_series) - Series temporales de variables monetarias

### [Datos de Divisas](currency.md)
- [`get_currencies`](currency.md#método-get_currencies) - Catálogo maestro de divisas
- [`get_exchange_rates`](currency.md#método-get_exchange_rates) - Cotizaciones de divisas para una fecha específica
- [`get_currency_series`](currency.md#método-get_currency_series) - Series temporales de cotizaciones para una divisa específica

### [Datos de Cheques](checks.md)
- [`get_banks`](checks.md#método-get_banks) - Listado de entidades bancarias
- [`get_reported_checks`](checks.md#método-get_reported_checks) - Información de cheques denunciados

### [Datos de Central de Deudores](debts.md)
- [`get_debtors`](debts.md#método-get_debtors) - Información de deudas registradas por CUIT/CUIL
- [`get_debtors_history`](debts.md#método-get_debtors_history) - Histórico de deudas por CUIT/CUIL
- [`get_rejected_checks`](debts.md#método-get_rejected_checks) - Cheques rechazados asociados a un CUIT/CUIL

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
from pyBCRAdata import get_monetary_series, get_currencies

df = get_monetary_series(id_variable=1)
```

## Data Categories

The API provides access to the following data categories:

### [Monetary Data](monetary.md)
- [`get_monetary_variables`](monetary.md#method-get_monetary_variables) - List of available monetary variables
- [`get_monetary_series`](monetary.md#method-get_monetary_series) - Time series of monetary variables

### [Currency Data](currency.md)
- [`get_currencies`](currency.md#method-get_currencies) - Currency master catalog
- [`get_exchange_rates`](currency.md#method-get_exchange_rates) - Currency quotes for a specific date
- [`get_currency_series`](currency.md#method-get_currency_series) - Time series of quotes for a specific currency

### [Check Data](checks.md)
- [`get_banks`](checks.md#method-get_banks) - List of banking entities
- [`get_reported_checks`](checks.md#method-get_reported_checks) - Information on reported checks

### [Debt Data](debts.md)
- [`get_debtors`](debts.md#method-get_debtors) - Debt information registered by tax ID (CUIT/CUIL)
- [`get_debtors_history`](debts.md#method-get_debtors_history) - Historical debt by tax ID (CUIT/CUIL)
- [`get_rejected_checks`](debts.md#method-get_rejected_checks) - Rejected checks associated with a tax ID (CUIT/CUIL)

## Common Parameters

All API methods accept the following common parameters:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| `debug` | `bool` | Returns the URL instead of the data | No |
| `json` | `bool` | Returns data as JSON instead of DataFrame | No |
