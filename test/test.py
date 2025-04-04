import pytest
from datetime import datetime, timedelta
import pandas as pd
from pyBCRAdata import BCRAclient

@pytest.fixture
def client():
    """Fixture para crear una instancia del cliente"""
    return BCRAclient()

class TestMonetaryData:
    """Tests para get_monetary_data"""

    def test_valid_params(self, client):
        """Test con parámetros válidos"""
        df = client.get_monetary_data(
            id_variable=1,
            desde="2023-01-01",
            hasta="2023-01-31"
        )
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert "valor" in df.columns

    def test_invalid_date_format(self, client):
        """Test con formato de fecha inválido"""
        with pytest.raises(ValueError, match="Formato de fecha inválido"):
            client.get_monetary_data(
                id_variable=7935,
                desde="01/01/2023"
            )

    def test_debug_mode(self, client):
        """Test modo debug"""
        url = client.get_monetary_data(
            id_variable=7,
            desde="2023-01-01",
            debug=True
        )
        assert isinstance(url, str)
        assert "api.bcra.gob.ar" in url

    def test_json_response(self, client):
        """Test respuesta en formato JSON"""
        response = client.get_monetary_data(
            id_variable=7,
            desde="2023-01-01",
            json=True
        )
        assert isinstance(response, dict)
        assert "results" in response

class TestCurrencyData:
    """Tests para endpoints de divisas"""

    def test_currency_master(self, client):
        """Test maestro de divisas"""
        df = client.get_currency_master()
        assert isinstance(df, pd.DataFrame)
        assert "codigo" in df.columns  # Cambiado de 'moneda' a 'codigo'
        assert "denominacion" in df.columns

    def test_currency_quotes(self, client):
        """Test cotizaciones"""
        df = client.get_currency_quotes()
        assert isinstance(df, pd.DataFrame)

    def test_currency_timeseries(self, client):
        """Test series temporales"""
        # Usar fechas fijas en lugar de dinámicas para mayor consistencia
        df = client.get_currency_timeseries(
            moneda="USD",
            fechadesde="2023-01-01",
            fechahasta="2023-01-31"
        )
        assert isinstance(df, pd.DataFrame)
        assert not df.empty, "El DataFrame no debería estar vacío"
        assert "fecha" in df.columns

class TestChecksData:
    """Tests para endpoints de cheques"""

    def test_checks_master(self, client):
        """Test maestro de entidades"""
        df = client.get_checks_master()
        assert isinstance(df, pd.DataFrame)
        assert "codigoEntidad" in df.columns

    def test_checks_reported(self, client):
        """Test cheques denunciados"""
        df = client.get_checks_reported(
            codigo_entidad=11,
            numero_cheque=203775991
        )
        assert isinstance(df, pd.DataFrame)

    def test_missing_required_args(self, client):
        """Test argumentos requeridos faltantes"""
        with pytest.raises(ValueError, match="Faltan argumentos requeridos"):
            client.get_checks_reported(codigo_entidad=11)

class TestErrorHandling:
    """Tests de manejo de errores"""

    def test_invalid_params(self, client):
        """Test parámetros inválidos"""
        with pytest.raises(ValueError, match="Parámetros inválidos"):
            client.get_monetary_data(parametro_invalido=123)

    def test_invalid_entity_code(self, client):
        """Test código de entidad inválido"""
        df = client.get_checks_reported(
            codigo_entidad=999999,  # código inválido
            numero_cheque=123
        )
        assert df.empty

    def test_ssl_verification(self):
        """Test verificación SSL desactivada"""
        client = BCRAclient(verify_ssl=False)
        df = client.get_monetary_data(id_variable=7935)
        assert isinstance(df, pd.DataFrame)

class TestHelperMethods:
    """Tests para métodos auxiliares"""

    def test_url_building(self, client):
        """Test construcción de URLs"""
        url = client.get_monetary_data(
            id_variable=7935,
            debug=True
        )
        assert "estadisticas/v3.0/monetarias" in url

    def test_data_types(self, client):
        """Test tipos de datos"""
        df = client.get_monetary_data(id_variable=7935)
        assert df['valor'].dtype == 'float64'
        if 'fecha' in df.columns:
            assert pd.api.types.is_datetime64_any_dtype(df['fecha'])
