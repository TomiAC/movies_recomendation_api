from fastapi import FastAPI
from src.colaborative import get_user_recommendations
from src.utils import load_data
from src.matrix_builder import build_user_item_matrix
from src.popularity import get_popular_movies
from src.content import prepare_content_based, get_similar_movies
from fastapi.exceptions import HTTPException

app = FastAPI()

movies, ratings, tags = load_data()
matrix = build_user_item_matrix(ratings)
tfidf_matrix, movie_indices, movies_df_content = prepare_content_based(movies, tags)

@app.get("/")
def home():
    return {"mensaje": "API de recomendación de películas"}

@app.get("/recommend/content/{movie_id}")
def recommend_by_content(movie_id: int, top_n: int = 10):
    try:
        recs = get_similar_movies(movie_id, movies_df_content, tfidf_matrix, movie_indices, top_n=top_n)
        return recs.to_dict(orient='records')
    except Exception:
        raise HTTPException(status_code=404, detail="Movie not found")

@app.get("/recommend/{user_id}")
def recommend(user_id: int):
    if user_id not in matrix.index:
        raise HTTPException(status_code=404, detail="User not found")
    recs = get_user_recommendations(user_id, matrix, movies)
    return recs.to_dict(orient='records')

@app.get("recomendacion/nuevo_usuario/{user_id}")
def recomendacion_nuevo_usuario(user_id: int):
    return {"mensaje": f"Recomendaciones para el usuario {user_id}"}

@app.get("/populares")
def populares():
    return get_popular_movies(movies, ratings, top_n=10)