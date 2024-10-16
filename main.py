##################### se importan librerías
from fastapi import FastAPI
import uvicorn
import pandas as pd
from ML.recommendation_system import get_recommendations, decode_game

###################### se crea la instancia de la matríz

# se crea una instancia de FastAPI y se personaliza
app = FastAPI()
app.title = "API de Sistema de Recomendaciones de Steam"

# se crea una función para importar los archivos y manejar los errores
def load_data():
    try:
        df = pd.read_parquet(r'\src\Parquet\games.parquet')
        users = pd.read_parquet(r'\src\Parquet\user_items.parquet')
        reviews = pd.read_parquet(r'\src\Parquet\user_reviews_sentiment_analysis.parquet')
    #except FileNotFoundError as e:
    #    print("Archivo no encontrado. Intentando cargar archivos CSV...")
    #    try:
    #        df = pd.read_csv(f'.\src\CSV\games.csv')
    #        users = pd.read_csv(r'.\src\CSV\user_items.csv')
    #        reviews = pd.read_csv(r'.\src\CSV\user_reviews_sentiment_analysis.csv')
    #    except Exception as e:
    #        print(f"Error al cargar los datos desde CSV: {e}")
    #        return None, None, None
    except Exception as e:
        print(f"Error al cargar los datos desde parquet: {e}")
        return None, None, None
    return df, users, reviews



# se ejecuta la función load_data almacenando los resultados en los distintos dfs
df, users, reviews = load_data()

# Verificar si los DataFrames han sido cargados
if df is not None and users is not None and reviews is not None:
    # se obtienen juegos únicos
    unique_games = df.drop_duplicates(subset='id')

    # se obtienen los géneros únicos
    unique_genres = df.drop_duplicates(subset=['genres'])

    #convertir los tipos de datos de ser necesario
    users['item_id'] = users['item_id'].astype(int)  # Convertir item_id a int
    reviews['item_id'] = reviews['item_id'].astype(int)  # Convertir item_id a int
    # Unir users con juegos (df) asegurándote de que no haya duplicación de la columna id
    user_games = users.merge(unique_games[['id', 'price']], 
                            left_on='item_id', 
                            right_on='id', 
                            how='left').drop(columns=['id'])

    # Unir el resultado anterior con reviews
    user_games = user_games.merge(reviews[['user_id', 'item_id', 'recommend']], 
                                left_on=['user_id', 'item_id'], 
                                right_on=['user_id', 'item_id'], 
                                how='left')

###################### funciones

# Ruta raíz ("/")
@app.get("/")
async def root():
    '''
    Bienvenido a la API de Juegos, Usuarios y Recomendaciones de Steam
    '''
    return {
        "message": "API de Desarrolladores de Videojuegos. Accede a otros endpoints.",
        "endpoints": {
            "/": "Información general",
            "/developer/{desarrollador}": "Informe sobre los juegos de un desarrollador. Ingresar el desarrollador en minúscula y sin espacios.",
            "/userdata/{user_id}": "Información sobre los datos de un usuario",
            "/UserForGenre/{genre}": "Recibe un género y devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.",
            "/best_developer_year/{year}": "Recibe un año y devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos)",
            "/developer_reviews_analysis/{developer}": "Recibe un desarrollador y devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo."
        }}

@app.get("/developer/{desarrollador}")
async def developer(desarrollador: str):
    '''
    Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.
    '''
    # Filtrar por la empresa desarrolladora proporcionada
    developer_games = df[df['developer'] == desarrollador]
    
    if developer_games.empty:
        return {"error": "No se encontraron datos para el desarrollador proporcionado"}
    
    developer_games.drop_duplicates(subset=['id'], inplace=True)

    # Agrupar por año y calcular la cantidad de items y el porcentaje de juegos gratuitos
    developer_summary = developer_games.groupby('release_year').agg(
        total_items=('app_name', 'count'),
        free_content_percentage=('price', lambda x: (x == 0).mean() * 100)
    ).reset_index()

    # Convertir el DataFrame a un diccionario para devolverlo como respuesta JSON
    result = developer_summary.to_dict(orient='records')

    return {"desarrollador": desarrollador, "datos_por_año": result}

@app.get("/userdata/{user_id}")
async def userdata(user_id: str):
    '''
    Recibe el id del usuario y devuelve la cantidad de dinero gastado por este, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.
    '''
    # Filtrar el DataFrame para obtener solo los datos del usuario con el user_id dado
    user_data = user_games[user_games['user_id'] == user_id]
    
    # Verificar si el usuario tiene registros
    if user_data.empty:
        return {"error": "Usuario no encontrado"}
    
    # Calcular la cantidad de dinero gastado
    total_spent = user_data['price'].sum()
    
    # Calcular el porcentaje de recomendación
    total_reviews = user_data['recommend'].notna().sum()  # Total de reviews válidos (no NaN)
    positive_reviews = user_data['recommend'].sum()  # Total de recomendaciones positivas (asumiendo 1 = recomendado)
    recommend_percentage = (positive_reviews / total_reviews) * 100 if total_reviews > 0 else 0
    
    # Calcular la cantidad de items
    items_count = user_data['item_id'].nunique()
    
    # Devolver la respuesta en formato JSON
    return {
        "user_id": user_id,
        "total_spent": total_spent,
        "recommendation_percentage": recommend_percentage,
        "items_count": items_count
    }

@app.get("/UserForGenre/{genre}")
async def UserForGenre(genre: str):
    '''
    Recibe un género y devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.
    '''
    # Filtrar los juegos por el género dado y eliminar duplicados de id
    games_genre=df[df['genres'] == genre]
    games_genre = games_genre.drop_duplicates('id')

    # asegurarse que existan juegos con dicho género
    if games_genre.empty:
        return {"error": f"No hay juegos con el género '{genre}'"}

    # filtrar entre los usuarios que hayan jugado juegos del género pedido y sumar el tiempo de juego
    users_genres = users[users['item_id'].isin(games_genre['id'])]

    # verificar que haya jugadores que hayan jugado al género
    if users_genres.empty:
        return {"error": f"No hay usuarios que hayan jugado juegos con el género '{genre}'"}
    
    # agrupar por usuario y sumar el tiempo de juego
    users_playtime = users_genres.groupby('user_id')['playtime_forever'].sum()

    # buscar al usuario con más horas jugadas
    top_user = users_playtime.idxmax()

    # obtener los juegos del usuario con más horas jugadas
    users_genres = users_genres[users_genres['user_id'] == top_user].merge(games_genre[['id', 'release_year']], left_on='item_id', right_on='id')

    # agrupar por release_year y sumar las horas jugadas
    year_playtime = users_genres.groupby('release_year')['playtime_forever'].sum().reset_index()

    # convertir la lista de horas jugadas a diccionario
    result = year_playtime.to_dict(orient='records')

    return {
        f"Usuario con más horas jugadas en el género {genre}:": top_user,
        "Horas jugadas:": result
    }

@app.get("/best_developer_year/{year}")
async def best_developer_year(year: int):
    '''
    Recibe un año y devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos)
    '''
    # filtrar los juegos lanzados en el año dado
    games_year = unique_games[unique_games['release_year'] == year]
    
    # verificar que haya juegos lanzados en el año dado
    if games_year.empty:
        return {"error": f"No se encontraron juegos lanzados en el año {year}"}

    # Agrupar por desarrollador y sumar tanto las recomendaciones positivas como los comentarios positivos
    developer_reviews = games_year.groupby('developer').agg({
        'recommend_pos': 'sum', 
        'review_pos': 'sum'
    })

    # Asegurarse de que existan recomendaciones
    if developer_reviews.empty:
        return {"error": f"No se encontraron recomendaciones para juegos del año {year}"}

    # Ordenar los desarrolladores por número de recomendaciones positivas y obtener el top 3
    top_3_developers = developer_reviews.sort_values('recommend_pos', ascending=False).head(3)

    # Convertir el resultado al formato deseado (nombre del developer con lista de comentarios negativos y positivos)
    top_3_list = {
        developer: {"Comentarios positivos": row['review_pos'], "Recomendaciones positivas": row['recommend_pos']}
        for developer, row in top_3_developers.iterrows()
    }

    # Retornar el top 3 de desarrolladores
    return {
        "year": year,
        "top_3_developers": top_3_list
    }

@app.get("/developer_reviews_analysis/{developer}")
async def developer_reviews_analysis(developer: str):
    '''
    Recibe un desarrollador y devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.
    '''
    # filtrar los juegos lanzados por el desarrollador dado
    games_year = unique_games[unique_games['developer'] == developer]
    
    # verificar que haya juegos lanzados por el desarrollador dado
    if games_year.empty:
        return {"error": f"No se encontraron juegos lanzados por el desarrollador {developer}"}

    # Agrupar por desarrollador y sumar tanto las recomendaciones positivas como las negativas
    developer_reviews = games_year.groupby('developer').agg({
        'review_neg': 'sum',
        'review_pos': 'sum'
    })

    # Asegurarse de que existan recomendaciones
    if developer_reviews.empty:
        return {"error": f"No se encontraron recomendaciones para juegos del desarrollador {developer}"}

    # Convertir el resultado al formato deseado (nombre del developer como clave, cantidad de comentarios negativos, neutrales y positivos, y cantidad de recomendaciones positivas y negativas) y retornar
    return {
        developer: [{"Negative": developer_reviews['review_neg'], "Positive": developer_reviews['review_pos']}]
    }

@app.get("/recomendacion_juego/{game}")
async def recomendacion_juego(id: int):
    '''
    Recibe el ID de un juego y retorna cinco juegos recomendados similares.
    '''
    # Filtrar los juegos similares al dado
    ids = get_recommendations(id)

    # traer nombres
    games = ids['id'].apply(decode_game)
    return games


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)