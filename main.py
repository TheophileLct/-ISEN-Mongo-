import requests
import json
from pprint import pprint

def get_data(ville):

    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=300&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)

    response_json = json.loads(response.text.encode('utf8'))

    return response_json.get("records", [])

vlilles = get_data("lille")

for vlille in vlilles.find({"commune":"LILLE"}):
    pprint(vlille)