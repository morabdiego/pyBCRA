# Instalación y Configuración

## Requisitos

- Python 3.7 o superior
- pandas
- requests

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
