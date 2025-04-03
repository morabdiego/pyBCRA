# pyBCRAdata v0.2.0

A Python client for accessing monetary statistics and foreign exchange data published by the Central Bank of Argentina (BCRA). Designed for economists, analysts, and developers working with macroeconomic data.

📍 **GitHub Repository**: [https://github.com/morabdiego/pyBCRA](https://github.com/morabdiego/pyBCRA)

## 📦 Installation

```bash
pip install pyBCRAdata
```

## 🔑 API Access

This client interacts with BCRA's public APIs available at [BCRA's API Catalog](https://www.bcra.gob.ar/BCRAyVos/catalogo-de-APIs-banco-central.asp).

No authentication token is required to access the data. However, please note:
- BCRA may implement rate limiting based on IP address
- Be mindful of request frequency to avoid potential access restrictions
- Consider implementing caching for frequently accessed data

```python
from pyBCRAdata import BCRAclient

# Initialize the client
client = BCRAclient()

# Make API calls
df = client.get_monetary_data()
```

## 🏦 Monetary Data

### Get Monetary Statistics
```python
# Basic monetary data query. Get all id_variables availables
df = client.get_monetary_data()

# With filters and pagination
df = client.get_monetary_data(
    id_variable="6",  # Tasa de Política Monetaria (en % n.a.)
    desde="2024-01-01",
    hasta="2024-03-21",
    limit=100
)
print(df.head())
```

## 💱 Currency Data

### 1. Get Currency Master Data
```python
# Get list of available currencies
currencies = client.get_currency_master()
print(currencies.head())

# Debug mode
api_url = client.get_currency_master(debug=True)
```

### 2. Get Currency Quotes
```python
# Get latest exchange rates
latest_rates = client.get_currency_quotes()

# Get historical rates with pagination
historical_rates = client.get_currency_quotes(
    fecha="2024-03-15",
    offset=0,
    limit=100
)
print(historical_rates)
```

### 3. Get Currency Time Series
```python
# Get historical data for a specific currency
usd_history = client.get_currency_timeseries(
    moneda="USD",  # Required parameter
    fechadesde="2023-01-01",
    fechahasta="2024-01-01",
    offset=0,
    limit=500
)
print(usd_history.head())
```

## 📚 API Reference

### Initialization
```python
from pyBCRAdata import BCRAclient

# Basic initialization with system certificates
client = BCRAclient()
```
```python
import pyBCRAdata as client
# or
# from pyBCRAdata import get_*
```

- `BCRAclient(cert_path=None, verify_ssl=True)`
    - `cert_path`: If you need to use a custom SSL certificate, specify its path here. Use this only if the default certificate has expired.
    - `verify_ssl`: If SSL certificate has expired you can disable SSL verification. Not recommended for production environments
    - If using a custom certificate, ensure it includes all required certificates (root, intermediate, server)
    - Custom certificates can be obtained from api.bcra.gob.ar

### Monetary Data Methods
- `get_monetary_data(id_variable=None, desde=None, hasta=None, offset=None, limit=None, debug=False, json=False)`
    - Get monetary statistics with optional variable ID, date range and pagination
    - `id_variable`: Specific monetary variable ID
    - `desde`: Start date (YYYY-MM-DD)
    - `hasta`: End date (YYYY-MM-DD)
    - `offset`: Pagination offset.
    - `limit`: Maximum number of records
    - `debug`: Return URL instead of data
    - `json`: Return data as JSON instead of DataFrame

### Currency Data Methods
- `get_currency_master(debug=False, json=False)`
    - Get list of available currencies and their codes
    - `debug`: Return URL instead of data
    - `json`: Return data as JSON instead of DataFrame

- `get_currency_quotes(fecha=None, offset=None, limit=None, debug=False, json=False)`
    - Get exchange rates for all currencies
    - `fecha`: Specific date (YYYY-MM-DD)
    - `offset`: Pagination offset
    - `limit`: Maximum number of records
    - `debug`: Return URL instead of data
    - `json`: Return data as JSON instead of DataFrame

- `get_currency_timeseries(moneda, fechadesde=None, fechahasta=None, offset=None, limit=None, debug=False, json=False)`
    - Get historical exchange rates for a specific currency
    - `moneda`: Currency ISO code (Required)
    - `fechadesde`: Start date (YYYY-MM-DD)
    - `fechahasta`: End date (YYYY-MM-DD)
    - `offset`: Pagination offset
    - `limit`: Maximum number of records
    - `debug`: Return URL instead of data
    - `json`: Return data as JSON instead of DataFrame

## 🛠️ Data Response Format

All methods return pandas DataFrames by default, but can return JSON if `json=True` is specified. For more information about the structure of the API's data, refer to the BCRA's documentation or test the methods directly.

## 🗺️ Roadmap

Future versions will include:
- SSL certificate manager
- Integration with BCRA's Debtors and Checks APIs
- Cache Manager
- Examples in Google Colab

## 👋 About

Created by Diego Mora — Economist and Python Developer.
- [LinkedIn](https://www.linkedin.com/in/morabdiego)
- [GitHub](https://github.com/morabdiego)
- Email: morabdiego@gmail.com

## 🤝 Contributing

Issues, suggestions, and contributions are welcome! Feel free to:
- Report issues via GitHub Issues
- Send suggestions or feedback to morabdiego@gmail.com
- Submit pull requests with improvements

## 📜 License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](http://creativecommons.org/licenses/by-nc/4.0/).

You are free to:
- Share: Copy and redistribute the material in any medium or format
- Adapt: Remix, transform, and build upon the material

Under the following terms:
- Attribution: You must give appropriate credit
- NonCommercial: You may not use the material for commercial purposes
