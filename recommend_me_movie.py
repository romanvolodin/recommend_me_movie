from environs import Env
import requests


TMDB_API_URL = "https://api.themoviedb.org/3"


if __name__ == "__main__":
    env = Env()
    env.read_env() 

    api_key = env.str("RMM_API_KEY")
    payload = {
        "api_key": api_key,
        "language": "ru-RU",
        "query": "Terminator",
    }
    response = requests.get(f"{TMDB_API_URL}/search/movie", params=payload, timeout=10)
