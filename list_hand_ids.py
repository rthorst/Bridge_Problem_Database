"""
CLI to add new hands to the dataset efficienctly.
"""
import json
import os
import pymongo
import bson

def list_hand_ids():
    """ wrapper function to enter hands """

    # Load existing hands.
    client = pymongo.MongoClient()
    db = client["bridge_problem_database"]
    hands_collection = db["hands"]

    for hand in hands_collection.find():

        print(hand["_id"])
        print(hand["question"])
        print(hand)

list_hand_ids()
