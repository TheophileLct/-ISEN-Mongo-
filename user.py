
#repond à la question 3:
from pprint import pprint
from pymongo import MongoClient,GEOSPHERE


client = MongoClient('localhost', 27017)
db=client.test_database
#j ai pas le nom de la base de donnée :((
collection=db.test_collection
pprint(collection.find_one())

"""class user:
	def __init__(self):
		self.name="billy"
		self.position=[0,0]

	def station_proche(self):
		query = {"loc": SON([("$near", self.position), ("$maxDistance", 100)])}
		for station in db.???.find(query).limit(2):
			pprint(station)"""