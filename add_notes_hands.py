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

if __name__ == "__main__":

    hand_str = "T83 KQT5 75 QJ83"
    hand_list = parse_hand_string_to_list(hand_str)
    print(hand_list)
