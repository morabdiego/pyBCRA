# Instalación y Configuración

## Requisitos

- Python 3.7 o superior
- pandas

## Instalación

Puedes instalar pyBCRAdata directamente desde PyPI:

```bash
pip install pyBCRAdata
```

## Configuración básica

```python
from pyBCRAdata import BCRAclient

# Inicialización básica con certificados del sistema
client = BCRAclient()
```

## Configuración avanzada

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

## Importación alternativa

```python
import pyBCRAdata as client

# O importar métodos específicos
from pyBCRAdata import BCRAclient, get_monetary_data
```

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

## Alternative Import

```python
import pyBCRAdata as client

# Or import specific methods
from pyBCRAdata import BCRAclient, get_monetary_data
```
