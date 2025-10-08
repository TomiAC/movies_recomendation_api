import os
import joblib
from functools import lru_cache

DATA_PATH = "precomputed_data"

class PrecomputedDataManager:
    def __init__(self, data_path: str):
        self.user_item_matrix = joblib.load(os.path.join(data_path, "user_item_matrix.joblib"))
        self.tfidf_matrix = joblib.load(os.path.join(data_path, "tfidf_matrix.joblib"))
        self.movie_indices = joblib.load(os.path.join(data_path, "movie_indices.joblib"))
        self.movies_df_content = joblib.load(os.path.join(data_path, "movies_df_content.joblib"))

@lru_cache()
def get_data_manager():
    return PrecomputedDataManager(DATA_PATH)