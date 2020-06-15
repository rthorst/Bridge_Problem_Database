"""
CLI to add new hands to the dataset efficienctly.
"""
import json
import os
import pymongo
import bson

def edit_hands_wrapper():

    # Load existing hands.
    client = pymongo.MongoClient()
    db = client["bridge_problem_database"]
    hands_collection = db["hands"]

    for hand in hands_collection.find({}):

        hand_id_to_edit = hand["_id"]

        print(hand["question"])
        hidden_hands = input("hidden hands?")
        print(hidden_hands)

        query = {"_id" : hand_id_to_edit} # update rows matching this query.
        update = {"$set" : {"hidden_hands" : hidden_hands}} # update to perform.

        hands_collection.update_one(query, update)

edit_hands_wrapper()
