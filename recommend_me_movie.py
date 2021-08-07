import argparse

from environs import Env
import requests


TMDB_API_URL = "https://api.themoviedb.org/3"


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'movie_title',
        help = 'Movie title for recommendations',
    )
    return parser.parse_args()


def fetch_random_movies(num=10):
    import random
    movies = []
    used_ids = []
    while True:
        random_id = random.randint(0, 100000)
        if random_id in used_ids:
            continue
        movie = requests.get(f"{TMDB_API_URL}/movie/{random_id}", params=payload, timeout=5)
        if movie.status_code == 200:
            movies.append(movie.json())
            used_ids.append(random_id)
        if len(movies) >= num:
            break
    return movies


if __name__ == "__main__":
    env = Env()
    env.read_env() 

    api_key = env.str("RMM_API_KEY")
    language = env.str("RMM_LANGUAGE")

    args = parse_arguments()

    payload = {
        "api_key": api_key,
        "language": language,
        "query": args.movie_title,
    }
    response = requests.get(f"{TMDB_API_URL}/search/movie", params=payload, timeout=10)
    print(response.json())