"""
CLI to add new hands to the dataset efficienctly.
"""
import json
import os

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

    NOT_13_CARDS_ERROR_MSG = "hand cannt be parsed into 13 cards"
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

    # Validate context and correct answer, which simply must be strings.
    elif key in ["context", "correct_answer"]:
        assert type(value) == type("aa"), NOT_STRING_ERROR
        parsed_value = value

    # Validate hand ID, which simply must be integer.
    elif key in ["hand_id"]:
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
        "hand_id" : 1,
        "hidden_hands" : "NS"
        }
    """

    # Json representation of the hand, to be build in stages.
    hand_json = {}

    # Query the needed information.
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
    data_p = os.path.join("data", "hands.json")
    f = open(data_p, "r")
    hands_json = json.loads(f.read())

    # Back up the old hands.
    os.system("cp data/hands.json data/hands_backup.json")

# While user wants to keep entering hands, enter one 
    # and assign it the next numerical ID.
    done = False
    last_hand_id = hands_json[-1]["hand_id"]
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

        # Assign the current hand the next numerical ID in sequence.
        hand_json["hand_id"] = last_hand_id + 1
        last_hand_id += 1

        # Add this new hand to the data structure containing all hands.
        hands_json.append(hand_json)

        # Write the updated hands to the dataset.
        with open("data/hands.json", "w") as of:
            out = json.dumps(hands_json)
            of.write(out)

        # Update the user on how many hands are currently in the database.
        print("Hands currently in the database: ", len(hands_json))

if __name__ == "__main__":

    hand_str = "T83 KQT5 75 QJ83"
    hand_list = parse_hand_string_to_list(hand_str)
    #print(hand_list)

    #hand_json = ask_for_hand()
    #print(hand_json)

    enter_hands_wrapper()
