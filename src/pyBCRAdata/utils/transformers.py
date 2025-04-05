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
        elif data_format == DataFormat.REJECTED_CHECKS:
            return DataFrameTransformer._transform_rejected_checks(data)
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
        # Lista para almacenar los datos aplanados
        flattened_data = []

        # Si no hay datos, devolver DataFrame vacío
        if not data:
            return pd.DataFrame()

        # Datos base para todas las filas
        common_data = {
            'identificacion': data.get('identificacion', np.nan),
            'denominacion': data.get('denominacion', np.nan)
        }

        # Procesar los períodos y entidades
        periodos = data.get('periodos', [])

        # Si no hay períodos, devolver solo datos comunes
        if not periodos:
            return pd.DataFrame([common_data])

        # Iterar por cada período y entidad
        for periodo in periodos:
            periodo_value = periodo.get('periodo', np.nan)

            # Obtener las entidades del período
            entidades = periodo.get('entidades', [])

            # Si no hay entidades, crear fila con solo período
            if not entidades:
                row = {**common_data, 'periodo': periodo_value}
                flattened_data.append(row)
                continue

            # Procesar cada entidad
            for entidad in entidades:
                # Crear fila combinando datos comunes, período y entidad
                row = {
                    **common_data,
                    'periodo': periodo_value,
                    **entidad
                }
                flattened_data.append(row)

        # Convertir a DataFrame
        return pd.DataFrame(flattened_data)

    @staticmethod
    def _transform_rejected_checks(data: Dict) -> pd.DataFrame:
        """Transforma datos de cheques rechazados en DataFrame."""
        # Lista para almacenar los datos aplanados
        flattened_data = []

        # Si no hay datos, devolver DataFrame vacío
        if not data:
            return pd.DataFrame()

        # Datos base para todas las filas
        common_data = {
            'identificacion': data.get('identificacion', np.nan),
            'denominacion': data.get('denominacion', np.nan)
        }

        # Procesar los causales
        causales = data.get('causales', [])

        # Si no hay causales, devolver solo datos comunes
        if not causales:
            return pd.DataFrame([common_data])

        # Iterar por cada causal
        for causal in causales:
            causal_value = causal.get('causal', np.nan)

            # Obtener las entidades del causal
            entidades = causal.get('entidades', [])

            # Si no hay entidades, crear fila con solo causal
            if not entidades:
                row = {**common_data, 'causal': causal_value}
                flattened_data.append(row)
                continue

            # Procesar cada entidad
            for entidad in entidades:
                entidad_value = entidad.get('entidad', np.nan)

                # Obtener los detalles de la entidad
                detalles = entidad.get('detalle', [])

                # Si no hay detalles, crear fila con solo entidad y causal
                if not detalles:
                    row = {
                        **common_data,
                        'causal': causal_value,
                        'entidad': entidad_value
                    }
                    flattened_data.append(row)
                    continue

                # Procesar cada detalle
                for detalle in detalles:
                    # Crear fila completa
                    row = {
                        **common_data,
                        'causal': causal_value,
                        'entidad': entidad_value,
                        **detalle
                    }
                    flattened_data.append(row)

        # Convertir a DataFrame
        return pd.DataFrame(flattened_data)
