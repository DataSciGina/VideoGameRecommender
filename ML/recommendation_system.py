import pandas as pd
import warnings

# Ignorar advertencias
warnings.filterwarnings('ignore')

### Cargar DataSets
try:
    df = pd.read_parquet('src/Parquet/dummies.parquet')
    games = pd.read_parquet('src/Parquet/games.parquet')
except FileNotFoundError:
    df = pd.read_csv('src/CSV/dummies.csv')
    games = pd.read_csv('src/CSV/games.csv')


### Función para obtener recomendaciones
def get_recommendations(item_id: int, model):
    ''' 
    Esta función recibe el id de un juego, la matriz de similitud de coseno, items y la cantidad de juegos que se deseen recomendar y retorna esa cantidad de elementos.
    '''
    # Verifica si el item_id existe en los datos
    if item_id not in df['id'].values:
        raise ValueError(f"Item con id {item_id} no encontrado.")
    
    # Obtiene el índice del ítem en df (no en el df escalado)
    idx = df.index[df['id'] == item_id].tolist()[0]
    
    # Obtiene las similitudes para el ítem especificado
    sim_scores = list(enumerate(model[idx]))
    
    # Ordena los ítems basados en la similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Selecciona los top 5 ítems más similares, omitiendo el primero (el mismo ítem)
    sim_scores = sim_scores[1:6]
    
    # Obtiene los índices de los ítems
    item_indices = [i[0] for i in sim_scores]
    
    # Retorna los ítems recomendados basados en sus IDs originales
    recommended_items = df.iloc[item_indices]['id'].values
    
    return pd.DataFrame(recommended_items, columns=['id'])

### Función para decodificar información de un juego
def decode_game(id):
    # Filtrar el DataFrame por ID
    game = games[games['id'] == id]

    if game.empty:
        return f"No se encontró un juego con el ID {id}"

    # Retorna un diccionario con el nombre y categoría del juego (asumiendo columna 1 = nombre, 2 = categoría)
    return {
        'name': game.iloc[0, 1],
        'category': game.iloc[0, 2]
    }
