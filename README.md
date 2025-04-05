# pyBCRAdata v0.3.3

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

Requiere **Python 3.7+**, **requests** y **pandas**. Ver [documentación de instalación](https://github.com/morabdiego/pyBCRA/blob/main/docs/guides/installation.md) para más detalles.

## 📊 Ejemplo Rápido

```python
from pyBCRAdata import BCRAclient

# Inicializar cliente
client = BCRAclient()

# Obtener tasa de política monetaria
df = client.get_monetary_data(
    id_variable="6",  # Tasa de Política Monetaria (en % n.a.)
    desde="2024-01-01",
    hasta="2024-03-21"
)
print(df.head())

# Obtener cotización histórica del dólar
usd = client.get_currency_timeseries(
    moneda="USD",
    fechadesde="2024-01-01",
    fechahasta="2024-03-21"
)
print(usd.head())
```

## 📚 Documentación

La documentación completa está disponible en la carpeta [docs](https://github.com/morabdiego/pyBCRA/tree/main/docs/):

- **[Guías de Usuario](https://github.com/morabdiego/pyBCRA/tree/main/docs/guides/)** - Instrucciones paso a paso para tareas comunes
- **[Referencia de API](https://github.com/morabdiego/pyBCRA/tree/main/docs/api/)** - Información detallada sobre cada método
- **[Ejemplos Prácticos](https://github.com/morabdiego/pyBCRA/tree/main/docs/examples/)** - Casos de uso para implementaciones específicas

> **Nota**: Toda la documentación está disponible en español e inglés. Cada archivo incluye ambos idiomas con una separación clara.

### Principales áreas de datos

- **[Datos Monetarios](https://github.com/morabdiego/pyBCRA/blob/main/docs/guides/monetary_data.md)** - Estadísticas monetarias y financieras
- **[Datos de Divisas](https://github.com/morabdiego/pyBCRA/blob/main/docs/guides/currency_data.md)** - Cotizaciones y series históricas
- **[Información de Deudores](https://github.com/morabdiego/pyBCRA/blob/main/docs/guides/debtors_data.md)** - Consultas sobre deudas y cheques rechazados

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

---

# pyBCRAdata v0.3.3 [English]

Python client to access monetary statistics, exchange rate data, and debtor information published by the Central Bank of the Argentine Republic (BCRA).
Designed for economists, analysts, and developers working with macroeconomic data.

📍 **GitHub Repository**: [https://github.com/morabdiego/pyBCRA](https://github.com/morabdiego/pyBCRA)

## 🛆 Installation

```bash
pip install pyBCRAdata
```

Requires **Python 3.7+**, **requests**, and **pandas**. See [installation documentation](https://github.com/morabdiego/pyBCRA/blob/main/docs/guides/installation.md) for more details.

## 📊 Quick Example

```python
from pyBCRAdata import BCRAclient

# Initialize client
client = BCRAclient()

# Get monetary policy rate
df = client.get_monetary_data(
    id_variable="6",  # Monetary Policy Rate (in % p.a.)
    desde="2024-01-01",
    hasta="2024-03-21"
)
print(df.head())

# Get historical USD exchange rate
usd = client.get_currency_timeseries(
    moneda="USD",
    fechadesde="2024-01-01",
    fechahasta="2024-03-21"
)
print(usd.head())
```

## 📚 Documentation

Complete documentation is available in the [docs](https://github.com/morabdiego/pyBCRA/tree/main/docs/) folder:

- **[User Guides](https://github.com/morabdiego/pyBCRA/tree/main/docs/guides/)** - Step-by-step instructions for common tasks
- **[API Reference](https://github.com/morabdiego/pyBCRA/tree/main/docs/api/)** - Detailed information about each method
- **[Practical Examples](https://github.com/morabdiego/pyBCRA/tree/main/docs/examples/)** - Use cases for specific implementations

> **Note**: All documentation is available in both Spanish and English. Each file includes both languages with clear separation.

### Main Data Areas

- **[Monetary Data](https://github.com/morabdiego/pyBCRA/blob/main/docs/guides/monetary_data.md)** - Monetary and financial statistics
- **[Currency Data](https://github.com/morabdiego/pyBCRA/blob/main/docs/guides/currency_data.md)** - Exchange rates and historical series
- **[Debtor Information](https://github.com/morabdiego/pyBCRA/blob/main/docs/guides/debtors_data.md)** - Queries about debts and rejected checks

## 🔑 API Access

This client interacts with the public BCRA APIs available in the [BCRA API Catalog](https://www.bcra.gob.ar/BCRAyVos/catalogo-de-APIs-banco-central.asp).

No authentication token is required, but please note that:
- The BCRA may implement rate limitations based on IP address
- Consider implementing caching for frequently accessed data

For detailed information on error handling, server responses, and legal notices, please refer directly to the [BCRA API Catalog](https://www.bcra.gob.ar/BCRAyVos/catalogo-de-APIs-banco-central.asp) page. This project is solely a client to facilitate data access, and all legal responsibility belongs to the BCRA as the API provider.

## 👋 About

Created by Diego Mora — Economist and Python Developer.

- [LinkedIn](https://www.linkedin.com/in/morabdiego)
- [GitHub](https://github.com/morabdiego)
- 📧 Email: morabdiego@gmail.com

## 📜 License

This project is licensed under [Creative Commons Attribution-NonCommercial 4.0 International License](http://creativecommons.org/licenses/by-nc/4.0/).
