import pandas as pd
from sqlalchemy.orm import Session
import sys
import os

# Add project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import SessionLocal, engine, create_db_and_tables
from src.models import Base, Movie, User, Rating, Tag
from routers.auth import get_password_hash

def load_data():
    db: Session = SessionLocal()

    try:
        # Check if data is already loaded
        if db.query(Movie).first() or db.query(User).first():
            print("Data appears to be already loaded. Aborting.")
            return

        print("Loading movies...")
        movies_df = pd.read_csv('datasets/movies.csv')
        for _, row in movies_df.iterrows():
            movie = Movie(id=row['movieId'], title=row['title'], genres=row['genres'])
            db.add(movie)
        db.commit()
        print(f"{len(movies_df)} movies loaded.")

        print("Loading users, ratings, and tags...")
        ratings_df = pd.read_csv('datasets/ratings.csv')
        tags_df = pd.read_csv('datasets/tags.csv')

        # Get unique users from both files
        user_ids = pd.concat([ratings_df['userId'], tags_df['userId']]).unique()
        hashed_password = get_password_hash("password")
        for user_id in user_ids:
            user = User(
                id=int(user_id),
                username=f"user{user_id}",
                hashed_password=hashed_password
            )
            db.add(user)
        db.commit()
        print(f"{len(user_ids)} users loaded.")

        print("Loading ratings...")
        for _, row in ratings_df.iterrows():
            rating = Rating(
                user_id=row['userId'],
                movie_id=row['movieId'],
                rating=row['rating'],
                timestamp=row['timestamp']
            )
            db.add(rating)
        db.commit()
        print(f"{len(ratings_df)} ratings loaded.")

        print("Loading tags...")
        for _, row in tags_df.iterrows():
            tag = Tag(
                user_id=row['userId'],
                movie_id=row['movieId'],
                tag=row['tag'],
                timestamp=row['timestamp']
            )
            db.add(tag)
        db.commit()
        print(f"{len(tags_df)} tags loaded.")

        print("\nData loading complete!")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating database and tables...")
    create_db_and_tables()
    print("Database and tables created.")
    load_data()
