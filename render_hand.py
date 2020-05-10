import textwrap
import streamlit

def render_single_hand(list_of_cards, hidden=False):
    """
    return a string representation of a single hand.

    parameters:
    -------------
    list_of_cards (string []) e.g. ["S9", "C7", "HA"...]
    hidden (boolean) if true, replace the hand with empty string.

    returns:
    --------------
    rendered_hand (string) e.g. 
        S: 972
        H: AJ75
        D: KQT
        C: 976
    """

    CLUB = "&#9827;"
    DIAMOND = "&#9826;"
    HEART = "&#9825;"
    SPADE = "&#9824;"
    
    # In case of a hidden hand, simply return 4 empy lines.
    if hidden:
        return "\n "*4

    # Build a string representation of the hand, one suit at a time.
    rendered_hand = ""
    SORT_ORDER = {
        "A" : 1,    "K" : 2,   "Q" : 3,   "J" : 4,
        "T" : 5,    "9" : 6,   "8" : 7,   "7" : 8,
        "6" : 9,    "5" : 10,   "4" : 11,   "3" : 12,
        "2" : 12
    }
    suit_string_to_markdown = {
            "C" : CLUB, 
            "D": DIAMOND,
            "H" : HEART, 
            "S" : SPADE,
            }
    for suit in ["S", "H", "D", "C"]:

        # Get all cards in this suit, and strip the suit symbol away.
        # E.g. ["9", "2", "K"]
        cards_in_this_suit = [card for card in list_of_cards if card[0] == suit]
        cards_in_this_suit = [card[1:] for card in cards_in_this_suit]
        
        # Sort the cards in this suit in "card" order, e.g. A first, K, .... 2.
        cards_in_this_suit.sort(key=lambda card: SORT_ORDER[card])

        # Add the sorted cards to the rendered_hand.
        this_line = "\n{} ".format(suit_string_to_markdown[suit])
        for card in cards_in_this_suit:
            this_line += card
        rendered_hand += this_line

    return rendered_hand

def render_four_hands(list_of_hands, hidden_hands = ""):
    """
    Render four hands as a string representation.

    Parameters:
    --------------        
    list_of_hands, shape (4,)
        N, W, S, E hands.
        each hand is a list of cards, e.g. ["CA", "D4", ...]
    
    hidden_hands (str) e.g. "NE" or "" or "NSEW"
        hands to hide, specified as characters N, S, E, or W.
    
    Returns: 
    --------------
    rendered_hands  (string)
        This is a full hand diagram.
    """

    # Extract the individual hands from the input, list_of_hands.
    north_hand, west_hand, south_hand, east_hand = list_of_hands
    north_hidden = "N" in hidden_hands
    south_hidden = "S" in hidden_hands
    east_hidden = "E" in hidden_hands
    west_hidden = "W" in hidden_hands
    
    # Render the individual hands, one at a time.
    rendered_hands = ""
    HAND_WIDTH = 10 # number of characters to pad each hand to.
    TEN_WHITESPACE = " "*10

    north_hand_rendered = render_single_hand(north_hand, hidden=north_hidden)
    west_hand_rendered = render_single_hand(west_hand, hidden=west_hidden)
    east_hand_rendered = render_single_hand(east_hand, hidden=east_hidden)
    south_hand_rendered = render_single_hand(south_hand, hidden=south_hidden)

    # Render hands as HTML
    rendered_hands = """
    <table width="600" style="border: none">
    <tr style="border: none">
        <td width="33%" style="border: none"></td>
        <td width="33%" style="border: none">{}</td>  
        <td width="33%" style="border: none"></td>
    </tr>
    <tr style="border: none">
        <td width="33%" style="border: none">{}</td>
        <td width="33%" style="border: none"></td>  
        <td width="33%" style="border: none">{}</td>
    </tr>
    <tr style="border: none">
    </tr>
        <td width="33%" style="border: none"></td>
        <td width="33%" style="border: none">{}</td>  
        <td width="33%" style="border: none"></td>
    </table>
    """.format(north_hand_rendered, west_hand_rendered, east_hand_rendered,
               south_hand_rendered)

    # Remove extraneous line break at the left of the rendered hands.
    rendered_hands = rendered_hands.lstrip("\n")

    # For HTML rendering convert " " -> nbsp and "\n" -> br
    rendered_hands = rendered_hands.replace("\n", "<br>")

    return rendered_hands 

def render_four_hands_with_context(list_of_hands, context="", hidden_hands=""):
    """
    Render four hands as a string, with optional context.

    Parameters:
    -------------
    list_of_hands, shape (4,)
        N, W, S, E hands.
        each hand is a list of cards, e.g. ["CA", "D4", ...]
    context (string). Description of context.
        e.g. "Contract: 4S. West leads the club king. You win and play 
        which suit from dummy?"
    hidden_hands (string) e.g. "" or "NSWE" or "NS"

    Returns:
    --------------
    None
    """

    # Render the four hands as a hand diagram (string).
    rendered_hands = render_four_hands(list_of_hands=list_of_hands,
            hidden_hands=hidden_hands)

    # Add the optional context below with leading whitespace.
    if len(context) > 0:

        context = context.lstrip()
        justified_context = "\n".join(textwrap.wrap(context, 30))
        rendered_hands += ("\n\n" + justified_context)

    return rendered_hands


if __name__ == "__main__":

    """
    This is legacy code to test this module in the command line.
    TODO, this should eventually be refactored into proper unit tests.
    """

    # Render one hand.
    hand = ["CA", "C4", "C3", "C2", "CJ", "DJ", "D6", "D3", "S7", "S6", "S4", "HT", "H8"]
    rendered_hand = render_single_hand(hand, hidden=False)
    #print(rendered_hand)

    # Render four hands.
    north_hand = ["CA", "C4", "C3", "C2", "CJ", "DJ", "D6", "D3", "S7", "S6", "S4", "HT", "H8"]
    south_hand = ["SA", "SK", "S5", "HJ", "H9", "H4", "DA", "DK", "DQ", "DJ", "DT", "D6", "CA"]
    west_hand = ["SQ", "S9", "S6", "S4", "H8", "H7", "H2", "D8", "D4", "D2", "C9", "C7", "C2"]
    east_hand = ["SJ", "S7", "S2", "HA", "H6", "H3", "D9", "D3", "CK", "CT", "C6", "C5", "C2"]
    list_of_hands = [north_hand, west_hand, south_hand, east_hand]

    rendered_hands = render_four_hands(list_of_hands)
    for hidden_hands in ["N", "S", "E", "W", "", "NS"]:
        print(hidden_hands)
        rendered_hands = render_four_hands(list_of_hands, hidden_hands)
        print(rendered_hands)

    # Render the same four hands, with context.
    context = """
    Contract: 4S. You win the CK lead in dummy and play which suit?
    """
    hidden_hands = "SE"
    rendered_hands_with_context = render_four_hands_with_context(
            list_of_hands=list_of_hands,
            context=context,
            hidden_hands=hidden_hands)
    print(rendered_hands_with_context)

