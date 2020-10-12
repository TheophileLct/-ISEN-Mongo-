import requests
import json
from pprint import pprint

def get_vrennes():
    url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&rows=9969&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)

    response_json = json.loads(response.text.encode('utf8'))

    return response_json.get("records", [])

vlilles = get_vrennes()

for vlille in vlilles:
    pprint(vlille)