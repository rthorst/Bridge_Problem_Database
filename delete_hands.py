"""
CLI to add new hands to the dataset efficienctly.
"""
import json
import os
import pymongo
import bson

def delete_hands():

    # Load existing hands.
    client = pymongo.MongoClient()
    db = client["bridge_problem_database"]
    hands_collection = db["hands"]

    hands_collection.delete_many({})

if __name__ == "__main__":
    delete_hands()
