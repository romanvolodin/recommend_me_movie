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


if __name__ == "__main__":
    env = Env()
    env.read_env() 

    api_key = env.str("RMM_API_KEY")

    args = parse_arguments()

    payload = {
        "api_key": api_key,
        "language": "ru-RU",
        "query": args.movie_title,
    }
    response = requests.get(f"{TMDB_API_URL}/search/movie", params=payload, timeout=10)
    print(response.json())