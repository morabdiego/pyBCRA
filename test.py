from src.pyBCRAdata.getter import BCRAclient

client = BCRAclient()

# Test monetary data
url_monetary = client.get_monetary_data(id_variable="123", desde="2025-01-01", hasta="2025-03-31", debug=True)
print(url_monetary)

# Test currency master
url_master = client.get_currency_master(debug=True)
print(url_master)

# Test currency quotes
url_quotes = client.get_currency_quotes(debug=True)
print(url_quotes)

# Test currency timeseries
url_timeseries = client.get_currency_timeseries(moneda="USD", fechadesde="2025-01-01", fechahasta="2025-03-31", debug=True)
print(url_timeseries)
