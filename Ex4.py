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

#recherche("Planetes")
##update


#delete station
#ne marche pas ??

def remove_station(nom):
	collec.deleteMany({"name":nom})
#remove_station("Planetes")
#recherche("Planetes")
#deactivate

#give ratio

'''c est un programe un peu nul, il part du principe que 
les stations font toute 20 places et cherche les sizes plus petites
que 20 * ratio /100 
 c est le bon query mais faudra changer la bdd pour reelement faire l'exo'''
def give_ration(ratio):
	maxplaces=20
	places=int(maxplaces*maxplaces/100)
	for station in collec.find({"size": { "$lt": places}}):
		pprint(station)
give_ration(20)