from src.pyBCRAdata.api.client import BCRAclient

client = BCRAclient()

# Test monetary data
url_monetary = client.get_monetary_data(id_variable="123", desde="2025-01-01", hasta="2025-03-31")
print(url_monetary)

# Test currency master
url_master = client.get_currency_master()
print(url_master)

# Test currency quotes
url_quotes = client.get_currency_quotes()
print(url_quotes)

# Test currency timeseries
url_timeseries = client.get_currency_timeseries(moneda="USD", fechadesde="2025-01-01", fechahasta="2025-03-31")
print(url_timeseries)
