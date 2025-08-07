def build_user_item_matrix(ratings):
    return ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)