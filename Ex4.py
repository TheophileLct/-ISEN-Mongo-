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
# recherche("Planetes")

# -----------------------------------------------------
# update une station, on la fait pour le nom ici, mais il
#  est possible de mettre à jour ce que l'on souhaite.


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
# update_boolean_active_station()


# Coordonnées autyour de la station "Theatre sébastopol"
x0 = [3.058289, 50.629045]
x1 = [3.058287, 50.629043]
x2 = [3.058299, 50.629055]
x3 = [3.028279, 50.629035]
# A executer pour mettre faux
#update_station_activity_by_zone(x0, x1, x2, x3, False)

# A reexécuter pour mettre True
#update_station_activity_by_zone(x0, x1, x2, x3, True)

# ----------------------------------------------------------------
# Donne le nombre de station avec un nombre total sous


def give_ration(ratio):
    maxplaces = 20
    places = int(maxplaces*maxplaces/100)
    for station in collec.find({"size": {"$lt": places}}):
        pprint(station)


# give_ration(20)
