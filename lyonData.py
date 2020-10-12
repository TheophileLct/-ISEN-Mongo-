import requests
import json
from pprint import pprint

def get_vlyon():
    key="2f3f00af9ce4e0959c3611b330a7be5f1af2b436"
    url = "https://api.jcdecaux.com/vls/v3/stations?contract=Lyon&apiKey=2f3f00af9ce4e0959c3611b330a7be5f1af2b436"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)

    response_json = json.loads(response.text.encode('utf8'))

    return response_json

vlilles = get_vlyon()

for vlille in vlilles:
    pprint(vlille)