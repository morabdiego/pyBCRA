# Cheques Denunciados / Reported Checks

## Español

### Descripción
Acceso a la información sobre cheques denunciados publicada por el BCRA, incluyendo el listado de entidades bancarias y cheques denunciados.

### Métodos Disponibles

#### `get_banks()`
Obtiene el listado de entidades bancarias emisoras.

**Retorna:**
- `pandas.DataFrame`: DataFrame con las entidades bancarias

**Ejemplo:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
bancos = client.get_banks()
print(bancos.head())
```

#### `get_reported_checks(codigo_entidad, numero_cheque)`
Obtiene información sobre un cheque denunciado específico.

**Parámetros:**
- `codigo_entidad` (str): Código de la entidad bancaria emisora
- `numero_cheque` (str): Número del cheque

**Retorna:**
- `pandas.DataFrame`: DataFrame con la información del cheque denunciado

**Ejemplo:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
cheque = client.get_reported_checks(
    codigo_entidad="072",
    numero_cheque="12345678"
)
print(cheque.head())
```

---

## English

### Description
Access to information about reported checks published by the BCRA, including the list of issuing banks and reported checks.

### Available Methods

#### `get_banks()`
Gets the list of issuing banks.

**Returns:**
- `pandas.DataFrame`: DataFrame with the banks

**Example:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
banks = client.get_banks()
print(banks.head())
```

#### `get_reported_checks(codigo_entidad, numero_cheque)`
Gets information about a specific reported check.

**Parameters:**
- `codigo_entidad` (str): Code of the issuing bank
- `numero_cheque` (str): Check number

**Returns:**
- `pandas.DataFrame`: DataFrame with the reported check information

**Example:**
```python
from pyBCRAdata import BCRAclient

client = BCRAclient()
check = client.get_reported_checks(
    codigo_entidad="072",
    numero_cheque="12345678"
)
print(check.head())
```
