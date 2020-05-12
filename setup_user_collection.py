import pymongo
import json 

# Load "hands" collection.
client = pymongo.MongoClient()
db = client["bridge_problem_database"]
user_collection = db["user"]
user_collection.drop() # drop if already exists.

# Add guest and Robert users.
guest_user = {
    "username" : "guest",
    "elo" : 1200}
robert_user = {
    "username" : "robert",
    "elo" : 1300
}
user_collection.insert_one(guest_user)
user_collection.insert_one(robert_user)
