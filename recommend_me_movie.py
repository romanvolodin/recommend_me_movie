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
    parser.add_argument(
        '--count',
        help = 'Movie count to recommend',
        type = int,
        default = 5,
    )
    return parser.parse_args()


def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except json.decoder.JSONDecodeError:
        return


def fetch_movie(movie_id):
    response = requests.get(
        f"{TMDB_API_URL}/movie/{movie_id}", params=payload, timeout=5
    )
    if response.status_code == 200:
        return response.json()


def fetch_movie_keywords(movie_id):
    response = requests.get(
        f"{TMDB_API_URL}/movie/{movie_id}/keywords", params=payload, timeout=5
    )
    if response.status_code == 200:
        return response.json()["keywords"]


def fetch_movie_lists(movie_id):
    response = requests.get(
        f"{TMDB_API_URL}/movie/{movie_id}/lists", params=payload, timeout=5
    )
    if response.status_code == 200:
        return response.json()["results"]


def fetch_random_movies(movie_count=10):
    import random
    movies = []
    used_ids = []
    while True:
        if len(movies) >= movie_count:
            break

        random_id = random.randint(0, 100000)
        if random_id in used_ids:
            continue
        
        movie = fetch_movie(random_id)
        if movie is None:
            continue

        movie_keywords = fetch_movie_keywords(random_id)
        movie["keywords"] = []
        if movie_keywords:
            movie["keywords"] = movie_keywords

        movie_lists = fetch_movie_lists(random_id)
        movie["lists"] = []
        if movie_lists:
            movie["lists"] = movie_lists

        movies.append(movie)
        used_ids.append(random_id)
    return movies


def find_movie_by_title(title, movies_data):
    try:
        sample_movie = [
            movie for movie in movies_data
            if title.lower() == movie['title'].lower()
        ][0]
        return sample_movie
    except IndexError:
        return


def recommend_movies(sample_movie, movies_data, movie_count=10):
    recommended_movies = {}
    for movie in movies_data:
        if movie == sample_movie:
            continue

        recommendation_weight = 0

        for genre in movie['genres']:
            if genre in sample_movie['genres']:
                recommendation_weight += 1

        for keyword in movie['keywords']:
            if keyword in sample_movie['keywords']:
                recommendation_weight += 1

        for playlist in movie['lists']:
            if playlist in sample_movie['lists']:
                recommendation_weight += 1

        if recommendation_weight > 0:
            recommended_movies[recommendation_weight] = movie

    recommended_movies = dict(reversed(sorted(recommended_movies.items())))

    return dict(list(recommended_movies.items())[:movie_count])


if __name__ == "__main__":
    env = Env()
    env.read_env() 

    api_key = env.str("RMM_API_KEY")
    language = env.str("RMM_LANGUAGE")

    args = parse_arguments()
    movie_title = args.movie_title
    movie_db_path = args.db_path
    count = args.count

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
    
    sample_movie = find_movie_by_title(movie_title, movies_data)

    if sample_movie is not None:
        recommended_movies = recommend_movies(sample_movie, movies_data, count)

    if not recommended_movies:
        exit('Sorry, can\'t find any movie. Try different movie title.')

    for recommended_movie in recommended_movies.values():
        print(recommended_movie['title'])
