import requests
import json
from pprint import pprint
from pymongo import MongoClient, GEOSPHERE
import time
import dateutil.parser

atlas = MongoClient(
    'mongodb+srv://dbUser:isen123@cluster0.cndhu.mongodb.net/bicycle?retryWrites=true&w=majority')
bdd = atlas.get_database('bicycle')
collec = bdd.stations


def getNearestStations(longitute, latitude, max_distance):
    collec.create_index([("geometry", "2dsphere")])
    stations = collec.find({
        "geometry": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [longitute, latitude]
                },
                "$maxDistance": max_distance
            }
        }
    }
    )
    nearestStations = []
    for station in stations:
        datas = [
            {
                "name": station.get('name'),
                "coordinates": station.get('geometry', {}).get('coordinates'),
                "bike": get_bikebyid(station.get('_id')),
                "stand": get_standbyid(station.get('_id'))
            }
        ]
        nearestStations.append(datas)
    return nearestStations


def get_bikebyid(id):
    try:
        tps = collec.find_one({"station_id": id}, {'bike_availbale': 1})
        return tps['bike_availbale']
    except:
        return -1


def get_standbyid(id):
    try:
        tps = collec.find_one({"station_id": id}, {'stand_availbale': 1})
        return tps['stand_availbale']
    except:
        return -1


stations = getNearestStations(3.096542, 50.63422, 1000)
for station in stations:
    pprint(station)
