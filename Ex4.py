import requests
import json
import pymongo
from pprint import pprint
from pymongo import MongoClient
from pymongo import TEXT

atlas = MongoClient(
    'mongodb+srv://dbUser:isen123@cluster0.cndhu.mongodb.net/bicycle?retryWrites=true&w=majority')
bdd = atlas.get_database('bicycle')
collec = bdd.stations

#get with letters in name

collec.create_index([("name", TEXT)])
def recherche(txt):
	for station in collec.find({"$text": {"$search": txt,"$caseSensitive":False}}):
		pprint(station)

recherche("Planetes")
##update


#delete station
def remove_station(nom):
	collec.deleteMany({"name":nom})
remove_station("Planetes")
recherche("Planetes")
#deactivate

#give ratio