from typing import Any, Dict, List, Union
import pandas as pd
import numpy as np
from ..config.settings import DataFormat

class DataFrameTransformer:
    """Clase para transformar datos de la API en DataFrames."""
    @staticmethod
    def transform(data: Any, data_format: DataFormat) -> pd.DataFrame:
        """Transforma datos según el formato especificado."""
        transformers = {
            DataFormat.CHECKS: DataFrameTransformer._transform_checks,
            DataFormat.CURRENCY: DataFrameTransformer._transform_currency,
            DataFormat.TIMESERIES: DataFrameTransformer._transform_timeseries,
            DataFormat.DEBTS: DataFrameTransformer._transform_debts,
            DataFormat.REJECTED_CHECKS: DataFrameTransformer._transform_rejected_checks,
            DataFormat.DEFAULT: lambda x: pd.DataFrame(x)
        }

        # Obtener el transformador adecuado o usar el por defecto
        transformer = transformers.get(data_format, transformers[DataFormat.DEFAULT])
        return transformer(data)

    @staticmethod
    def _transform_nested_data(
        data: Union[Dict, List],
        common_fields: List[str] = None,
        level1_field: str = None,
        level1_key: str = None,
        level2_field: str = None,
        level2_key: str = None,
        level3_field: str = None,
        extract_common_to_all: bool = True
        ) -> pd.DataFrame:
        """
        Método genérico para transformar datos anidados en DataFrame.

        Parameters:
        -----------
        data: Dict o List - Los datos a transformar
        common_fields: List[str] - Campos comunes a extraer del primer nivel
        level1_field: str - Campo que contiene los items del primer nivel
        level1_key: str - Clave para extraer valor del primer nivel
        level2_field: str - Campo que contiene los items del segundo nivel
        level2_key: str - Clave para extraer valor del segundo nivel
        level3_field: str - Campo que contiene los items del tercer nivel
        extract_common_to_all: bool - Si se deben extraer campos comunes a todas las filas
        """
        if not data:
            return pd.DataFrame()

        # Manejar listas como caso especial para timeseries
        if isinstance(data, list):
            flattened_data = []
            for entry in data:
                if level1_field and level1_field in entry:
                    for item in entry.get(level1_field, []):
                        # Añadir el campo común (fecha) a cada item
                        if level1_key and level1_key in entry:
                            item[level1_key] = entry[level1_key]
                        flattened_data.append(item)
            return pd.DataFrame(flattened_data)

        # Caso de diccionario (resto de formatos)
        common_data = {}
        if common_fields and extract_common_to_all:
            common_data = {field: data.get(field, np.nan) for field in common_fields}

        # Si no hay campo de primer nivel, es un caso simple
        if not level1_field:
            if level2_field and level2_field in data:
                # Caso currency: solo detalle con fecha común
                df = pd.DataFrame(data.get(level2_field, []))
                if not df.empty and level1_key and level1_key in data:
                    df[level1_key] = data[level1_key]
                return df
            return pd.DataFrame([common_data]) if common_data else pd.DataFrame()

        # Si hay campo de primer nivel pero no existe en data, retornar datos comunes
        level1_items = data.get(level1_field, [])
        if not level1_items and common_data:
            return pd.DataFrame([common_data])

        flattened_data = []

        # Procesar el primer nivel
        for item1 in level1_items:
            item1_value = item1.get(level1_key, np.nan) if level1_key else None
            level1_data = {**common_data}
            if level1_key and item1_value is not None:
                level1_data[level1_key] = item1_value

            # Si no hay segundo nivel, añadir datos del primer nivel
            if not level2_field or level2_field not in item1:
                # Para checks, añadir valores por defecto
                if not level2_field and not level2_key and level1_field == 'detalles' and not level1_items:
                    default_values = {'sucursal': np.nan, 'numeroCuenta': np.nan, 'causal': np.nan}
                    flattened_data.append({**level1_data, **default_values})
                else:
                    flattened_data.append(level1_data)
                continue

            # Procesar el segundo nivel
            for item2 in item1.get(level2_field, []):
                if not level2_key:
                    # Si no hay clave específica, usar todo el objeto
                    row = {**level1_data, **item2}
                    flattened_data.append(row)
                    continue

                item2_value = item2.get(level2_key, np.nan)
                level2_data = {**level1_data, level2_key: item2_value}

                # Si no hay tercer nivel, añadir datos del segundo nivel
                if not level3_field or level3_field not in item2:
                    flattened_data.append(level2_data)
                    continue

                # Procesar el tercer nivel
                for item3 in item2.get(level3_field, []):
                    row = {**level2_data, **item3}
                    flattened_data.append(row)

        return pd.DataFrame(flattened_data)

    @staticmethod
    def _transform_checks(data: Dict) -> pd.DataFrame:
        """Transforma datos de cheques en DataFrame."""
        common_fields = ['numeroCheque', 'denunciado', 'fechaProcesamiento', 'denominacionEntidad']
        return DataFrameTransformer._transform_nested_data(
            data=data,
            common_fields=common_fields,
            level1_field='detalles'
        )

    @staticmethod
    def _transform_currency(data: Dict) -> pd.DataFrame:
        """Transforma datos de divisas en DataFrame."""
        return DataFrameTransformer._transform_nested_data(
            data=data,
            level1_key='fecha',
            level2_field='detalle'
        )

    @staticmethod
    def _transform_timeseries(data: List) -> pd.DataFrame:
        """Transforma series temporales en DataFrame."""
        return DataFrameTransformer._transform_nested_data(
            data=data,
            level1_field='detalle',
            level1_key='fecha'
        )

    @staticmethod
    def _transform_debts(data: Dict) -> pd.DataFrame:
        """Transforma datos de deudas en DataFrame."""
        return DataFrameTransformer._transform_nested_data(
            data=data,
            common_fields=['identificacion', 'denominacion'],
            level1_field='periodos',
            level1_key='periodo',
            level2_field='entidades'
        )

    @staticmethod
    def _transform_rejected_checks(data: Dict) -> pd.DataFrame:
        """Transforma datos de cheques rechazados en DataFrame."""
        return DataFrameTransformer._transform_nested_data(
            data=data,
            common_fields=['identificacion', 'denominacion'],
            level1_field='causales',
            level1_key='causal',
            level2_field='entidades',
            level2_key='entidad',
            level3_field='detalle'
        )
