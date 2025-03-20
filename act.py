import pandas as pd
import numpy as np

class DataProcessor:
    @staticmethod
    def carga_de_archivo(file_path):
        """
        Carga archivos con extensión .csv o .html y los convierte en un DataFrame.
        Si el archivo tiene otra extensión, lanza un error con el mensaje correspondiente.
        """
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.html'):
            return pd.read_html(file_path)[0]
        else:
            raise ValueError(f"Hola, acabas de ingresar un documento que desconozco, con extensión: {file_path.split('.')[-1]}")

    @staticmethod
    def sustitucion_valores_nulos(df):
        """
        Sustituye los valores nulos de:
        - Columnas con índice de número primo por '1111111'
        - Otras columnas numéricas por '1000001'
        - Columnas no numéricas por 'Valor Nulo'
        """
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return False
            return True
        
        for idx, col in enumerate(df.columns):
            if df[col].dtype in ['int64', 'float64']:
                df[col].fillna(1111111 if is_prime(idx) else 1000001, inplace=True)
            else:
                df[col].fillna("Valor Nulo", inplace=True)
        return df

    @staticmethod
    def identificar_valores_nulos(df):
        """
        Identifica valores nulos por columna y en todo el DataFrame.
        """
        nulls_per_column = df.isnull().sum()
        total_nulls = df.isnull().sum().sum()
        return nulls_per_column, total_nulls

    @staticmethod
    def sustitucion_valores_atipicos(df):
        """
        Identifica valores atípicos en columnas numéricas con el método del rango intercuartílico
        y los sustituye con la leyenda 'Valor Atípico'.
        """
        for col in df.select_dtypes(include=['int64', 'float64']).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df[col] = df[col].apply(lambda x: "Valor Atípico" if x < lower_bound or x > upper_bound else x)
        return df