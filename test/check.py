from pyBCRAdata import BCRAclient

client = BCRAclient()

df = client.get_checks_reported(codigo_entidad=11, numero_cheque=203775991)
print(df)
