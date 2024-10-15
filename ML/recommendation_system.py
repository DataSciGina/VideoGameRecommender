import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import os
import sys

# Ignorar advertencias
warnings.filterwarnings('ignore')

### Cargar DataSets

# Se importa el dataset
try:
    df = pd.read_parquet('data\Parquet\dummies.parquet')
    games = pd.read_parquet('data\Parquet\games.parquet')
except FileNotFoundError:
    df = pd.read_csv(f'src\CSV\dummies.csv')
    games = pd.read_csv(f'src\CSV\games.csv')

## Escalar Datos

# Inicializar escalador
scaler = StandardScaler()

# se escala la data en otro df
scaled_data = scaler.fit_transform(df)
scaled_df = pd.DataFrame(scaled_data)

# calcular matriz de similitud
matrix = cosine_similarity(scaled_df)

def get_recommendations(item_id, similarity_matrix=matrix, items=df, top_n=5):
    ''' 
    Esta función recibe el id de un juego, la matriz de similitud de coseno, items y la cantidad de juegos que se deseen recomendar y retorna esa cantidad de elementos.
    '''
    # Obtiene el índice del ítem
    idx = items.index[items['id'] == item_id].tolist()[0]
    
    # Obtiene las similitudes para el ítem especificado
    sim_scores = list(enumerate(similarity_matrix[idx]))
    
    # Ordena los ítems basados en la similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Selecciona los top_n ítems más similares
    sim_scores = sim_scores[1:top_n + 1]  # Omite el primer elemento (el mismo ítem)
    
    # Obtiene los índices de los ítems
    item_indices = [i[0] for i in sim_scores]
    
    # Retorna los ítems recomendados
    return pd.DataFrame(items.iloc[item_indices]['id'])

def decode_game(id):
    # Filtrar el DataFrame por ID
    game = games[games['id'] == id]

    if game.empty:
        return f"No se encontró un juego con el ID {id}"

    # seleccionar solo una de las copias de id
    res = game.iloc[0, 1] + " (" + game.iloc[0, 2] + ")"

    return dict(res)

def matrix():
    '''
    retorna la matríz de correlación
    '''
    return matrix