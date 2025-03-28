from pyBCRAdata import APIGetter

# Initialize the client with your API token
client = APIGetter()

# Try getting some data
df = client.get_monetary_data()
print(df.head())
