import requests
import omdb
from config import API_KEY_KP,API_KEY_OMDB
omdb.set_default('apikey', API_KEY_OMDB)

def get_movie_rating(movie_name):
    url = f"https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=4&query={movie_name}"
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY_KP
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if "docs" in data and len(data["docs"]) > 0:
        movie = data["docs"][0]  # Берем первый фильм из результатов поиска
        kp_rating = movie.get("rating", {}).get("kp", None)
        id_imdb = movie.get("externalId", {}).get("imdb", None)
        year = movie.get("year", "")
        img = movie.get("poster", {}).get("previewUrl", None)
        if img or year is None:
            img == 0
            year == 0
        if id_imdb is None:
            id_imdb == 0
        alternative_name = movie.get("alternativeName", "")
        return kp_rating, alternative_name, id_imdb, year, img
    else:
        return None, None, None
def get_movie_rating1(movie_name):
    url = f"https://api.kinopoisk.dev/v1.4/movie/search?page=1&limit=4&query={movie_name}"
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_KEY_KP
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    if "docs" in data and len(data["docs"]) > 0:
        movie = data["docs"][0]  # Берем первый фильм из результатов поиска
        kp_rating = movie.get("rating", {}).get("kp", None)
        id_imdb = movie.get("externalId", {}).get("imdb", None)
        year = movie.get("year", "")
        img = movie.get("poster", {}).get("previewUrl", None)
        if img or year is None:
            img == 0
            year == 0
        if id_imdb is None:
            id_imdb == 0
        alternative_name = movie.get("alternativeName", "")
        return kp_rating, alternative_name, id_imdb
    else:
        return None, None, None
def get_omdb_ratings(alternative_name, id_imdb):
    movie_data = omdb.get(title=alternative_name)
    if not movie_data:
        movie_data = omdb.imdbid(id_imdb)
    if not movie_data:
        return None, None
    imdb_rating_str = movie_data.get('imdb_rating', 0)
    metascore_str = movie_data.get('metascore', 0)
    try:
        imdb_rating = float(imdb_rating_str) if imdb_rating_str != 'N/A' else 0
    except ValueError:
        imdb_rating = 0
    try:
        metascore = float(metascore_str) / 10 if metascore_str != 'N/A' else 0
    except ValueError:
        metascore = 0
    rt_rating_str = next((rating['value'] for rating in movie_data['ratings'] if rating['source'] == 'Rotten Tomatoes'), None)
    if rt_rating_str is None:
        rt_rating = 0
    else :
        rt_rating = float(rt_rating_str.replace('%', ''))
    if rt_rating != 0  and metascore != 0:
        crit_rating = (rt_rating / 10 + metascore) / 2
    if rt_rating == 0:
        crit_rating = metascore
    else:
        crit_rating = rt_rating / 10

    return imdb_rating, crit_rating

def calculate_average_rating(kp_rating, imdb_rating, crit_rating):
    if kp_rating is None or imdb_rating is None or crit_rating is None:
        return None
    else:
        return (kp_rating + imdb_rating + crit_rating) / 3
