import textwrap
import streamlit
import numpy as np

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

def render_four_hands(list_of_hands, hidden_hands = "",
        dealer_string = "S", auction_string = ""):
    """
    Render four hands with auction as a string representation.

    Parameters:
    --------------        
    list_of_hands, shape (4,)
        N, W, S, E hands.
        each hand is a list of cards, e.g. ["CA", "D4", ...] 
    hidden_hands (str) e.g. "NE" or "" or "NSEW"
        hands to hide, specified as characters N, S, E, or W.
    dealer_string (string) e.g. "S"
    auction_string (string) e.g. "P P 1H P P 2H P P P"

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
    
    # Render the auction as markdown based on auction string and dealer.
    auction_rendered = render_auction(auction_string=auction_string,
            dealer=dealer_string)

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
    <tr style="border: none" height="33%">
        <td width="23%" style="border: none"></td>
        <td width="23%" style="border: none">{}</td>  
        <td width="23%" style="border: none"></td>
        <td width="30%" style="border: none">{}</td>
    </tr>
    <tr style="border: none" height="33%">
        <td width="23%" style="border: none">{}</td>
        <td width="23%" style="border: none"></td>  
        <td width="23%" style="border: none">{}</td>
        <td width="30%" style="border: none"></td>
    </tr>
    <tr style="border: none" height="33%">
    </tr>
        <td width="23%" style="border: none"></td>
        <td width="23%" style="border: none">{}</td>  
        <td width="23%" style="border: none"></td>
        <td width="30%" style="border: none"></td>
    </table>
    """.format(north_hand_rendered, auction_rendered, west_hand_rendered, 
            east_hand_rendered, south_hand_rendered)

    # Remove extraneous line break at the left of the rendered hands.
    rendered_hands = rendered_hands.lstrip("\n")

    # For HTML rendering convert " " -> nbsp and "\n" -> br
    rendered_hands = rendered_hands.replace("\n", "<br>")

    return rendered_hands 

def render_four_hands_with_question(list_of_hands, question="", hidden_hands="",
        dealer_string="S", auction_string=""):
    """
    Render four hands as a string, with optional question

    Parameters:
    -------------
    list_of_hands, shape (4,)
        N, W, S, E hands.
        each hand is a list of cards, e.g. ["CA", "D4", ...]
    context (string). Description of context.
        e.g. "Contract: 4S. West leads the club king. You win and play 
        which suit from dummy?"
    hidden_hands (string) e.g. "" or "NSWE" or "NS"
    dealer_string (string) e.g. "S"
    auction_string (string) e.g. "P P 1H P 2H P P P "

    Returns:
    --------------
    None
    """

    # Render the four hands as a hand diagram (string).
    rendered_hands = render_four_hands(list_of_hands=list_of_hands,
            hidden_hands=hidden_hands, dealer_string=dealer_string,
            auction_string=auction_string)

    # Add the optional question below with leading whitespace.
    if len(question) > 0:

        question = question.lstrip()
        justified_question = "\n".join(textwrap.wrap(question, 30))
        rendered_hands += ("\n\n" + justified_question)

    return rendered_hands


def render_auction(auction_string, dealer):
    """Render auction from string to markdown 

    Parameters:
    ------------
    auction_string (string) e.g. "P P 1H P 2H P P P"
    dealer (string) N S E or W

    Returns:
    ------------
    auction_markdown (string) e.g.
            N    E    S    W    
            --------------------
            P    P    1H   P
            2H   P    P    P
            P

            Note that "H" here is coded as 
            &#9825, etc.
    """

    # Replace suit letters with symbols. 
    suit_letter_to_symbol = {
            "C" : "&#9827;",
            "D" : "&#9826;",
            "H" : "&#9825;",
            "S" : "&#9824;"
    }
    for suit_letter, suit_symbol in suit_letter_to_symbol.items():
        auction_string = auction_string.replace(suit_letter, suit_symbol)

    # Split the auction into individual bids.
    bids_list = auction_string.rstrip().split()

    # Left-pad the bids with -- to beign the auction with North.
    dealer_to_pad_amount = {
        "N" : 0,
        "E" : 1,
        "S" : 2,
        "W" : 3
    }
    for pad_amount in range(dealer_to_pad_amount[dealer]):
        bids_list.insert(0, "-")

    # Right-pad the auction with - to end with east.
    auction_length_mod_four = len(bids_list) % 4
    remainder_to_pad_amount = {
        0 : 0,
        1 : 3,
        2 : 2,
        3 : 1
    }
    for pad_iteration in range(remainder_to_pad_amount[auction_length_mod_four]):
        bids_list.append("-")
    
    # Reshape the bids list of a rectangular matrix of shape 
    # (nrounds, 4). This is possible because the auction has been 
    # left-and right-padded to have length % 4 = 0.
    auction_rounds = int(len(bids_list)/4)
    rectangular_bids_list = np.reshape(bids_list, (auction_rounds, 4))

    # Render the auction as markdown with a header and lines of auction.
    auction_markdown = """
    <table width="100%" style="border-spacing: 0px;">
    <tr style="border : 0">
        <td style="border: none">N</td>
        <td style="border: none">E</td>
        <td style="border: none">S</td>
        <td style="border: none">W</td>
    </tr>
    """
    for auction_row in rectangular_bids_list:
        
        row_markdown = "<tr style='border: none'>\n"
        for bid in auction_row:
            bid_markdown = "<td style='border: none'>" + bid + "</td>\n"
            row_markdown += bid_markdown
        row_markdown += "</tr>\n"

        auction_markdown += row_markdown

    auction_markdown += "</table>"
    print(auction_markdown)

    return auction_markdown

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

    # Render an auction as markdown.
    dealer = "E"
    auction = "1N 2S P 2N P 4S P P P"
    auction = ""
    rendered_auction = render_auction(auction, dealer)
    print(rendered_auction)
