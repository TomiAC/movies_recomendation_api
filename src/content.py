from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

def prepare_content_based(movies, tags):
    # Juntamos títulos con los tags por movieId
    tags_grouped = tags.groupby("movieId")["tag"].apply(lambda x: " ".join(x)).reset_index()
    movies_df = pd.merge(movies, tags_grouped, on="movieId", how="left")
    movies_df["tag"] = movies_df["tag"].fillna("")
    movies_df["content"] = movies_df["title"] + " " + movies_df["tag"]

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df["content"])
    movie_indices = pd.Series(movies_df.index, index=movies_df['movieId'])
    
    return tfidf_matrix, movie_indices, movies_df

def get_similar_movies(movie_id, movies_df, tfidf_matrix, movie_indices, top_n=10):
    if movie_id not in movie_indices:
        return pd.DataFrame()

    idx = movie_indices[movie_id]
    cosine_similarities = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    sim_scores = list(enumerate(cosine_similarities))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices_similar = [i[0] for i in sim_scores]
    similar_movies = movies_df.iloc[movie_indices_similar][['movieId', 'title']]
    return similar_movies