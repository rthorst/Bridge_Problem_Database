import pymongo
import json 

# Load "hands" collection.
client = pymongo.MongoClient()
db = client["bridge_problem_database"]
hands_collection = db["hands"]

# Get all hands.
for hand in hands_collection.find():
    if "elo" not in hand.keys():
        
        hand_id = hand["_id"]
        query = {"_id" : hand_id} # update rows matching this query.
        update = {"$set" : {"elo" : 1200}} # update to perform.
        hands_collection.update_one(query, update)


