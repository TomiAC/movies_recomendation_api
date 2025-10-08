from sqlalchemy.orm import Session
from src.models import Movie

def create_test_movie(session: Session, title: str = "Test Movie", genres: str = "Test|Genre") -> Movie:
    movie = Movie(title=title, genres=genres)
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie
