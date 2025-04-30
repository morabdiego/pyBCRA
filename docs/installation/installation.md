# Instalación y Configuración

## Requisitos

- Python 3.7 o superior
- pandas

## Instalación

Puedes instalar pyBCRAdata directamente desde PyPI:

```bash
pip install pyBCRAdata
```

## Uso Básico

El paquete puede ser utilizado de dos formas:

### 1. Usando instancias preconfiguradas (recomendado)

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

# Inicialización básica con certificados del sistema
client = BCRAclient()
```

## Configuración Avanzada

Los certificados SSL tienen una fecha de expiración (el más próximo 23/4/2026). Intentaremos mantener el proyecto actualizado cuando esto suceda. Si encuentras errores SSL utiliza un certificado.pem actualizado, puedes obtenerlo por ejemplo de la siguiente manera:

1. Abre el sitio web en un navegador como Chrome o Firefox en alguna url de la api, por ejemplo https://api.bcra.gob.ar/estadisticas/v3.0/monetarias?.
2. Inspecciona el certificado del sitio (clic en el candado > Más información > Ver certificado).
3. Exporta la cadena completa de certificados (servidor, intermedio, raíz) y úsala en tu script. Debe ser un archivo.pem


### Certificados SSL personalizados

Si necesitas utilizar certificados personalizados:

```python
client = BCRAclient(
    cert_path="/ruta/a/tu/certificado.pem",
    verify_ssl=True
)
```

### Desactivar verificación SSL (no recomendado para producción)

```python
client = BCRAclient(verify_ssl=False)
```

## Ejemplos de Uso

### Obtener variables monetarias
```python
from pyBCRAdata import monetary

# Obtener lista de variables disponibles
variables = monetary.variables()

# Obtener serie histórica
serie = monetary.series(
    id_variable=1,
    desde="2023-01-01",
    hasta="2023-12-31"
)
```

### Consultar cotizaciones
```python
from pyBCRAdata import currency

# Obtener cotizaciones del día
cotizaciones = currency.rates(fecha="2024-01-01")

# Obtener serie histórica del dólar
serie = currency.series(
    moneda="USD",
    fechadesde="2023-01-01",
    fechahasta="2023-12-31"
)
```

### Consultar cheques
```python
from pyBCRAdata import checks

# Obtener entidades bancarias
bancos = checks.banks()

# Consultar cheque denunciado
cheque = checks.reported(
    codigo_entidad=123,
    numero_cheque=456789
)
```

### Consultar deudores
```python
from pyBCRAdata import debtors

# Consultar deudas actuales
deudas = debtors.debtors(identificacion="12345678")

# Consultar historial de deudas
historial = debtors.history(identificacion="12345678")

# Consultar cheques rechazados
rechazados = debtors.rejected(identificacion="12345678")
```

## Parámetros Comunes

Todas las APIs comparten algunos parámetros comunes:

- `json`: Si es `True`, retorna los datos en formato JSON en lugar de DataFrame
- `debug`: Si es `True`, retorna la URL construida en lugar de hacer la llamada a la API

## Manejo de Errores

El paquete maneja varios tipos de errores:

- `ValueError`: Cuando faltan argumentos requeridos o se proporcionan argumentos inválidos
- `requests.exceptions.RequestException`: Para errores de conexión o HTTP
- `pandas.errors.EmptyDataError`: Cuando no hay datos disponibles

---

# 🌐 Installation and Configuration

## Requirements

- Python 3.7 or higher
- pandas

## Installation

You can install pyBCRAdata directly from PyPI:

```bash
pip install pyBCRAdata
```

## Basic Configuration

```python
from pyBCRAdata import BCRAclient

# Basic initialization with system certificates
client = BCRAclient()
```

## Advanced Configuration

SSL certificates have an expiration date (the earliest is April 23, 2026). We will try to keep the project updated when this happens. If you encounter SSL errors, use an updated .pem certificate. You can obtain it, for example, as follows:

1. Open the website in a browser like Chrome or Firefox at an API URL, for example https://api.bcra.gob.ar/estadisticas/v3.0/monetarias?
2. Inspect the site's certificate (click the lock > More information > View certificate).
3. Export the complete certificate chain (server, intermediate, root) and use it in your script. It must be a .pem file.

### Custom SSL Certificates

If you need to use custom certificates:

```python
client = BCRAclient(
    cert_path="/path/to/your/certificate.pem",
    verify_ssl=True
)
```

### Disable SSL Verification (not recommended for production)

```python
client = BCRAclient(verify_ssl=False)
```

### URL base personalizada

If you need to use a different base URL:

```python
client = BCRAclient(
    base_url="https://api.custom.bcra.gob.ar",
    verify_ssl=True
)
```

## Alternative Import

```python
import pyBCRAdata as client

# Or import specific methods
from pyBCRAdata import BCRAclient, get_monetary_variables
```

## Usage Examples

### Getting monetary variables
```python
from pyBCRAdata import monetary

# Get list of available variables
variables = monetary.variables()

# Get historical series
serie = monetary.series(
    id_variable=1,
    desde="2023-01-01",
    hasta="2023-12-31"
)
```

### Getting currency rates
```python
from pyBCRAdata import currency

# Get currency rates for today
cotizaciones = currency.rates(fecha="2024-01-01")

# Get historical series of the dollar
serie = currency.series(
    moneda="USD",
    fechadesde="2023-01-01",
    fechahasta="2023-12-31"
)
```

### Getting checks
```python
from pyBCRAdata import checks

# Get bank entities
bancos = checks.banks()

# Get reported check
cheque = checks.reported(
    codigo_entidad=123,
    numero_cheque=456789
)
```

### Getting debtors
```python
from pyBCRAdata import debtors

# Get current debts
deudas = debtors.debtors(identificacion="12345678")

# Get debts history
historial = debtors.history(identificacion="12345678")

# Get rejected checks
rechazados = debtors.rejected(identificacion="12345678")
```

## Common Parameters

All APIs share some common parameters:

- `json`: If True, returns data in JSON format instead of DataFrame
- `debug`: If True, returns the constructed URL instead of making the API call

## Error Handling

The package handles several types of errors:

- `ValueError`: When required arguments are missing or invalid
- `requests.exceptions.RequestException`: For connection or HTTP errors
- `pandas.errors.EmptyDataError`: When no data is available
