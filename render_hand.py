import textwrap

def render_single_hand(list_of_cards):
    """
    return a string representation of a single hand.

    input:
        list_of_cards (string []) e.g. ["S9", "C7", "HA"...]

    returns:
        rendered_hand (string) e.g. 
        S: 972
        H: AJ75
        D: KQT
        C: 976
    """

    # Build the representation one suit at a time.
    rendered_hand = ""
    SORT_ORDER = {
        "A" : 1,    "K" : 2,   "Q" : 3,   "J" : 4,
        "T" : 5,    "9" : 6,   "8" : 7,   "7" : 8,
        "6" : 9,    "5" : 10,   "4" : 11,   "3" : 12,
        "2" : 12
    }
    for suit in ["S", "H", "D", "C"]:

        # Get all cards in this suit.
        cards_in_this_suit = [card for card in list_of_cards if card[0] == suit]

        # Strip the suit symbol away
        cards_in_this_suit = [card[1:] for card in cards_in_this_suit]
        
        # Sort the cards in "card" order, e.g. A, K, Q, ..T, 9, ...2.
        cards_in_this_suit.sort(key=lambda card: SORT_ORDER[card])

        # Add the sorted cards to the string hand.
        this_line = "\n{}: ".format(suit)
        for card in cards_in_this_suit:
            this_line += card
        rendered_hand += this_line

    return rendered_hand

def render_four_hands(list_of_hands):
    """
    Render four hands in string representation.

    Input:
        list_of_hands, shape (4,)
        N, W, S, E hands.
        each hand is a list of cards, e.g. ["CA", "D4", ...]
    Output: rendered_hands  (string)
    """

    # Parse input hands.
    north_hand, west_hand, south_hand, east_hand = list_of_hands
    
    # Render the hands one at a time.
    rendered_hands = ""
    HAND_WIDTH = 10 # number of characters to pad each hand to.
    TEN_WHITESPACE = " "*10

    # North.
    north_hand_rendered = render_single_hand(north_hand)
    for line in north_hand_rendered.split("\n"):
        line = line.ljust(HAND_WIDTH)
        rendered_hands += ("\n" + TEN_WHITESPACE + line + TEN_WHITESPACE)
        
    # West and East. 
    west_hand_rendered = render_single_hand(west_hand)
    east_hand_rendered = render_single_hand(east_hand)
    for west_line, east_line in zip(west_hand_rendered.split("\n"), 
            east_hand_rendered.split("\n")):
        west_line = west_line.ljust(HAND_WIDTH)
        east_line = east_line.ljust(HAND_WIDTH)
        rendered_hands += ("\n" + west_line + TEN_WHITESPACE + east_line)
    
    # South.
    south_hand_rendered = render_single_hand(south_hand)
    for line in south_hand_rendered.split("\n"):
        line = line.ljust(HAND_WIDTH)
        rendered_hands += ("\n" + TEN_WHITESPACE + line + TEN_WHITESPACE)

    return rendered_hands 

def render_four_hands_with_context(list_of_hands, context=""):
    """
    Render four hands as a string, with optional context.

    Input:
        list_of_hands, shape (4,)
        N, W, S, E hands.
        each hand is a list of cards, e.g. ["CA", "D4", ...]

        context (string). Description of context.
        e.g. "Contract: 4S. West leads the club king. You win and play which suit from dummy?"
    """

    # Render the four hands as a hand diagram (string).
    rendered_hands = render_four_hands(list_of_hands)

    # Add the optional context.
    if len(context) > 0:

        context = context.lstrip()
        justified_context = "\n".join(textwrap.wrap(context, 30))
        rendered_hands += ("\n\n" + justified_context)

    return rendered_hands

def ask_for_answer(correct_answer):
    """
    Ask the user for an answer and return whether the answer is correct.

    Parameters:
        correct_answer (string)

    Returns:
        user_answer (string)
    """
    
    # Ask the user for an answer.
    msg = "\nYour Answer: "
    user_answer = input(msg)
    
    return user_answer

def provide_feedback(user_answer, correct_answer):
    """
    Provide feedback to the shell.

    Parameters:
        user_answer (string)
        correct_answer (string)

    Return true if user_answer == correct_answer.
    """

    if user_answer == correct_answer:
        msg = "Correct!"
    else:
        msg = "Incorrect! Correct answer is {}".format(correct_answer)
        msg = "\n".join(textwrap.wrap(msg, 30))
    
    print(msg)
    
    return None

def render_four_hands_with_context_and_ask_for_answer(list_of_hands, context, correct_answer):
    """
    Parameters:
        
        list_of_hands, shape (4,)
        N, W, S, E hands.
        each hand is a list of cards, e.g. ["CA", "D4", ...]

        context (string). Description of context.
        e.g. "Contract: 4S. West leads the club king. You win and play which suit from dummy?"
    
        correct_answer (string). Correct answer.

    Returns None
    """
    rendered_hands_with_context = render_four_hands_with_context(
            list_of_hands, context)
    print(rendered_hands_with_context)

    user_answer = ask_for_answer(correct_answer)
    provide_feedback(user_answer, correct_answer)

    return None

if __name__ == "__main__":

    # Render one hand.
    hand = ["CA", "C4", "C3", "C2", "CJ", "DJ", "D6", "D3", "S7", "S6", "S4", "HT", "H8"]
    rendered_hand = render_single_hand(hand)
    #print(rendered_hand)

    # Render four hands.
    north_hand = ["CA", "C4", "C3", "C2", "CJ", "DJ", "D6", "D3", "S7", "S6", "S4", "HT", "H8"]
    south_hand = ["SA", "SK", "S5", "HJ", "H9", "H4", "DA", "DK", "DQ", "DJ", "DT", "D6", "CA"]
    west_hand = ["SQ", "S9", "S6", "S4", "H8", "H7", "H2", "D8", "D4", "D2", "C9", "C7", "C2"]
    east_hand = ["SJ", "S7", "S2", "HA", "H6", "H3", "D9", "D3", "CK", "CT", "C6", "C5", "C2"]
    list_of_hands = [north_hand, west_hand, south_hand, east_hand]

    rendered_hands = render_four_hands(list_of_hands)
    #print(rendered_hands)

    # Render the same four hands, with context.
    context = """
    Contract: 4S. You win the CK lead in dummy and play which suit?
    """
    rendered_hands_with_context = render_four_hands_with_context(list_of_hands, context)
    #print(rendered_hands_with_context)

    # Ask for an answer.
    correct_answer = "H"
    render_four_hands_with_context_and_ask_for_answer(list_of_hands,
            context, correct_answer)
