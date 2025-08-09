import logging
from fastapi import APIRouter, HTTPException, Depends
from src.colaborative import get_user_recommendations
from src.utils import load_data
from src.matrix_builder import build_user_item_matrix
from src.popularity import get_popular_movies
from src.content import prepare_content_based, get_similar_movies
from src.hybrid import get_hybrid_recommendations
from .auth import get_current_user, User

logger = logging.getLogger(__name__)

router = APIRouter()

movies, ratings, tags = load_data()
matrix = build_user_item_matrix(ratings)
tfidf_matrix, movie_indices, movies_df_content = prepare_content_based(movies, tags)

@router.get("/recommend/content/{movie_id}")
def recommend_by_content(movie_id: int, top_n: int = 10, current_user: User = Depends(get_current_user)):
    logger.info(f"Content recommendation request for movie_id: {movie_id}, top_n: {top_n}")
    try:
        recs = get_similar_movies(movie_id, movies_df_content, tfidf_matrix, movie_indices, top_n=top_n)
        logger.info(f"Content recommendations generated for movie_id: {movie_id}")
        return recs.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Error in content recommendation for movie_id: {movie_id} - {e}")
        raise HTTPException(status_code=404, detail="Movie not found")

@router.get("/recommend/hybrid")
def recommend_hybrid(top_n: int = 10, current_user: User = Depends(get_current_user)):
    user_id = current_user.userId
    logger.info(f"Hybrid recommendation request for user_id: {user_id}, top_n: {top_n}")
    if user_id not in matrix.index:
        logger.warning(f"User with id: {user_id} not found for hybrid recommendation.")
        raise HTTPException(status_code=404, detail="User not found")
    recs = get_hybrid_recommendations(user_id, movies, ratings, matrix, movies_df_content, tfidf_matrix, movie_indices, top_n=top_n)
    logger.info(f"Hybrid recommendations generated for user_id: {user_id}")
    return recs.to_dict(orient='records')

@router.get("/recommend")
def recommend(current_user: User = Depends(get_current_user)):
    user_id = current_user.userId
    logger.info(f"Collaborative filtering recommendation request for user_id: {user_id}")
    if user_id not in matrix.index:
        logger.warning(f"User with id: {user_id} not found for collaborative recommendation.")
        raise HTTPException(status_code=404, detail="User not found")
    recs = get_user_recommendations(user_id, matrix, movies, top_n=10)
    logger.info(f"Collaborative filtering recommendations generated for user_id: {user_id}")
    return recs.to_dict(orient='records')

@router.get("/populares")
def populares(current_user: User = Depends(get_current_user)):
    logger.info("Popular movies request")
    recs = get_popular_movies(movies, ratings, top_n=10)
    logger.info("Popular movies returned")
    return recs
