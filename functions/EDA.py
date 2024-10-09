import pandas as pd

def get_file(name_file):
    '''
    Recibe el nombre del archivo (sin la extensión) y lo busca en la carpeta src respectiva al formato.
    Retorna un DataFrame con los datos del archivo previamente procesado.
    Si el archivo no se encuentra, intenta cargarlo como CSV.
    '''
    try:
        file = pd.read_parquet('..\data\Parquet\{name_file}.parquet')
        return file
    except FileNotFoundError:
        file = pd.read_csv(f'..\src\CSV\{name_file}.csv')
        return file
    return None