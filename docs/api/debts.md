# Central de Deudores / Debtors Central

## Español

### Descripción
Acceso a la información de deudores del BCRA, incluyendo deudas actuales, historial de deudas y cheques rechazados.

### Métodos Disponibles

#### `get_debtors(identificacion)`
Obtiene información sobre las deudas actuales de un deudor.

**Parámetros:**
- `identificacion` (str): Número de CUIT/CUIL/DNI del deudor

**Retorna:**
- `pandas.DataFrame`: DataFrame con la información de deudas

**Ejemplo:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
deudas = client.get_debtors(identificacion="20123456789")
print(deudas.head())
```

#### `get_debtors_history(identificacion)`
Obtiene el historial de deudas de un deudor.

**Parámetros:**
- `identificacion` (str): Número de CUIT/CUIL/DNI del deudor

**Retorna:**
- `pandas.DataFrame`: DataFrame con el historial de deudas

**Ejemplo:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
historial = client.get_debtors_history(identificacion="20123456789")
print(historial.head())
```

#### `get_rejected_checks(identificacion)`
Obtiene información sobre cheques rechazados de un deudor.

**Parámetros:**
- `identificacion` (str): Número de CUIT/CUIL/DNI del deudor

**Retorna:**
- `pandas.DataFrame`: DataFrame con la información de cheques rechazados

**Ejemplo:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
cheques = client.get_rejected_checks(identificacion="20123456789")
print(cheques.head())
```

---

## English

### Description
Access to BCRA's debtor information, including current debts, debt history and rejected checks.

### Available Methods

#### `get_debtors(identificacion)`
Gets information about a debtor's current debts.

**Parameters:**
- `identificacion` (str): CUIT/CUIL/DNI number of the debtor

**Returns:**
- `pandas.DataFrame`: DataFrame with debt information

**Example:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
debts = client.get_debtors(identificacion="20123456789")
print(debts.head())
```

#### `get_debtors_history(identificacion)`
Gets a debtor's debt history.

**Parameters:**
- `identificacion` (str): CUIT/CUIL/DNI number of the debtor

**Returns:**
- `pandas.DataFrame`: DataFrame with debt history

**Example:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
history = client.get_debtors_history(identificacion="20123456789")
print(history.head())
```

#### `get_rejected_checks(identificacion)`
Gets information about a debtor's rejected checks.

**Parameters:**
- `identificacion` (str): CUIT/CUIL/DNI number of the debtor

**Returns:**
- `pandas.DataFrame`: DataFrame with rejected checks information

**Example:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
checks = client.get_rejected_checks(identificacion="20123456789")
print(checks.head())
```
