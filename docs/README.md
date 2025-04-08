# pyBCRAdata v0.3.4

[![PyPI version](https://img.shields.io/pypi/v/pyBCRAdata.svg?logo=pypi&logoColor=white)](https://badge.fury.io/py/pyBCRAdata)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg?logo=creative-commons&logoColor=white)](http://creativecommons.org/licenses/by-nc/4.0/)
[![pandas](https://img.shields.io/badge/pandas-dependency-brightgreen.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![requests](https://img.shields.io/badge/requests-dependency-blue.svg?logo=python&logoColor=white)](https://docs.python-requests.org/)
[![Argentina](https://img.shields.io/badge/Country-Argentina-blue.svg?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI4MDAiIGhlaWdodD0iNTAwIj48cGF0aCBmaWxsPSIjNzRBQ0RGIiBkPSJNMCAwaDgwMHY1MDBIMHoiLz48cGF0aCBmaWxsPSIjZmZmIiBkPSJNMCAxNjdoODAwdjE2NkgweiIvPjxjaXJjbGUgZmlsbD0iI0ZDRDExNiIgY3g9IjQwMCIgY3k9IjI1MCIgcj0iNTgiLz48L3N2Zz4=)](https://www.bcra.gob.ar/)
[![Documentation](https://img.shields.io/badge/docs-GitHub-yellow.svg?logo=github&logoColor=white)](https://github.com/morabdiego/pyBCRA/tree/main/docs)

Cliente Python para acceder a estadísticas monetarias, datos de tipo de cambio e información de deudores publicados por el Banco Central de la República Argentina (BCRA).
Diseñado para economistas, analistas y desarrolladores que trabajan con datos macroeconómicos.

📍 **Repositorio GitHub**: [https://github.com/morabdiego/pyBCRA](https://github.com/morabdiego/pyBCRA)

## 🛆 Instalación

```bash
pip install pyBCRAdata
```

Requiere **Python 3.7+**, **requests** y **pandas**. Ver [documentación de instalación](https://github.com/morabdiego/pyBCRA/blob/main/docs/installation/installation.md) para más detalles.

## 📊 Ejemplo Rápido

```python
from pyBCRAdata import BCRAclient

# Inicializar cliente
client = BCRAclient()

# Obtener tasa de política monetaria
df = client.get_monetary_series(
    id_variable="6",  # Tasa de Política Monetaria (en % n.a.)
    desde="2024-01-01",
    hasta="2024-03-21"
)
print(df.head())

# Obtener cotización histórica del dólar
usd = client.get_currency_series(
    moneda="USD",
    fechadesde="2024-01-01",
    fechahasta="2024-03-21"
)
print(usd.head())
```

## 📚 Documentación

La documentación completa está disponible en la carpeta [docs](https://github.com/morabdiego/pyBCRA/tree/main/docs/):

- **[Documentación de Instalación](https://github.com/morabdiego/pyBCRA/tree/main/docs/installation/)** - Instrucciones para la instalación
- **[Referencia de API](https://github.com/morabdiego/pyBCRA/tree/main/docs/api/)** - Información detallada sobre cada método

> **Nota**: Toda la documentación está disponible en español e inglés. Cada archivo incluye ambos idiomas con una separación clara.

### Principales áreas de datos

- **[Estadísticas Monetarias](https://github.com/morabdiego/pyBCRA/blob/main/docs/api/monetary.md)** - Variables monetarias y series históricas
- **[Estadísticas Cambiarias](https://github.com/morabdiego/pyBCRA/blob/main/docs/api/currency.md)** - Monedas, cotizaciones y series históricas
- **[Central de Deudores](https://github.com/morabdiego/pyBCRA/blob/main/docs/api/debts.md)** - Deudores, historial y cheques rechazados
- **[Cheques Denunciados](https://github.com/morabdiego/pyBCRA/blob/main/docs/api/checks.md)** - Bancos y cheques denunciados

## 🔑 Acceso a la API

Este cliente interactúa con las APIs públicas del BCRA disponibles en el [Catálogo de APIs del BCRA](https://www.bcra.gob.ar/BCRAyVos/catalogo-de-APIs-banco-central.asp).

No se requiere token de autenticación, pero tenga en cuenta que:
- El BCRA puede implementar limitaciones de tasa basadas en dirección IP
- Considere implementar caché para datos de acceso frecuente

Para información detallada sobre manejo de errores, respuestas del servidor y avisos legales, consulte directamente la página del [Catálogo de APIs del BCRA](https://www.bcra.gob.ar/BCRAyVos/catalogo-de-APIs-banco-central.asp). Este proyecto es únicamente un cliente para facilitar el acceso a los datos y toda responsabilidad legal corresponde al BCRA como proveedor de la API.

## 👋 Acerca de

Creado por Diego Mora — Economista y Desarrollador Python.

- [LinkedIn](https://www.linkedin.com/in/morabdiego)
- [GitHub](https://github.com/morabdiego)
- 📧 Email: morabdiego@gmail.com

## 📜 Licencia

Este proyecto está licenciado bajo [Creative Commons Attribution-NonCommercial 4.0 International License](http://creativecommons.org/licenses/by-nc/4.0/).

---

# Documentación de pyBCRAdata

Esta carpeta contiene la documentación completa de pyBCRAdata.

## Estructura

- **`/installation`** - Guías de usuario y tutoriales
  - [Instalación y configuración](installation/installation.md)

- **`/api`** - Referencia detallada de la API
  - [Índice](api/index.md)
  - [Estadísticas Monetarias](api/monetary.md) - Variables monetarias y series históricas
  - [Estadísticas Cambiarias](api/currency.md) - Monedas, cotizaciones y series históricas
  - [Central de Deudores](api/debts.md) - Deudores, historial y cheques rechazados
  - [Cheques Denunciados](api/checks.md) - Bancos y cheques denunciados

---

# pyBCRAdata Documentation

This folder contains the complete documentation for pyBCRAdata.

## Structure

- **`/installation`** - User guides and tutorials
  - [Installation and setup](installation/installation.md)

- **`/api`** - Detailed API reference
  - [Index](api/index.md)
  - [Monetary Statistics](api/monetary.md) - Monetary variables and historical series
  - [Exchange Rate Statistics](api/currency.md) - Currencies, exchange rates and historical series
  - [Debtors Central](api/debts.md) - Debtors, history and rejected checks
  - [Reported Checks](api/checks.md) - Banks and reported checks
