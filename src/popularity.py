def get_popular_movies(movies_df, ratings_df, top_n=10):
    # Número mínimo de votos para estar en la lista (umbral)
    m = ratings_df['movieId'].value_counts().quantile(0.90)  # top 10% más votadas
    movie_stats = ratings_df.groupby('movieId').agg({
        'rating': ['mean', 'count']
    })
    movie_stats.columns = ['rating_mean', 'rating_count']
    movie_stats = movie_stats.reset_index()

    qualified = movie_stats[movie_stats['rating_count'] >= m].copy()

    C = ratings_df['rating'].mean()

    # Fórmula de IMDb
    qualified['score'] = qualified.apply(
        lambda x: (x['rating_count'] / (x['rating_count'] + m)) * x['rating_mean'] +
                  (m / (x['rating_count'] + m)) * C,
        axis=1
    )

    # Unimos con los títulos
    popular_movies = qualified.merge(movies_df, on='movieId')
    popular_movies = popular_movies.sort_values('score', ascending=False)

    return popular_movies[['movieId', 'title', 'score']].head(top_n).to_dict(orient='records')