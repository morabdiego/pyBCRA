from typing import Any, Dict, List
import pandas as pd
import numpy as np
from ..config.settings import DataFormat

class DataFrameTransformer:
    """Clase para transformar datos de la API en DataFrames."""
    @staticmethod
    def transform(data: Any, data_format: DataFormat) -> pd.DataFrame:
        """Transforma datos según el formato especificado."""
        if data_format == DataFormat.CHECKS:
            return DataFrameTransformer._transform_checks(data)
        elif data_format == DataFormat.CURRENCY:
            return DataFrameTransformer._transform_currency(data)
        elif data_format == DataFormat.TIMESERIES:
            return DataFrameTransformer._transform_timeseries(data)
        elif data_format == DataFormat.DEBTS:
            return DataFrameTransformer._transform_debts(data)
        elif data_format == DataFormat.DEFAULT:
            return pd.DataFrame(data)
        else:
            return pd.DataFrame(data)

    @staticmethod
    def _transform_checks(data: Dict) -> pd.DataFrame:
        """Transforma datos de cheques en DataFrame."""
        base_data = {
            'numeroCheque': data['numeroCheque'],
            'denunciado': data['denunciado'],
            'fechaProcesamiento': data['fechaProcesamiento'],
            'denominacionEntidad': data['denominacionEntidad']
        }
        if not data['detalles']:
            return pd.DataFrame([{
                **base_data,
                'sucursal': np.nan,
                'numeroCuenta': np.nan,
                'causal': np.nan
            }])
        rows = [{**base_data, **detalle} for detalle in data['detalles']]
        return pd.DataFrame(rows)

    @staticmethod
    def _transform_currency(data: Dict) -> pd.DataFrame:
        """Transforma datos de divisas en DataFrame."""
        df = pd.DataFrame(data.get('detalle', []))
        if not df.empty:
            df['fecha'] = data.get('fecha')
        return df

    @staticmethod
    def _transform_timeseries(data: List) -> pd.DataFrame:
        """Transforma series temporales en DataFrame."""
        flattened_data = [
            {**detalle, 'fecha': entry['fecha']}
            for entry in data
            for detalle in entry.get('detalle', [])
        ]
        return pd.DataFrame(flattened_data)

    @staticmethod
    def _transform_debts(data: Dict) -> pd.DataFrame:
        """Transforma datos de deudas en DataFrame."""
        flattened_data = []
        results = data.get('results', {})

        # Datos comunes para todas las filas
        common_data = {
            'identificacion': results.get('identificacion'),
            'denominacion': results.get('denominacion')
        }

        # Iterar a través de los periodos y entidades
        for periodo in results.get('periodos', []):
            for entidad in periodo.get('entidades', []):
                # Combinar datos comunes con periodo y entidad
                row = {
                    **common_data,
                    'periodo': periodo.get('periodo'),
                    **entidad  # Incluir todos los campos de la entidad automáticamente
                }
                flattened_data.append(row)

        return pd.DataFrame(flattened_data)
