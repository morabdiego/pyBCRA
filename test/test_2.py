from pyBCRAdata import BCRAclient

client = BCRAclient()

url = client.get_debts(
    identificacion='23409233449'
)

print(url)
