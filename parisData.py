import requests
import json
from pprint import pprint

def get_vparis():
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=2971&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)

    response_json = json.loads(response.text.encode('utf8'))

    return response_json.get("records", [])

vlilles = get_vparis()

for vlille in vlilles:
    pprint(vlille)