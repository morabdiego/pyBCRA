# pyBCRAdata API Reference

## Overview

pyBCRAdata es un cliente Python para acceder a la API del Banco Central de la República Argentina (BCRA). Proporciona una interfaz simple y eficiente para obtener datos económicos y financieros.

## Instalación

```bash
pip install pyBCRAdata
```

## Uso Básico

El paquete puede ser utilizado de dos formas:

### 1. Usando instancias preconfiguradas

```python
from pyBCRAdata import monetary, currency, checks, debtors

# Obtener variables monetarias
monetary.variables()

# Obtener cotizaciones de monedas
currency.rates(fecha="2024-01-01")

# Obtener entidades bancarias
checks.banks()

# Consultar deudores
debtors.debtors(identificacion="12345678")
```

### 2. Usando el cliente completo

```python
from pyBCRAdata import BCRAclient

# Crear cliente con configuración personalizada
client = BCRAclient(
    base_url="https://api.bcra.gob.ar",  # Opcional
    cert_path="/path/to/cert.pem",       # Opcional
    verify_ssl=True                      # Opcional
)

# Usar las APIs
client.monetary.variables()
client.currency.rates(fecha="2024-01-01")
client.checks.banks()
client.debtors.debtors(identificacion="12345678")
```

## APIs Disponibles

El paquete proporciona acceso a las siguientes APIs:

- [Monetary API](monetary.md): Datos monetarios y financieros
- [Currency API](currency.md): Cotizaciones y tipos de cambio
- [Checks API](checks.md): Información sobre cheques y entidades bancarias
- [Debtors API](debts.md): Consulta de deudores y cheques rechazados

## Parámetros Comunes

Todas las APIs comparten algunos parámetros comunes:

- `json`: Si es `True`, retorna los datos en formato JSON en lugar de DataFrame
- `debug`: Si es `True`, retorna la URL construida en lugar de hacer la llamada a la API

## Manejo de Errores

- La validación de parámetros (tipos, formatos, etc.) es gestionada por el paquete.
- Los errores del servidor (status_code != 200) se manejan devolviendo el JSON de respuesta del servidor.
- Por defecto, todos los métodos retornan un `pandas.DataFrame` con los datos solicitados.
