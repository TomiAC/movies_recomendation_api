import logging
import pandas as pd
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.colaborative import get_user_recommendations
from src.matrix_builder import build_user_item_matrix
from src.popularity import get_popular_movies
from src.content import prepare_content_based, get_similar_movies
from src.hybrid import get_hybrid_recommendations
from .auth import get_current_user, User
from src.database import SessionLocal
from src.models import Movie, Rating, Tag

logger = logging.getLogger(__name__)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_data_from_db(db: Session):
    movies = pd.read_sql(db.query(Movie).statement, db.bind)
    ratings = pd.read_sql(db.query(Rating).statement, db.bind)
    tags = pd.read_sql(db.query(Tag).statement, db.bind)
    # Rename columns to match CSVs
    movies.rename(columns={'id': 'movieId'}, inplace=True)
    ratings.rename(columns={'user_id': 'userId', 'movie_id': 'movieId'}, inplace=True)
    tags.rename(columns={'user_id': 'userId', 'movie_id': 'movieId'}, inplace=True)
    return movies, ratings, tags

@router.get("/recommend/content/{movie_id}")
def recommend_by_content(movie_id: int, top_n: int = 10, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    logger.info(f"Content recommendation request for movie_id: {movie_id}, top_n: {top_n}")
    try:
        movies, _, tags = get_data_from_db(db)
        tfidf_matrix, movie_indices, movies_df_content = prepare_content_based(movies, tags)
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
    
    movies, ratings, tags = get_data_from_db(db)
    matrix = build_user_item_matrix(ratings)
    
    if user_id not in matrix.index:
        logger.warning(f"User with id: {user_id} not found for hybrid recommendation.")
        raise HTTPException(status_code=404, detail="User not found")
        
    tfidf_matrix, movie_indices, movies_df_content = prepare_content_based(movies, tags)
    recs = get_hybrid_recommendations(user_id, movies, ratings, matrix, movies_df_content, tfidf_matrix, movie_indices, top_n=top_n)
    logger.info(f"Hybrid recommendations generated for user_id: {user_id}")
    return recs.to_dict(orient='records')

@router.get("/recommend")
def recommend(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.userId
    logger.info(f"Collaborative filtering recommendation request for user_id: {user_id}")
    
    movies, ratings, _ = get_data_from_db(db)
    matrix = build_user_item_matrix(ratings)

    if user_id not in matrix.index:
        logger.warning(f"User with id: {user_id} not found for collaborative recommendation.")
        raise HTTPException(status_code=404, detail="User not found")
    
    recs = get_user_recommendations(user_id, matrix, movies, top_n=10)
    logger.info(f"Collaborative filtering recommendations generated for user_id: {user_id}")
    return recs.to_dict(orient='records')

@router.get("/populares")
def populares(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    logger.info("Popular movies request")
    movies, ratings, _ = get_data_from_db(db)
    recs = get_popular_movies(movies, ratings, top_n=10)
    logger.info("Popular movies returned")
    return recs