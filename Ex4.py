import requests
import json
import pymongo
from pprint import pprint
from pymongo import MongoClient
from pymongo import TEXT
from bson.objectid import ObjectId

atlas = MongoClient(
    'mongodb+srv://dbUser:isen123@cluster0.cndhu.mongodb.net/bicycle?retryWrites=true&w=majority')
bdd = atlas.get_database('bicycle')
collec = bdd.stations

# -----------------------------------------------------
# Trouver une station avec un nom.
collec.create_index([("name", TEXT)])


def recherche(txt):
    for station in collec.find({"$text": {"$search": txt, "$caseSensitive": False}}):
        pprint(station)


# Test de notre fonction recherche
recherche("Planetes")

# -----------------------------------------------------
# update une station


def update_name_station(id, newName):
    collec.update(
        {"_id": id},
        {"$set": {'name': newName}})


# -----------------------------------------------------
# supprimer une station
def remove_station(id):
    collec.delete_one(
        {"_id": id}
    )


# remove_station("Planetes")

# -----------------------------------------------------
# Désactiver les stations dans un carré choisi


def update_station_activity_by_zone(x0, x1, x2, x3, state):
    collec.update_many(
        {"geometry": {
            "$geoWithin":
                {
                    "$polygon": [[x0[0], x0[1]], [x1[0], x1[1]], [x2[0], x2[1]], [x3[0], x3[1]]]
                }
        }
        },
        {"$set": {"active": state}})


# Lors de la création de la BDD nous n'avions pas mis l'activité donc nous le faisons maintenant.
def update_boolean_active_station():
    {
        collec.update_many(
            {},
            {"$set": {"active": True}}, upsert=False, array_filters=None)
    }


# ----------------------------------------------------------------
# Donne le nombre de station avec un nombre total sous
def give_ration(ratio):
    maxplaces = 20
    places = int(maxplaces*maxplaces/100)
    for station in collec.find({"size": {"$lt": places}}):
        pprint(station)


give_ration(20)
