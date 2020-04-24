import json 
import numpy as np
from render_hand import render_four_hands_with_context_and_ask_for_answer

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

def ask_see_another_hand_or_quit():
    """ 
    ask the user whether they want to see another hand or quit. 
    
    parameters: none
    returns: True if the user wants to see another hand.
    """

    # Ask the user whether they want to see another hand.
    msg = "See another hand? y/n"
    user_input = ""
    while user_input not in ["y", "n"]:
        user_input = input(msg)

    # Return True if user wants to see another hand.
    return (user_input == "y")

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
    hand_indices = np.arange(len(hands), dtype=np.int8)
    np.random.shuffle(hand_indices)

    # Show hands in random order until the user asks to stop.
    for hand_index in hand_indices:

        # Ask the user if they want to see another hand.
        user_wants_to_see_another_hand = ask_see_another_hand_or_quit()
        if not user_wants_to_see_another_hand:
            break

        # Show the hand.
        hand_json = hands[hand_index]
        list_of_hands = [
                hand_json["n_hand"],
                hand_json["w_hand"],
                hand_json["s_hand"],
                hand_json["e_hand"]
                ]
        context = hand_json["context"]
        correct_answer = hand_json["correct_answer"]
        render_four_hands_with_context_and_ask_for_answer(list_of_hands, 
                context, correct_answer)

    # Done message.
    print("Done!")

    return None

if __name__ == "__main__":

    hands = load_hands() 
    show_hands_continuously(hands)
