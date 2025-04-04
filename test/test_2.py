from pyBCRAdata import BCRAclient

client = BCRAclient()

url = client.get_currency_timeseries(
    moneda='USD',
    fechadesde='2023-01-01',
    fechahasta='2023-10-01',
    limit=10,
    offset=0,
    debug=True
)

print(url)
