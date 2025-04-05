from pyBCRAdata import BCRAclient

client = BCRAclient()

df_1 = client.get_monetary_data(id_variable=6)
df_2 = client.get_monetary_data()
df_3 = client.get_monetary_data(id_variable=6, desde='2023-01-01', hasta='2023-01-31', limit=10, offset=0)

print(df_1.head())
print(df_2.head())
print(df_3.head())
