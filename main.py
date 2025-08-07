from fastapi import FastAPI
from src.colaborative import get_user_recommendations
from src.utils import load_data
from src.matrix_builder import build_user_item_matrix
from src.popularity import get_popular_movies
from fastapi.exceptions import HTTPException

app = FastAPI()

movies, ratings = load_data()
matrix = build_user_item_matrix(ratings)

@app.get("/")
def home():
    return {"mensaje": "API de recomendación de películas"}

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