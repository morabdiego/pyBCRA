# Ejemplo: Análisis de Datos Monetarios

En este ejemplo, mostraremos cómo obtener y visualizar la tasa de política monetaria del BCRA a lo largo del tiempo.

## Obtener los datos

```python
import pandas as pd
import matplotlib.pyplot as plt
from pyBCRAdata import BCRAclient

# Inicializar el cliente
client = BCRAclient()

# Obtener la tasa de política monetaria (variable ID=6)
df = client.get_monetary_data(
    id_variable="6",  # Tasa de Política Monetaria (en % n.a.)
    desde="2023-01-01",
    hasta="2024-03-21"
)

# Convertir la fecha a formato datetime
df['fecha'] = pd.to_datetime(df['fecha'])

# Ordenar por fecha
df = df.sort_values('fecha')
```

## Visualizar los datos

```python
# Configurar el gráfico
plt.figure(figsize=(12, 6))
plt.plot(df['fecha'], df['valor'], linewidth=2)

# Añadir títulos y etiquetas
plt.title('Tasa de Política Monetaria del BCRA', fontsize=16)
plt.xlabel('Fecha', fontsize=12)
plt.ylabel('Tasa (% n.a.)', fontsize=12)
plt.grid(True, alpha=0.3)

# Mejorar el formato del eje Y
plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(100))

# Mostrar el gráfico
plt.tight_layout()
plt.show()
```

## Análisis estadístico básico

```python
# Calcular estadísticas descriptivas
stats = df['valor'].describe()
print("Estadísticas descriptivas:")
print(stats)

# Calcular cambio porcentual mes a mes
df['mes'] = df['fecha'].dt.to_period('M')
monthly_avg = df.groupby('mes')['valor'].mean()
monthly_change = monthly_avg.pct_change() * 100

print("\nCambio porcentual mes a mes:")
print(monthly_change)
```

Este ejemplo muestra cómo obtener, visualizar y realizar un análisis básico de la tasa de política monetaria. Puede adaptarse fácilmente para otras variables monetarias cambiando el `id_variable`.
