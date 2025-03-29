from pyBCRAdata import APIGetter

# Initialize the client with your API token
client = APIGetter()

# Try getting some data
df = client.get_currency_quotes()
print(df.head())
