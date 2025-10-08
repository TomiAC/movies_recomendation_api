import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.colaborative import get_user_recommendations
from src.popularity import get_popular_movies
from src.content import get_similar_movies
from src.hybrid import get_hybrid_recommendations
from dependencies import get_data_manager, PrecomputedDataManager
from .auth import get_current_user, User
from src.database import get_db
from src.utils import get_data_from_db
from src.models import Rating as RatingModel
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()

class RatingCreate(BaseModel):
    movie_id: int
    rating: float

@router.post("/rate")
def rate_movie(rating: RatingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    logger.info(f"Rating submission request for movie_id: {rating.movie_id} by user_id: {current_user.id}")
    
    db_rating = RatingModel(
        user_id=current_user.id,
        movie_id=rating.movie_id,
        rating=rating.rating,
        timestamp=int(datetime.now().timestamp())
    )
    
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    
    logger.info(f"Rating of {rating.rating} for movie {rating.movie_id} by user {current_user.id} saved.")
    
    return {"message": "Rating submitted successfully"}

@router.get("/recommend/content/{movie_id}")
def recommend_by_content(movie_id: int, top_n: int = 10, current_user: User = Depends(get_current_user), data_manager: PrecomputedDataManager = Depends(get_data_manager)):
    logger.info(f"Content recommendation request for movie_id: {movie_id}, top_n: {top_n}")
    try:
        recs = get_similar_movies(movie_id, data_manager.movies_df_content, data_manager.tfidf_matrix, data_manager.movie_indices, top_n=top_n)
        logger.info(f"Content recommendations generated for movie_id: {movie_id}")
        return recs.to_dict(orient='records')
    except Exception as e:
        logger.error(f"Error in content recommendation for movie_id: {movie_id} - {e}")
        raise HTTPException(status_code=404, detail="Movie not found")

@router.get("/recommend/hybrid")
def recommend_hybrid(top_n: int = 10, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), data_manager: PrecomputedDataManager = Depends(get_data_manager)):
    user_id = current_user.id
    logger.info(f"Hybrid recommendation request for user_id: {user_id}, top_n: {top_n}")
    
    movies, ratings, _ = get_data_from_db(db)
    
    if user_id not in data_manager.user_item_matrix.index:
        logger.warning(f"User with id: {user_id} not found for hybrid recommendation.")
        raise HTTPException(status_code=404, detail="User not found")
        
    recs = get_hybrid_recommendations(user_id, movies, ratings, data_manager.user_item_matrix, data_manager.movies_df_content, data_manager.tfidf_matrix, data_manager.movie_indices, top_n=top_n)
    logger.info(f"Hybrid recommendations generated for user_id: {user_id}")
    return recs.to_dict(orient='records')

@router.get("/recommend")
def recommend(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), data_manager: PrecomputedDataManager = Depends(get_data_manager)):
    user_id = current_user.id
    logger.info(f"Collaborative filtering recommendation request for user_id: {user_id}")
    
    movies, _, _ = get_data_from_db(db)

    if user_id not in data_manager.user_item_matrix.index:
        logger.warning(f"User with id: {user_id} not found for collaborative recommendation.")
        raise HTTPException(status_code=404, detail="User not found")
    
    recs = get_user_recommendations(user_id, data_manager.user_item_matrix, movies, top_n=10)
    logger.info(f"Collaborative filtering recommendations generated for user_id: {user_id}")
    return recs.to_dict(orient='records')

@router.get("/populars")
def populars(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    logger.info("Popular movies request")
    movies, ratings, _ = get_data_from_db(db)
    recs = get_popular_movies(movies, ratings, top_n=10)
    logger.info("Popular movies returned")
    return recs