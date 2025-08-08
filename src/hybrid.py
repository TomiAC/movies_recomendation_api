import pandas as pd
from src.content import get_similar_movies
from src.colaborative import get_user_recommendations

def get_hybrid_recommendations(user_id, movies, ratings, matrix, movies_df_content, tfidf_matrix, movie_indices, top_n=10):
    # 1. Obtener la película mejor calificada por el usuario
    user_ratings = ratings[ratings['userId'] == user_id]
    if user_ratings.empty:
        # No hay calificaciones para el usuario
        return pd.DataFrame(columns=['movieId', 'title'])
    
    best_movie_id = user_ratings.sort_values(by='rating', ascending=False).iloc[0]['movieId']

    # 2. Obtener recomendaciones basadas en contenido para esa película
    content_recs = get_similar_movies(best_movie_id, movies_df_content, tfidf_matrix, movie_indices, top_n=top_n)

    # 3. Obtener recomendaciones colaborativas
    collab_recs = get_user_recommendations(user_id, matrix, movies, top_n=top_n)

    # 4. Combinar y eliminar duplicados
    hybrid_recs = pd.concat([content_recs, collab_recs]).drop_duplicates(subset='movieId').head(top_n)
    
    return hybrid_recs
