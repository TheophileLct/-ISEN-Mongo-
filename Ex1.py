import requests
import json
import pymongo
from pprint import pprint
from pymongo import MongoClient

atlas = MongoClient(
    'mongodb+srv://dbUser:isen123@cluster0.cndhu.mongodb.net/bicycle?retryWrites=true&w=majority')
bdd = atlas.get_database('bicycle')
collec = bdd.stations


def get_self_service(ville=["Lille", "Lyon", "Paris", "Rennes"], live_data=False):
    list_stations = []
    if "Lille" in ville:
        url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=300&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        response_json = json.loads(response.text.encode('utf8'))
        records = response_json.get("records", [])
        for elem in records:
            vlilles_to_insert = [
                {
                    'name': elem.get('fields', {}).get('nom', '').title(),
                    'geometry': elem.get('geometry'),
                    'size': elem.get('fields', {}).get('nbvelosdispo') + elem.get('fields', {}).get('nbplacesdispo'),
                    'source': {
                        'dataset': 'Lille',
                        'id_ext': elem.get('fields', {}).get('libelle')
                    },
                    'tpe': elem.get('fields', {}).get('type', '') == 'AVEC TPE'
                }
            ]
            list_stations.append(vlilles_to_insert)
            collec.insert_many(vlilles_to_insert)
    if "Lyon" in ville:
        url = "https://api.jcdecaux.com/vls/v3/stations?contract=Lyon&apiKey=6447f398d41c4eb8e8dad3646290848a8b90a5da"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        records = json.loads(response.text.encode('utf8'))
        for elem in records:
            velov_to_insert = [
                {
                    'name': elem.get('nom', '').title(),
                    'geometry': {"type": "Point", "coordinates": [elem.get('position', {}).get('longitude'), elem.get('position', {}).get('latitude')]},
                    'size': elem.get('mainStands', {}).get('availabilities', {}).get('capacity'),
                    'source': {
                        'dataset': 'lyon',
                        'id_ext': elem.get('number')
                    },
                    'tpe': elem.get('banking', '') == 'AVEC TPE'
                }
            ]
            list_stations.append(velov_to_insert)
            collec.insert_many(velov_to_insert)
    if "Paris" in ville:
        url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=1500"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        response_json = json.loads(response.text.encode('utf8'))
        records = response_json.get("records", [])
        for elem in records:
            velib_to_insert = [
                {
                    'name': elem.get('fields', {}).get('name', '').title(),
                    'geometry': elem.get('geometry'),
                    'size': elem.get('fields', {}).get('capacity'),
                    'source': {
                        'dataset': 'Paris',
                        'id_ext': elem.get('fields', {}).get('stationcode')
                    },
                    'tpe': True if elem.get('fields', {}).get('is_renting') == 'OUI' else False,
                }
            ]
            list_stations.append(velib_to_insert)
            collec.insert_many(velib_to_insert)
    if "Rennes" in ville:
        url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&rows=9969&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        response_json = json.loads(response.text.encode('utf8'))
        records = response_json.get("records", [])
        for elem in records:
            vstar_to_insert = [
                {
                    'name': elem.get('fields', {}).get('nom', '').title(),
                    'geometry': elem.get('geometry'),
                    'size': elem.get('fields', {}).get('nombreemplacementsactuels'),
                    'source': {
                        'dataset': 'rennes',
                        'id_ext': elem.get('fields', {}).get('idstation')
                    },
                    'tpe': 'unknown'
                }
            ]
            list_stations.append(vstar_to_insert)
            collec.insert_many(vstar_to_insert)

    return list_stations


list_stations = get_self_service()
