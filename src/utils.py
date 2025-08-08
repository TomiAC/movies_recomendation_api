import pandas as pd

def load_data():
    movies = pd.read_csv("datasets/movies.csv")
    ratings = pd.read_csv("datasets/ratings.csv")
    links = pd.read_csv("datasets/links.csv")
    tags = pd.read_csv("datasets/tags.csv")
    return movies, ratings, tags