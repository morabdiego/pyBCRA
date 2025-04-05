from pyBCRAdata import BCRAclient

client = BCRAclient()

result = client.get_debts(
    identificacion='23409233449'
)

print(result)
