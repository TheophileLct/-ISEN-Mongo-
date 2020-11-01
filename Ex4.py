import requests
import json
import pymongo
from pprint import pprint
from pymongo import MongoClient
from pymongo import TEXT
from bson.objectid import ObjectId
import time
import dateutil.parser

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
# recherche("Planetes")

# -----------------------------------------------------
# update une station avec le champ que l'on souhaite.


def update_station(id, champ, valeur):
    collec.update_one({"_id": id}, {"$set": {champ: valeur}})


# -----------------------------------------------------
# supprimer une station

def remove_station(id):
    collec.delete_one(
        {"_id": id}
    )


# remove_station('ObjectId("5f8c5e6d25a39a05160ef561")')

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


# On la déja exécuter pour mettre à jour toute la bdd une fois
update_boolean_active_station()


# Coordonnées autyour de la station "Theatre sébastopol"
x0 = [3.058289, 50.629045]
x1 = [3.058287, 50.629043]
x2 = [3.058299, 50.629055]
x3 = [3.028279, 50.629035]
# A executer pour mettre faux
# update_station_activity_by_zone(x0, x1, x2, x3, False)

# A reexécuter pour mettre True
# update_station_activity_by_zone(x0, x1, x2, x3, True)

# ----------------------------------------------------------------
# Question ratio


def give_ratio(ratio):
    collec.aggregate([
        {
            '$group': {
                "_id": {"_id": "$station_id"},
                "total_datas": {'$sum': 1},
                "last_hours": {'$max': "18:00"},
                "first_hours": {'$min': "19:00"}
            },
            '$lookup': {
                'from': 'test',
                'localField': "_id",
                'foreignField': "station_id",
                'as': "station"
            },
            '$match': {
                'ratio': {'$lte': ratio}
            },
            "$project": {
                "name": '$name',
                "size": [{'$sum': ['$bike_availbale', '$stand_availbale']}],
                "ratio":{'$divide': ['$bike_availbale', {'$sum': ['$bike_availbale', '$stand_availbale']}]},
            },
        }
    ])


# give_ratio(0.2)
