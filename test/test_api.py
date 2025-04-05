"""
Script para probar las funcionalidades de la API de BCRA relacionadas con deudas.
Este script muestra cómo utilizar los métodos para consultar deudas actuales,
históricas y cheques rechazados.
"""

import pandas as pd
from pyBCRAdata import BCRAclient

# Configuración de pandas para mostrar todas las columnas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Crear instancia del cliente
client = BCRAclient()

# CUIT/CUIL de ejemplo (reemplazar con uno válido)
identificacion = '23409233449'

# Función auxiliar para imprimir resultados
def print_result(title, result):
    print("\n" + "="*80)
    print(f" {title} ".center(80, "="))
    print("="*80)

    if isinstance(result, pd.DataFrame):
        if result.empty:
            print("Sin resultados (DataFrame vacío)")
        else:
            print(f"Resultado (DataFrame con {len(result)} filas y {len(result.columns)} columnas):")
            print(result.head())
    else:
        print("Resultado (JSON):")
        print(result)
    print("-"*80)

# 1. Probar get_debts (deudas actuales)
print("\nProbando get_debts...")
try:
    # Obtener el resultado como DataFrame (por defecto)
    debts_df = client.get_debts(identificacion=identificacion)
    print_result("DEUDAS ACTUALES (DataFrame)", debts_df)

    # Obtener el resultado como JSON raw
    debts_json = client.get_debts(identificacion=identificacion, json=True)
    print_result("DEUDAS ACTUALES (JSON)", debts_json)

    # Obtener solo la URL
    debts_url = client.get_debts(identificacion=identificacion, debug=True)
    print_result("DEUDAS ACTUALES (URL)", debts_url)

except Exception as e:
    print(f"Error en get_debts: {e}")

# 2. Probar get_debts_historical (deudas históricas)
print("\nProbando get_debts_historical...")
try:
    # Obtener el resultado como DataFrame (por defecto)
    hist_df = client.get_debts_historical(identificacion=identificacion)
    print_result("DEUDAS HISTÓRICAS (DataFrame)", hist_df)

    # Obtener el resultado como JSON raw
    hist_json = client.get_debts_historical(identificacion=identificacion, json=True)
    print_result("DEUDAS HISTÓRICAS (JSON)", hist_json)

    # Obtener solo la URL
    hist_url = client.get_debts_historical(identificacion=identificacion, debug=True)
    print_result("DEUDAS HISTÓRICAS (URL)", hist_url)

except Exception as e:
    print(f"Error en get_debts_historical: {e}")

# 3. Probar get_debts_rejected_checks (cheques rechazados)
print("\nProbando get_debts_rejected_checks...")
try:
    # Obtener el resultado como DataFrame (por defecto)
    checks_df = client.get_debts_rejected_checks(identificacion=identificacion)
    print_result("CHEQUES RECHAZADOS (DataFrame)", checks_df)

    # Obtener el resultado como JSON raw
    checks_json = client.get_debts_rejected_checks(identificacion=identificacion, json=True)
    print_result("CHEQUES RECHAZADOS (JSON)", checks_json)

    # Obtener solo la URL
    checks_url = client.get_debts_rejected_checks(identificacion=identificacion, debug=True)
    print_result("CHEQUES RECHAZADOS (URL)", checks_url)

except Exception as e:
    print(f"Error en get_debts_rejected_checks: {e}")

print("\nPruebas completadas.")
