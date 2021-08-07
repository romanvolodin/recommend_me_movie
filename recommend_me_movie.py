import argparse
from distutils.util import strtobool
import json
import os

from environs import Env
import requests


TMDB_API_URL = "https://api.themoviedb.org/3"


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'movie_title',
        help = 'Movie title for recommendations',
    )
    parser.add_argument(
        '--db-path',
        help = 'Path to movie DB json',
        default = 'movie-db.json',
    )
    return parser.parse_args()


def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except json.decoder.JSONDecodeError:
        return


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
    movie_title = args.movie_title
    movie_db_path = args.db_path

    payload = {
        "api_key": api_key,
        "language": language,
    }

    if not os.path.exists(movie_db_path):
        print(movie_db_path, "not found.")
        download_now = input(
            f"Download movies data from The Movie DB save it as {movie_db_path}? [y/n] "
        ).strip()
        if not strtobool(download_now):
            exit()
        try:
            number_of_movies = int(
                input("How many movies to download? (1 - 1000) ")
            )
        except ValueError:
            exit("Can't parse a number.")
        movies = fetch_random_movies(number_of_movies)
        with open(movie_db_path, 'w', encoding='utf-8') as f:
            json.dump(movies, f, ensure_ascii=False, separators=(',', ':'))

    try:
        movies_data = load_data(movie_db_path)
    except PermissionError as err:
        exit(err)

    if movies_data is None:
        exit(f'Error: Can\'t read {movie_db_path}. '
             f'Make sure the file contains a json data')
