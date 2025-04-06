from typing import Any, Dict, List, Union
import pandas as pd
import numpy as np

class DataFrameTransformer:
    """Clase para transformar datos de la API en DataFrames."""

    @staticmethod
    def transform(data: Any) -> pd.DataFrame:
        """Transforma datos JSON en DataFrame."""
        # Extraer results si existe
        if isinstance(data, dict) and 'results' in data:
            data = data['results']

        # Si no hay datos, retornar DataFrame vacío
        if not data:
            return pd.DataFrame()

        # Transformar datos usando el enfoque minimalista
        return DataFrameTransformer.__json_to_df(data)

    @staticmethod
    def __flatten_dict(d: dict, parent_key: str = '', sep: str = '_') -> dict:
        """Aplana un diccionario anidado en un diccionario plano."""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k

            if isinstance(v, dict):
                items.extend(DataFrameTransformer.__flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list) and all(isinstance(item, dict) for item in v):
                # Si la lista contiene diccionarios, procesar cada uno
                for i, item in enumerate(v):
                    items.extend(DataFrameTransformer.__flatten_dict(
                        item, f"{new_key}{sep}{i}", sep=sep).items())
            else:
                items.append((new_key, v))

        return dict(items)

    @staticmethod
    def __json_to_df(json_data: Union[Dict, List]) -> pd.DataFrame:
        """Convierte datos JSON en un DataFrame mediante aplanamiento."""
        if isinstance(json_data, dict):
            flattened_dict = DataFrameTransformer.__flatten_dict(json_data)
            return pd.DataFrame([flattened_dict])
        elif isinstance(json_data, list):
            if all(isinstance(item, dict) for item in json_data):
                flattened_list = [DataFrameTransformer.__flatten_dict(item) for item in json_data]
                return pd.DataFrame(flattened_list)
            else:
                # Lista de valores simples
                return pd.DataFrame(json_data)
        else:
            # Fallback para otros tipos de datos
            return pd.DataFrame([json_data]) if json_data is not None else pd.DataFrame()
