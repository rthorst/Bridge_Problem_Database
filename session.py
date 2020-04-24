import json 
import numpy as np


def load_hands(hands_p="hands.json"):
    """
    Load hands as a list of json objects.

    Input: hands_p (string) path to json hands file.
    Output: hands, json[]. Example:

       "n_hand" : ["SQ", "S6", "S2", "HA", "HK", "H6", "H2", "DA", "DQ", "D5", "CK", "C3", "C2"],
       "s_hand" : ["SA", "SK", "SJ", "ST", "S5", "HQ", "H7", "H3", "D7", "D4", "C8", "C7", "C5"],
       "w_hand" : ["S9", "S8", "S3", "HT", "H5", "DJ", "D9", "D8", "D6", "D3", "CJ", "C9", "C6"],
       "e_hand" : ["S7", "S4", "HJ", "H9", "H8", "H4", "DK", "DT", "D2", "CA", "CQ", "CT", "C4"],
       "context" : "Contract: 4 spades. You draw trumps in three rounds and play three top hearts ending in dummy, East having 4H. Which suit do you play next?",
       "correct_answer" : "H"
    """

    # Load list of hands.
    hands_str = open(hands_p, "r").read()
    hands_json = json.loads(hands_str)

    return hands_json

def show_hands_continuously(hands):
    """
    Continuously show hands to the user until the user asks to quit or hands run out.

    Parameters: hands: json[]
       
       Example:
       "n_hand" : ["SQ", "S6", "S2", "HA", "HK", "H6", "H2", "DA", "DQ", "D5", "CK", "C3", "C2"],
       "s_hand" : ["SA", "SK", "SJ", "ST", "S5", "HQ", "H7", "H3", "D7", "D4", "C8", "C7", "C5"],
       "w_hand" : ["S9", "S8", "S3", "HT", "H5", "DJ", "D9", "D8", "D6", "D3", "CJ", "C9", "C6"],
       "e_hand" : ["S7", "S4", "HJ", "H9", "H8", "H4", "DK", "DT", "D2", "CA", "CQ", "CT", "C4"],
       "context" : "Contract: 4 spades. You draw trumps in three rounds and play three top hearts ending in dummy, East having 4H. Which suit do you play next?",
       "correct_answer" : "H"
    
    Returns:  None
    """

    # Randomize order of showing hands.
    indices = np.arange(len(hands), dtype=np.int8)
    np.random.shuffle(indices)
    print(indices)

if __name__ == "__main__":

    hands = load_hands() 
    show_hands_continuously(hands)
