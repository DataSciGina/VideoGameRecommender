import pandas as pd
import numpy as np
import gzip
import ast
from pandas import json_normalize
import os

def load_data(file_path: str):
    '''
    Carga el DataSet desde un archivo gzip y lo retorna como un DataFrame de Pandas.
    '''
    arr = np.array([]) # se crea array de numpy

    # Se abre el archivo gzip y se lee línea por línea
    with gzip.open(file_path, 'rt', encoding='utf8') as file:
        # Se intenta convertir cada línea en un diccionario y agregarlo al array
        try:
            for line in file.readlines():
                arr = np.append(arr, ast.literal_eval(line))
        
        except ValueError:
            # Se intenta leer el archivo como un JSON y agregarlo al array
            arr = pd.read_json(file_path, lines=True)
            return arr
        except Exception as e:
            print(f'Error al cargar los datos: {e}')
            return None
        
    df = pd.DataFrame(arr)
    df  = pd.json_normalize(df[0])
    return df

def normalize(df, col: str):
    '''
    Recibe un DataFrame de Pandas y el nombre de la columna a expandir y normalizar de dicho DataFrame.
    Devuelve un DataFrame normalizado con la columna expandida.
    '''
    
    # Expande la columna y resetea el índice para que los valores de la columna sean filas independientes
    df_exp = df.explode(col)
    df_exp.reset_index(drop=True, inplace=True)
    
    # Expande la columna normalizada y concatena el DataFrame original con la expandida
    df_normalized = json_normalize(df_exp[col])
    res = pd.concat([df_exp.drop(columns=[col]), df_normalized], axis=1)
    
    return res

def export(df, project_root, file):
    '''
    Recibe un DataFrame de Pandas y la dirección del repositorio, y lo exporta como un archivo CSV en la ruta ./VideoGameRecommender/src/CSV, 
    y como un archivo Parquet en ./VideoGameRecommender/src/Parquet.
    '''
    
    file_path = os.path.join(project_root, 'src')
    csv_path = os.path.join(file_path, 'CSV')
    parquet_path = os.path.join(file_path, 'Parquet')

    # Crea los directorios si no existen
    if not os.path.exists(csv_path):
        print(f'Creando el directorio {csv_path}...')
        os.makedirs(csv_path, exist_ok=True)

    if not os.path.exists(parquet_path):
        print(f'Creando el directorio {parquet_path}...')
        os.makedirs(parquet_path, exist_ok=True)
    
    # Exportar a CSV
    df.to_csv(os.path.join(csv_path, f'{file}.csv'), index=False)
    
    # Exportar a Parquet
    df.to_parquet(os.path.join(parquet_path, f'{file}.parquet'), index=False)
    
    print('Archivos exportados exitosamente.')