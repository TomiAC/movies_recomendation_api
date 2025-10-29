import os
import sys
import pandas as pd
import joblib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.matrix_builder import build_user_item_matrix
from src.content import prepare_content_based
from src.database import SessionLocal
from src.utils import get_data_from_db

def precompute_and_save():
    db = SessionLocal()
    movies, ratings, tags = get_data_from_db(db)
    db.close()

    print("Building user-item matrix...")
    user_item_matrix = build_user_item_matrix(ratings)
    print("User-item matrix built.")

    print("Preparing content-based data...")
    tfidf_matrix, movie_indices, movies_df_content = prepare_content_based(movies, tags)
    print("Content-based data prepared.")

    output_dir = 'precomputed_data'
    os.makedirs(output_dir, exist_ok=True)

    print(f"Saving user-item matrix to {output_dir}/user_item_matrix.joblib...")
    joblib.dump(user_item_matrix, os.path.join(output_dir, 'user_item_matrix.joblib'))
    print("User-item matrix saved.")

    print(f"Saving TF-IDF matrix to {output_dir}/tfidf_matrix.joblib...")
    joblib.dump(tfidf_matrix, os.path.join(output_dir, 'tfidf_matrix.joblib'))
    print("TF-IDF matrix saved.")

    print(f"Saving movie indices to {output_dir}/movie_indices.joblib...")
    joblib.dump(movie_indices, os.path.join(output_dir, 'movie_indices.joblib'))
    print("Movie indices saved.")

    print(f"Saving content movies DataFrame to {output_dir}/movies_df_content.joblib...")
    joblib.dump(movies_df_content, os.path.join(output_dir, 'movies_df_content.joblib'))
    print("Content movies DataFrame saved.")

if __name__ == "__main__":
    precompute_and_save()
