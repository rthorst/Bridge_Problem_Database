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
hands_collection.drop() # remove existing hands.

# Load existing hands and remove the ID column,
# since mongo db will automatically assign a new
# _id field.
hands_j = open("data/hands.json", "r").read()
hands_j = json.loads(hands_j)
for j in hands_j:
    del j["hand_id"]

# Add an "elo" field with default value 1200 to each record.
for j in hands_j:
    j["elo"] = 1200

# Add these existing hands to the Mongo DB instance.
hands_collection.insert_many(hands_j)

# Count number of documents.
print("Check number of documents now in the hands table:")
print(hands_collection.count_documents({}))
