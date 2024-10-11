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

def get_frequency(dfr, elem, control=None):
    '''
    Recibe un DataFrame, el nombre de la columna sobre la cual sacar la frecuencia y el nombre de una columna de control para usar de referencia si se hizo un explode.
    Retorna un DataFrame con los elementos únicos, la cantidad de veces que aparece y el porcentaje de estos respecto al total de valores en el DataFrame.
    '''
    # si existe una columna de control se aislan las columnas y se eliminan los duplicados
    if control is not None:
        df = dfr[[control, elem]].drop_duplicates()
    else:
        # si no existe una columna de control, se aisla la columna necesaria
        df = dfr[[elem]]

    # se calcula la frecuencia
    freq = df[elem].value_counts().reset_index()
    freq.columns = [elem, 'frequency']

    # se calcula el porcentaje
    freq['percentage'] = (freq['frequency'] / freq['frequency'].sum()) * 100

    return freq