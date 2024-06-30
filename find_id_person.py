import requests
import json
from urllib.parse import quote
from config import API_KEY_KP

def get_id_person(person_name):
    person_name_conv = quote(person_name)
    url = f"https://api.kinopoisk.dev/v1.4/person/search?page=1&limit=3&query={person_name_conv}"
    headers = {
    "accept": "application/json",
    "X-API-KEY": API_KEY_KP}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    if data["docs"][0]["age"] == 0:
        first_person_id = data["docs"][1]["id"]
        return first_person_id
    else:
        first_person_id = data["docs"][0]["id"]
        return first_person_id
