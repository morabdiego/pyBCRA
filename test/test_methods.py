import pytest
from pyBCRAdata import BCRAclient

@pytest.fixture
def client():
    return BCRAclient()

@pytest.fixture(params=[True, False], ids=['debug_on', 'debug_off'])
def debug_mode(request):
    return request.param

def test_monetary_data_urls(client, debug_mode):
    df = client.monetary.series(id_variable=6, debug=debug_mode)
    assert df is not None

def test_monetary_master_urls(client, debug_mode):
    df = client.monetary.variables(debug=debug_mode)
    assert df is not None

def test_monetary_data_with_dates_urls(client, debug_mode):
    df = client.monetary.series(
        id_variable=6,
        desde='2023-01-01',
        hasta='2023-01-31',
        limit=12,
        offset=2,
        debug=debug_mode
    )
    assert df is not None

def test_currency_master_urls(client, debug_mode):
    df = client.currency.currencies(debug=debug_mode)
    assert df is not None

def test_currency_quotes_urls(client, debug_mode):
    df = client.currency.rates(fecha='2023-01-15', debug=debug_mode)
    assert df is not None

def test_currency_timeseries_urls(client, debug_mode):
    df = client.currency.series(
        moneda='USD',
        fechadesde='2023-01-01',
        fechahasta='2023-02-01',
        limit=12,
        offset=2,
        debug=debug_mode
    )
    assert df is not None

def test_debts_urls(client, debug_mode):
    df = client.debtors.debtors(identificacion='23409233449', debug=debug_mode)
    assert df is not None

def test_checks_master_urls(client, debug_mode):
    df = client.checks.banks(debug=debug_mode)
    assert df is not None

def test_checks_reported_urls(client, debug_mode):
    df = client.checks.reported(
        codigo_entidad=11,
        numero_cheque=20377516,
        debug=debug_mode
    )
    assert df is not None

def test_debts_historical_urls(client, debug_mode):
    df = client.debtors.history(identificacion='23409233449', debug=debug_mode)
    assert df is not None

def test_debts_rejected_checks_urls(client, debug_mode):
    df = client.debtors.rejected(identificacion='23409233449', debug=debug_mode)
    assert df is not None

def test_monetary_data_df(client):
    df = client.monetary.series(id_variable=6, debug=False)
    assert not df.empty

def test_monetary_master_df(client):
    df = client.monetary.variables(debug=False)
    assert not df.empty

def test_currency_master_df(client):
    df = client.currency.currencies(debug=False)
    assert not df.empty

def test_currency_quotes_df(client):
    df = client.currency.rates(fecha='2023-01-15', debug=False)
    assert not df.empty

def test_debts_df(client):
    df = client.debtors.debtors(identificacion='23409233449', debug=False)
    assert not df.empty
