from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_user_recommendations(user_id, user_item_matrix, movies, top_n=10):
    # Similitud entre usuarios
    user_sim = cosine_similarity(user_item_matrix)
    user_idx = user_item_matrix.index.get_loc(user_id)

    sim_scores = user_sim[user_idx]
    sim_users = np.argsort(sim_scores)[::-1][1:]

    # Ponderar los ratings de otros usuarios similares
    weighted_ratings = user_item_matrix.iloc[sim_users].T.dot(sim_scores[sim_users])
    weighted_ratings /= np.array([np.abs(sim_scores[sim_users]).sum()])

    user_seen = user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].index
    recs = weighted_ratings.drop(user_seen).sort_values(ascending=False).head(top_n)

    rec_movies = movies[movies['movieId'].isin(recs.index)]
    return rec_movies[['movieId', 'title']]