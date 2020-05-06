"""
CLI to add new hands to the dataset efficienctly.
"""
import json
import os
import pymongo
import bson

def parse_hand_string_to_list(hand_str):
    """
    Parse a hand string (AKJ, QJ...) to list ["SA", ...]

    Parameters:
        hand_str (string) e.g. AKJ QJT9 752 9842

    Returns:
        hand_list (string []) e.g. ["SA", ..., "C2"]
    """

    # Split the hand into strings of cards in each suit.
    hand_strs_by_suit = hand_str.split(" ")
    NOT_4_SUITS_ERROR_MSG = "hand cannot be parsed into 4 suits"
    assert len(hand_strs_by_suit), NOT_4_SUITS_ERROR_MSG

    # Build the hand list (e.g. ["SA", .... "C2"])
    hand_list = []
    suit_prefixes = ["S", "H", "D", "C"]
    for suit_prefix, cards_str in zip(suit_prefixes, hand_strs_by_suit):
        for card_str_without_suit in cards_str:

            card_str_with_suit = suit_prefix + card_str_without_suit
            hand_list.append(card_str_with_suit)

    NOT_13_CARDS_ERROR_MSG = "hand cannot be parsed into 13 cards"
    assert len(hand_list) == 13, NOT_13_CARDS_ERROR_MSG

    return hand_list

def validate_and_parse(key, value):
    """
    Validate and parse a given (key, value) pair.
    If vaild, return the parsed value.
    Otherwise, raise a descriptive exception.

    Parameters:
        key (string) e.g. "n_hand"
        value (flexible type) e.g. "KQT AJ54 932 872"
    Returns: 
        parsed_value (flexible type) the parsed representation of the value.
        If invalid, instead returns None and raises an Exception.
    """

    # Possible exceptions to raise.
    NOT_STRING_ERROR = "a string is required"
    NOT_INTEGER_ERROR = "an integer is required"
    INVALID_HIDDEN_HANDS_ERROR = """
    hidden hands can include only the letters NSEW
    """
    INVALID_KEY_ERROR = "key not understood"

    # Validate hands: check it can be parsed into 4 suits with 13 cards.
    if key in ["n_hand", "s_hand", "w_hand", "e_hand"]:
        # This function will raise an exception if the hand is invalid.
        parsed_value = parse_hand_string_to_list(value)
    
    # Validate hidden hands: string with NSEW only.
    elif key == "hidden_hands":
    
        # check for string.
        assert type(value) == type("aa"), NOT_STRING_ERROR
    
        # check only characters are NSEW.
        for c in value:
            assert c.lower() in 'nsew', INVALID_HIDDEN_HANDS_ERROR

        # parsed_value is simply a copy of the inputted value.
        parsed_value = value

    # Validate keys which simply must be strings.
    elif key in ["context", "correct_answer", "notes", "hand_id"]:
        assert type(value) == type("aa"), NOT_STRING_ERROR
        parsed_value = value
    

    # Validate integer-keys, currently just the ELO key.
    elif key in ["elo"]:
        assert type(value) == type(1), NOT_INTEGER_ERROR
        parsed_value = value

    # Unrecognized keys.
    else:
        raise Exception(INVALID_KEY_ERROR)

    return parsed_value
        

def ask_for_hand():
    """
    Ask user to enter a hand on the command line and return
    the hand as JSON.

    Parameters: None
    Returns: hand_json
        E.g.
        {
        "n_hand" : ["SQ", "S6", "S2", "HA", "HK", "H6", "H2", "DA", "DQ", "D5", "CK
        ", "C3", "C2"],
        "s_hand" : ["SA", "SK", "SJ", "ST", "S5", "HQ", "H7", "H3", "D7", "D4", "C8",
        "C7", "C5"],
        "w_hand" : ["S9", "S8", "S3", "HT", "H5", "DJ", "D9", "D8", "D6", "D3", "CJ",
        "C9", "C6"],
        "e_hand" : ["S7", "S4", "HJ", "H9", "H8", "H4", "DK", "DT", "D2", "CA", "CQ",
        "CT", "C4"],
        "context" : "Contract: 4 spades. You draw trumps in three rounds and play 
        three top hearts ending in dummy, East having 4H. Which suit do you play next?",
        "correct_answer" : "H",
        "_id" : hexadecimal hand ID,
        "hidden_hands" : "NS",
        "elo" : 1200
        }
    """

    # Json representation of the hand, to be build in stages.
    hand_json = {}

    # Query the needed information.
    # Note that we assign a default ELO of 1200 to the hand
    # rather than allow the user to enter this information.
    keys = ["n_hand", "s_hand", "w_hand", "e_hand", "context",
            "correct_answer", "hidden_hands", "notes"]
    labels = ["North Hand (e.g. T83 KQT5 75 QJ38):  ",
              "South Hand (e.g. AK5 J94 AKQJT6 A):  ",
              "West Hand (e.g. Q964 872 842 972):  ",
              "East Hand (e.g. J72 A63 93 KT652):  ",
              "Context (optional) e.g. contract and play:  ",
              "Correct Answer (case sensititive) e.g. H9 or H:  ",
              "Hidden Hands (optional) e.g. NSE or enter to continue:  ",
              "Notes (optional) e.g. From Bridgemaster Level 2 Problem 7:  "
            ]
    for key, label in zip(keys, labels):

        # Get input from the user.
        value = input(label)

        # Validate and parse the input provided by user.
        # If the value is invalid or the key is unrecognized, a
        # discriptive exception will be raised. Otherwise, appropriate
        # parsing will be performed, for example parsing the hand into 
        # a listof 13 cards.
        value = validate_and_parse(key, value)

        # Add input to the json representation of the hand.
        hand_json[key] = value

    return hand_json

def enter_hands_wrapper():
    """ wrapper function to enter hands """

    # Load existing hands.
    client = pymongo.MongoClient()
    db = client["bridge_problem_database"]
    hands_collection = db["hands"]

    # While user wants to keep entering hands, enter one 
    done = False
    while not done:

        # Ask the user if they want to enter another hand.
        continue_input = ""
        while continue_input not in ["y", "n"]:
            continue_input = input("Enter another hand? y/n:  ")
            continue_input = continue_input.lower() # case insensitive.
        if continue_input == "n":
            done = True
            break

        # Have the user enter the new hand, and parse the
        # results as a json. 
        hand_json = ask_for_hand()

        # Add the new hand to the MongoDB database.
        hands_collection.insert_one(hand_json)

        # Update the user on how many hands are currently in the database.
        print("Hands currently in the database: ", 
                hands_collection.count_documents({}))


def edit_hands_wrapper():

    # Load existing hands.
    client = pymongo.MongoClient()
    db = client["bridge_problem_database"]
    hands_collection = db["hands"]

    # Ask the user if they want to make another change.
    # While they want to make changes, accept changes one 
    # at a time and commit them to the database.
    done = False
    while not done:

        # Ask the user if they want to make another change.
        wants_to_continue = None
        while wants_to_continue not in ["y", "n"]:
                wants_to_continue = input("keep editing hands? y/n:  ")
        if wants_to_continue == "n":
            done = True
            break

        # Ask which hand to edit.
        hand_id_to_edit = input("which hand id would you like to edit?:  ")
        hand_id_to_edit = bson.objectid.ObjectId(hand_id_to_edit)

        # Need to list valid hand IDs from mongo db.
        INVALID_HAND_ID_ERROR = "hand id does not exist"
        HAND_ID_EXISTS = (type(hands_collection.find_one({"_id" : hand_id_to_edit})) 
                == type({"a": "b"}))
        assert HAND_ID_EXISTS, INVALID_HAND_ID_ERROR
        
        # Ask which key to edit.
        key_to_edit = input("which key would you like to edit?:  ")
        valid_keys = ["n_hand", "s_hand", "e_hand", "w_hand", "context", "notes", "correct_answer"]
        INVALID_KEY_ERROR = "key cannot be understood as one of ".format(valid_keys)
        assert key_to_edit in valid_keys, INVALID_KEY_ERROR

        # Show the old value of this key.
        OLD_KEY_VALUE = hands_collection.find_one(
            {"_id" : hand_id_to_edit}, # filter by
            {key_to_edit : 1, "_id": 0} # return fields where value = 1.
            )[key_to_edit]
        
        OLD_VALUE_MSG = "The old value of this key was: {}".format(OLD_KEY_VALUE)
        print(OLD_VALUE_MSG)

        # Prompt user for the new value associated with this key,
        # and validate/parse the new value.
        # this will raise an exception if invalid, otherwise, the 
        # parsed representation will be returned.
        new_value = input("What should the new value be?:  ")
        new_value = validate_and_parse(key_to_edit, new_value)

        # Update the relevant record in the database.
        query = {"_id" : hand_id_to_edit} # update rows matching this query.
        update = {"$set" : {key_to_edit : new_value}} # update to perform.

        hands_collection.update_one(query, update)

def ask_to_add_or_edit():
    """
    Ask user whether they want to add a new hand or edit existing hands,
    this serves as a wrapper around the main functions in this module, 
    enter_hands_wrapper() and edit_hands_wrapper()
    
    Returns None
    """

    desired_task = None
    while desired_task not in ["a", "e", "q"]:
        PROMPT = """
        Would you like to add a new hand [a],
        edit an existing hand [e], 
        or quit [q]? 
        Enter a, e, or q:\n
        """
        desired_task = input(PROMPT)

    if desired_task == "a": # add new hand
        enter_hands_wrapper()
    elif desired_task == "e": # edit hand.
        edit_hands_wrapper()
    else: # "q" , quit.
        return None

if __name__ == "__main__":

    hand_str = "T83 KQT5 75 QJ83"
    hand_list = parse_hand_string_to_list(hand_str)
    #print(hand_list)

    #hand_json = ask_for_hand()
    #print(hand_json)

    #enter_hands_wrapper()
    #edit_hands_wrapper()
    ask_to_add_or_edit()

