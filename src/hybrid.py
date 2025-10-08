import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from src.content import get_similar_movies
from src.colaborative import get_user_recommendations

def get_hybrid_recommendations(user_id, movies, ratings, matrix, movies_df_content, tfidf_matrix, movie_indices, top_n=10):
    # --- Estrategia Híbrida Mejorada ---
    # 1. Obtener recomendaciones colaborativas (como antes)
    collab_recs = get_user_recommendations(user_id, matrix, movies, top_n=top_n*2) # Pedimos más para tener margen

    # 2. Crear un "perfil de gusto" del usuario para recomendaciones de contenido
    user_ratings = ratings[ratings['userId'] == user_id]
    if user_ratings.empty:
        # Si no hay ratings, no podemos generar recomendaciones de contenido.
        # Devolvemos solo las colaborativas si existen, o un DataFrame vacío.
        return collab_recs.head(top_n)
    
    # Obtener las películas que el usuario ha calificado positivamente (e.g., > 3.5)
    liked_movies_ids = user_ratings[user_ratings['rating'] > 3.5]['movieId']
    
    # Filtrar solo las películas que están en nuestros datos de contenido
    liked_movie_indices = [movie_indices[movie_id] for movie_id in liked_movies_ids if movie_id in movie_indices]

    content_recs = pd.DataFrame() # Inicializamos por si no hay películas que le gusten
    if liked_movie_indices:
        # Crear el perfil del usuario promediando los vectores TF-IDF de las películas que le gustaron
        user_profile = np.asarray(np.mean(tfidf_matrix[liked_movie_indices], axis=0))
        
        # Calcular la similitud del coseno entre el perfil del usuario y todas las películas
        cosine_similarities = cosine_similarity(user_profile, tfidf_matrix)
        
        # Obtener los índices de las películas más similares
        sim_scores = list(enumerate(cosine_similarities[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Obtener los top_n resultados (excluyendo las que ya ha visto)
        movie_indices_rec = [i[0] for i in sim_scores[1:top_n*2+1]]
        
        # Mapear índices a movieIds y obtener títulos
        recommended_movie_ids = movies_df_content['movieId'].iloc[movie_indices_rec]
        
        # Crear el DataFrame de recomendaciones de contenido
        content_recs = movies_df_content[movies_df_content['movieId'].isin(recommended_movie_ids)]

    # 3. Combinar y eliminar duplicados (dando prioridad a las colaborativas)
    hybrid_recs = pd.concat([content_recs, collab_recs]).drop_duplicates(subset='movieId').head(top_n)
    
    return hybrid_recs
