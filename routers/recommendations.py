from fastapi import APIRouter, HTTPException
from src.colaborative import get_user_recommendations
from src.utils import load_data
from src.matrix_builder import build_user_item_matrix
from src.popularity import get_popular_movies
from src.content import prepare_content_based, get_similar_movies
from src.hybrid import get_hybrid_recommendations

router = APIRouter()

movies, ratings, tags = load_data()
matrix = build_user_item_matrix(ratings)
tfidf_matrix, movie_indices, movies_df_content = prepare_content_based(movies, tags)

@router.get("/recommend/content/{movie_id}")
def recommend_by_content(movie_id: int, top_n: int = 10):
    try:
        recs = get_similar_movies(movie_id, movies_df_content, tfidf_matrix, movie_indices, top_n=top_n)
        return recs.to_dict(orient='records')
    except Exception:
        raise HTTPException(status_code=404, detail="Movie not found")

@router.get("/recommend/hybrid/{user_id}")
def recommend_hybrid(user_id: int, top_n: int = 10):
    if user_id not in matrix.index:
        raise HTTPException(status_code=404, detail="User not found")
    recs = get_hybrid_recommendations(user_id, movies, ratings, matrix, movies_df_content, tfidf_matrix, movie_indices, top_n=top_n)
    return recs.to_dict(orient='records')

@router.get("/recommend/{user_id}")
def recommend(user_id: int):
    if user_id not in matrix.index:
        raise HTTPException(status_code=404, detail="User not found")
    recs = get_user_recommendations(user_id, matrix, movies, top_n=10)
    return recs.to_dict(orient='records')

@router.get("/populares")
def populares():
    return get_popular_movies(movies, ratings, top_n=10)