import requests
import json
from pprint import pprint
from pymongo import MongoClient
import time
import dateutil.parser

atlas = MongoClient(
    'mongodb+srv://dbUser:isen123@cluster0.cndhu.mongodb.net/bicycle?retryWrites=true&w=majority')
bdd = atlas.get_database('bicycle')
collec = bdd.stations


def get_vlille():
    url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=-1&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


def get_vparis():
    url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=1500"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


def get_vrennes():
    url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&rows=9969&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
    response = requests.request("GET", url)
    response_json = json.loads(response.text.encode('utf8'))
    return response_json.get("records", [])


def get_station_id(id_ext):
    tps = collec.find_one({'source.id_ext': id_ext}, {'_id': 1})
    return tps['_id']


while True:
    print('update')
    vlilles = get_vlille()
    datas_lille = [
        {
            "bike_availbale": elem.get('fields', {}).get('nbvelosdispo'),
            "stand_availbale": elem.get('fields', {}).get('nbplacesdispo'),
            "date": dateutil.parser.parse(elem.get('fields', {}).get('datemiseajour')),
            "station_id": get_station_id(elem.get('fields', {}).get('libelle'))
        }
        for elem in vlilles
    ]
    try:
        collec.insert_many(datas_lille, ordered=False)
    except:
        pass

    url = "https://api.jcdecaux.com/vls/v3/stations?contract=Lyon&apiKey=6447f398d41c4eb8e8dad3646290848a8b90a5da"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    response_json2 = json.loads(response.text.encode('utf8'))
    for elem in response_json2:
        datas_lyon = [
            {
                "bike_availbale": elem.get('mainStands', {}).get('availabilities', {}).get('bikes'),
                "stand_availbale": elem.get('mainStands', {}).get('availabilities', {}).get('stands'),
                "date": dateutil.parser.parse(elem.get('lastUpdate')),
                "station_id": get_station_id(elem.get('number'))
            }
        ]
    try:
        collec.insert_many(datas_lyon, ordered=False)
    except:
        pass

    vparis = get_vparis()
    for elem in vparis:
        datas_paris = [
            {
                "bike_availbale": elem.get('fields', {}).get('numbikesavailable'),
                "stand_availbale": elem.get('fields', {}).get('numdocksavailable'),
                "date": dateutil.parser.parse(elem.get('fields', {}).get('duedate')),
                "station_id": get_station_id(elem.get('fields', {}).get('stationcode'))
            }

        ]
    try:
        collec.insert_many(datas_paris, ordered=False)
    except:
        pass

    vrennes = get_vrennes()
    for elem in vrennes:
        try:
            datas_rennes = [
                {
                    "bike_availbale": elem.get('fields', {}).get('nombrevelosdisponibles'),
                    "stand_availbale": elem.get('fields', {}).get('nombreemplacementsdisponibles'),
                    "date": dateutil.parser.parse(elem.get('fields', {}).get('lastupdate')),
                    "station_id": get_station_id(elem.get('fields', {}).get('idstation'))
                }
            ]
        except:
            pass
    try:
        collec.insert_many(datas_rennes, ordered=False)
    except:
        pass

    time.sleep(10)
