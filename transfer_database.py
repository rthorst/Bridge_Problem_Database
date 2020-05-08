import pymongo
import json 

def write_mongodb_to_json():
    
    # Load "hands" collection.
    client = pymongo.MongoClient()
    db = client["bridge_problem_database"]
    hands_collection = db["hands"]

    # Get all records.
    all_hands = list(hands_collection.find({}))
    for hand in all_hands:
        del hand["_id"]
        
    # Write.
    with open("data/hands.json", "w") as of:
        of.write(json.dumps(all_hands))
    
def write_json_to_mongodb():
    


if __name__ == "__main__":
    write_mongodb_to_json()
