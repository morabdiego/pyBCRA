import json
from pyBCRAdata import BCRAclient

# Initialize the client
client = BCRAclient()

# Dictionary to store column information
columns_info = {}

# Test get_monetary_data
print("Testing get_monetary_data...")
try:
    df_monetary = client.get_monetary_data(desde="2023-01-01", hasta="2023-12-31", limit=5)
    print(df_monetary.head())
    columns_info["get_monetary_data"] = list(df_monetary.columns)
except Exception as e:
    print(f"Error in get_monetary_data: {e}")

# Test get_currency_master
print("\nTesting get_currency_master...")
try:
    debug_url = client.get_currency_master(debug=True)
    print(f"Debug URL for get_currency_master: {debug_url}")
    df_currency_master = client.get_currency_master()
    print(df_currency_master.head())
    columns_info["get_currency_master"] = list(df_currency_master.columns)
except Exception as e:
    print(f"Error in get_currency_master: {e}")

# Test get_currency_quotes
print("\nTesting get_currency_quotes...")
try:
    debug_url = client.get_currency_quotes(debug=True)
    print(f"Debug URL for get_currency_quotes: {debug_url}")
    df_currency_quotes = client.get_currency_quotes()
    print(df_currency_quotes.head())
    columns_info["get_currency_quotes"] = list(df_currency_quotes.columns)
except Exception as e:
    print(f"Error in get_currency_quotes: {e}")

# Test get_currency_timeseries
print("\nTesting get_currency_timeseries...")
try:
    debug_url = client.get_currency_timeseries(
        moneda="USD",
        fechadesde="2023-01-01",
        fechahasta="2023-12-31",
        limit=10,
        debug=True
    )
    print(f"Debug URL for get_currency_timeseries: {debug_url}")
    df_currency_timeseries = client.get_currency_timeseries(
        moneda="USD",
        fechadesde="2023-01-01",
        fechahasta="2023-12-31",
        limit=10
    )
    print(df_currency_timeseries.head())
    columns_info["get_currency_timeseries"] = list(df_currency_timeseries.columns)
except Exception as e:
    print(f"Error in get_currency_timeseries: {e}")

# Save column information to a JSON file
output_file = "columns_info.json"
try:
    with open(output_file, "w") as f:
        json.dump(columns_info, f, indent=4)
    print(f"\nColumn information saved to {output_file}")
except Exception as e:
    print(f"Error saving column information: {e}")
