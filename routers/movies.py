from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.models import Movie
from src.database import get_db
from .auth import get_current_user, User
from pydantic import BaseModel
from typing import List

router = APIRouter()

class MovieResponse(BaseModel):
    id: int
    title: str
    genres: str

    class Config:
        orm_mode = True

class PaginatedMovieResponse(BaseModel):
    total_count: int
    movies: List[MovieResponse]

@router.get("/movies", response_model=PaginatedMovieResponse)
def get_all_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    total_count = db.query(Movie).count()
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return {"total_count": total_count, "movies": movies}

@router.get("/movies/search", response_model=PaginatedMovieResponse)
def search_movie(name: str = Query(..., min_length=3), skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Movie).filter(Movie.title.contains(name))
    total_count = query.count()
    movies = query.offset(skip).limit(limit).all()
    return {"total_count": total_count, "movies": movies}
