import logging
import os
import joblib
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.colaborative import get_user_recommendations
from src.popularity import get_popular_movies
from src.content import get_similar_movies
from src.hybrid import get_hybrid_recommendations
from .auth import get_current_user, User
from src.database import SessionLocal
from src.utils import get_data_from_db

logger = logging.getLogger(__name__)

router = APIRouter()

# Cargar datos precalculados al iniciar la aplicación
DATA_PATH = "precomputed_data"
user_item_matrix = joblib.load(os.path.join(DATA_PATH, "user_item_matrix.joblib"))
tfidf_matrix = joblib.load(os.path.join(DATA_PATH, "tfidf_matrix.joblib"))
movie_indices = joblib.load(os.path.join(DATA_PATH, "movie_indices.joblib"))
movies_df_content = joblib.load(os.path.join(DATA_PATH, "movies_df_content.joblib"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
def recommend_hybrid(top_n: int = 10, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.userId
    logger.info(f"Hybrid recommendation request for user_id: {user_id}, top_n: {top_n}")
    
    movies, ratings, _ = get_data_from_db(db)
    
    if user_id not in user_item_matrix.index:
        logger.warning(f"User with id: {user_id} not found for hybrid recommendation.")
        raise HTTPException(status_code=404, detail="User not found")
        
    recs = get_hybrid_recommendations(user_id, movies, ratings, user_item_matrix, movies_df_content, tfidf_matrix, movie_indices, top_n=top_n)
    logger.info(f"Hybrid recommendations generated for user_id: {user_id}")
    return recs.to_dict(orient='records')

@router.get("/recommend")
def recommend(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.userId
    logger.info(f"Collaborative filtering recommendation request for user_id: {user_id}")
    
    movies, _, _ = get_data_from_db(db)

    if user_id not in user_item_matrix.index:
        logger.warning(f"User with id: {user_id} not found for collaborative recommendation.")
        raise HTTPException(status_code=404, detail="User not found")
    
    recs = get_user_recommendations(user_id, user_item_matrix, movies, top_n=10)
    logger.info(f"Collaborative filtering recommendations generated for user_id: {user_id}")
    return recs.to_dict(orient='records')

@router.get("/populares")
def populares(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    logger.info("Popular movies request")
    movies, ratings, _ = get_data_from_db(db)
    recs = get_popular_movies(movies, ratings, top_n=10)
    logger.info("Popular movies returned")
    return recs