from pyBCRAdata import BCRAclient

# Initialize the client with your API token
client = BCRAclient()

# Try getting some data
df = client.get_currency_quotes()
print(df.head())
