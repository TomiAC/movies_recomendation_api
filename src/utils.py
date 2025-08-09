import pandas as pd
from sqlalchemy.orm import Session
from src.models import Movie, Rating, Tag

def load_data():
    movies = pd.read_csv("datasets/movies.csv")
    ratings = pd.read_csv("datasets/ratings.csv")
    links = pd.read_csv("datasets/links.csv")
    tags = pd.read_csv("datasets/tags.csv")
    return movies, ratings, tags

def get_data_from_db(db: Session):
    movies = pd.read_sql(db.query(Movie).statement, db.bind)
    ratings = pd.read_sql(db.query(Rating).statement, db.bind)
    tags = pd.read_sql(db.query(Tag).statement, db.bind)
    # Rename columns to match CSVs
    movies.rename(columns={'id': 'movieId'}, inplace=True)
    ratings.rename(columns={'user_id': 'userId', 'movie_id': 'movieId'}, inplace=True)
    tags.rename(columns={'user_id': 'userId', 'movie_id': 'movieId'}, inplace=True)
    return movies, ratings, tags
