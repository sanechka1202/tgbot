import requests
import json
from config import API_KEY_KP
def filter_none_values(actor_titles):
    return [title for title in actor_titles if title is not None]
def get_listact_person(id_person):
   url = f"https://api.kinopoisk.dev/v1.4/person/{id_person}"
   headers = {
    "accept": "application/json",
    "X-API-KEY": API_KEY_KP}
   response = requests.get(url, headers=headers)
   data = json.loads(response.text)
   actor_movies = [movie["name"] for movie in data["movies"] if movie["enProfession"] == "actor"]
   actor_movies_norm = filter_none_values(actor_movies)
   img = data.get("photo", "")
   return actor_movies_norm,img
