"""
CLI to add new hands to the dataset efficienctly.
"""

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
        "hand_id" : 1
        }
    """

    # Json representation of the hand, to be build in stages.
    hand_json = {}

    # Query the needed information.
    keys = ["n_hand", "s_hand", "w_hand", "e_hand", "context", "correct_answer", "notes"]
    labels = ["North Hand (e.g. T83 KQT5 75 QJ38)",
              "South Hand (e.g. AK5 J94 AKQJT6 A)",
              "West Hand (e.g. Q964 872 842 972)",
              "East Hand (e.g. J72 A63 93 KT652)",
              "Context (optional) e.g. contract and play",
              "Correct Answer (case sensititive) e.g. H9 or H",
              "Notes (optional) e.g. From Bridgemaster Level 2 Problem 7"
            ]
    for key, label in zip(keys, labels):

        value = user_input(label)
        hand_j[key] = value

    return hand_json


if __name__ == "__main__":

    hand_str = "T83 KQT5 75 QJ83"
    hand_list = parse_hand_string_to_list(hand_str)
    print(hand_list)
