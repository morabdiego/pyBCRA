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
    def _extract_results(data: Dict) -> Any:
        """Extrae el campo 'results' de la respuesta si existe."""
        if isinstance(data, dict) and 'results' in data:
            return data['results']
        return data

    @staticmethod
    def _transform_nested_data(
        data: Union[Dict, List],
        schema_config: Dict = None
        ) -> pd.DataFrame:
        """
        Método genérico optimizado para transformar datos anidados en DataFrame
        según la configuración de schema.

        Parameters:
        -----------
        data: Dict o List - Los datos a transformar
        schema_config: Dict - Configuración de transformación basada en el schema
            {
                'common_fields': Lista de campos comunes a extraer,
                'levels': [
                    {
                        'field': Nombre del campo que contiene los items,
                        'key': Clave para identificar el valor del nivel
                    },
                    ...
                ]
            }
        """
        # Si no hay datos, retornar DataFrame vacío
        if not data:
            return pd.DataFrame()

        # Extraer 'results' si es necesario (muchas APIs lo tienen como contenedor principal)
        data = DataFrameTransformer._extract_results(data)

        # Si no hay configuración de schema, retornar DataFrame simple
        if not schema_config:
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return pd.DataFrame(data)
            elif isinstance(data, dict):
                return pd.DataFrame([data])
            return pd.DataFrame()

        # Lista simple
        if isinstance(data, list) and all(isinstance(item, dict) for item in data) and not schema_config.get('levels'):
            return pd.DataFrame(data)

        # Inicializar datos
        common_fields = schema_config.get('common_fields', [])
        levels = schema_config.get('levels', [])

        # Manejar respuesta plana (sin niveles)
        if isinstance(data, dict) and not levels:
            if common_fields:
                root_data = {field: data.get(field) for field in common_fields if field in data}
                return pd.DataFrame([root_data]) if root_data else pd.DataFrame()
            return pd.DataFrame([data])

        # Manejar caso de un solo nivel (como cotizaciones)
        if isinstance(data, dict) and len(levels) == 1 and levels[0]['field'] in data:
            level_field = levels[0]['field']
            level_key = levels[0].get('key')

            df = pd.DataFrame(data.get(level_field, []))
            if not df.empty and level_key and level_key in data:
                df[level_key] = data[level_key]
            return df

        # Procesar datos para estructura de series de tiempo
        if isinstance(data, list) and len(levels) == 1:
            level_field = levels[0]['field']
            level_key = levels[0].get('key')

            rows = []
            for entry in data:
                if level_field not in entry:
                    continue

                for detail in entry.get(level_field, []):
                    row = dict(detail)
                    if level_key and level_key in entry:
                        row[level_key] = entry[level_key]
                    rows.append(row)
            return pd.DataFrame(rows)

        # Procesar estructuras jerárquicas multinivel
        if isinstance(data, dict):
            # Extraer campos comunes
            root_data = {}
            if common_fields:
                root_data = {field: data.get(field) for field in common_fields if field in data}

            # Verificar primer nivel
            if not levels or levels[0]['field'] not in data:
                return pd.DataFrame([root_data]) if root_data else pd.DataFrame()

            # Procesar niveles jerárquicos
            rows = []
            current_data = data

            # Función recursiva para procesar niveles
            def process_level(level_idx, parent_data, accumulated_data):
                if level_idx >= len(levels):
                    # Hemos llegado al final de los niveles, agregar datos acumulados
                    rows.append({**accumulated_data, **{k: v for k, v in parent_data.items()
                                                       if k != levels[level_idx-1]['field']}})
                    return

                level_config = levels[level_idx]
                level_field = level_config['field']
                level_key = level_config.get('key')

                if level_field not in parent_data:
                    # Si no hay campo de nivel, agregar datos actuales
                    rows.append(accumulated_data)
                    return

                for item in parent_data.get(level_field, []):
                    new_data = {**accumulated_data}

                    # Agregar clave del nivel si existe
                    if level_key and level_key in item:
                        new_data[level_key] = item[level_key]

                    # Verificar si hay siguiente nivel
                    if level_idx + 1 < len(levels) and levels[level_idx + 1]['field'] in item:
                        process_level(level_idx + 1, item, new_data)
                    else:
                        # Último nivel o no hay más niveles anidados
                        item_data = {k: v for k, v in item.items() if k != level_field}
                        rows.append({**new_data, **item_data})

            # Iniciar procesamiento recursivo con el primer nivel
            process_level(0, current_data, root_data)
            return pd.DataFrame(rows)

        # Fallback: retornar DataFrame con datos originales
        return pd.DataFrame([data]) if isinstance(data, dict) else pd.DataFrame(data)

    @staticmethod
    def _transform_checks(data: Dict) -> pd.DataFrame:
        """Transforma datos de cheques en DataFrame."""
        schema_config = {
            'common_fields': ['numeroCheque', 'denunciado', 'fechaProcesamiento', 'denominacionEntidad'],
            'levels': [
                {'field': 'detalles'}
            ]
        }
        return DataFrameTransformer._transform_nested_data(data, schema_config)

    @staticmethod
    def _transform_currency(data: Dict) -> pd.DataFrame:
        """Transforma datos de divisas en DataFrame."""
        schema_config = {
            'levels': [
                {'field': 'detalle', 'key': 'fecha'}
            ]
        }
        return DataFrameTransformer._transform_nested_data(data, schema_config)

    @staticmethod
    def _transform_timeseries(data: List) -> pd.DataFrame:
        """Transforma series temporales en DataFrame."""
        schema_config = {
            'levels': [
                {'field': 'detalle', 'key': 'fecha'}
            ]
        }
        return DataFrameTransformer._transform_nested_data(data, schema_config)

    @staticmethod
    def _transform_debts(data: Dict) -> pd.DataFrame:
        """Transforma datos de deudas en DataFrame."""
        schema_config = {
            'common_fields': ['identificacion', 'denominacion'],
            'levels': [
                {'field': 'periodos', 'key': 'periodo'},
                {'field': 'entidades'}
            ]
        }
        return DataFrameTransformer._transform_nested_data(data, schema_config)

    @staticmethod
    def _transform_rejected_checks(data: Dict) -> pd.DataFrame:
        """Transforma datos de cheques rechazados en DataFrame."""
        schema_config = {
            'common_fields': ['identificacion', 'denominacion'],
            'levels': [
                {'field': 'causales', 'key': 'causal'},
                {'field': 'entidades', 'key': 'entidad'},
                {'field': 'detalle'}
            ]
        }
        return DataFrameTransformer._transform_nested_data(data, schema_config)
