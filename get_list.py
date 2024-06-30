import requests
import json
from config import API_KEY_KP
def filter_none_values(movie_titles):
    return [title for title in movie_titles if title is not None]
def get_list_person(id_person):
   url = f"https://api.kinopoisk.dev/v1.4/person/{id_person}"
   headers = {
    "accept": "application/json",
    "X-API-KEY": API_KEY_KP}
   response = requests.get(url, headers=headers)
   data = json.loads(response.text)
   director_movies = [movie["name"] for movie in data["movies"] if movie["enProfession"] == "director"]
   director_movies_norm = filter_none_values(director_movies)
   img = data.get("photo", "")
   return director_movies_norm,img
