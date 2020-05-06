"""Convert existing hands.json to a pymongo database.
"""

import json 
import pymongo

# Client connects to the PyMongo instance.
client = pymongo.MongoClient()

# Each PyMongo instance can support many databases.
# Connect to the hands database.
db = client["bridge_problem_database"]

# A table in PyMongo is called a "collection" (of
# documents). Create one to store hands.
hands_collection = db["hands"]
print(hands_collection.count_documents({}))

"""
# Insert a hand into the database.
hands_j = open("data/hands.json", "r").read()
hands_j = json.loads(hands_j)
hands_collection.insert_many(hands_j)
"""

