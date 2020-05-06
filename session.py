import json 
import numpy as np
from render_hand import render_four_hands_with_context_and_ask_for_answer
import sqlite3
import elo
import pymongo

def initialize_elo_table():
    """
    Create the elo table if it does not exist.

    Returns None.
    """

    # Connect to database file, creating if not exists.
    conn = sqlite3.connect("data/bridge_problems.sqlite")

    # Create hand ELO table if not exists.
    conn.execute("""
    create table if not exists hand_elo (
        hand_id serial primary key,
        elo integer
    );
    """)

    return None

def show_hand_header(player_elo, hand_elo, hand_id):
    """
    Display a brief header for each hand, retuning None.
    """

    DIVIDER = "="*30
    msg = DIVIDER + "\n"
    msg += "Hand id: {:.0f}\n".format(hand_id)
    msg += "Your elo: {:.0f} Hand elo {:.0f}\n".format(
            player_elo, hand_elo)
    msg += DIVIDER
    print(msg)

    return None

def load_hands():
    """
    Load hands as a list of json objects.

    Output: hands, json[]. Example:

       "n_hand" : ["SQ", "S6", "S2", "HA", "HK", "H6", "H2", "DA", "DQ", "D5", "CK", "C3", "C2"],
       "s_hand" : ["SA", "SK", "SJ", "ST", "S5", "HQ", "H7", "H3", "D7", "D4", "C8", "C7", "C5"],
       "w_hand" : ["S9", "S8", "S3", "HT", "H5", "DJ", "D9", "D8", "D6", "D3", "CJ", "C9", "C6"],
       "e_hand" : ["S7", "S4", "HJ", "H9", "H8", "H4", "DK", "DT", "D2", "CA", "CQ", "CT", "C4"],
       "context" : "Contract: 4 spades. You draw trumps in three rounds and play three top hearts ending in dummy, East having 4H. Which suit do you play next?",
       "correct_answer" : "H",
       "hand_id" : 1
"""

    # Connect to PyMongo database.
    client = pymongo.MongoClient()
    db = client["bridge_problem_database"]
    hands_collection = db["hands"]
    
    # Get all hands as a list of JSON objects.
    all_hands = hands_collection.find({})
    hands_json = list(all_hands)
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

def get_hand_elo(hand_id, conn):
    """
    Lookup hand ELO for a given hand ID, creating if not exists.

    Parameters:
        hand_id (integer) e.g. 2
        conn (sqlite3 connection object)

    Returns: 
        elo (integer) e.g. 1200
    """

    # Look up ELO for this hand.
    get_elo_statement = """
    select elo from hand_elo where hand_id = {}
    """.format(hand_id)
    res = conn.execute(get_elo_statement).fetchall()

    # If the ELO does not already exist, create it.
    if len(res) == 0:

        # Insert 1200 ELO for this hand into database.
        insert_statement = """
        insert into hand_elo (hand_id, elo) values ({}, {})
        """.format(hand_id, 1200)
        conn.execute(insert_statement)
        conn.commit()

        return 1200

    # Otherwise, return the existing ELO for this hand.
    return res[0][0]

def show_hands_continuously(hands, conn, player_elo=1200):
    """
    Continuously show hands to the user until the user asks to quit or hands run out.

    Parameters: hands: json[]
       
       Example:
       "n_hand" : ["SQ", "S6", "S2", "HA", "HK", "H6", "H2", "DA", "DQ", "D5", "CK", "C3", "C2"],
       "s_hand" : ["SA", "SK", "SJ", "ST", "S5", "HQ", "H7", "H3", "D7", "D4", "C8", "C7", "C5"],
       "w_hand" : ["S9", "S8", "S3", "HT", "H5", "DJ", "D9", "D8", "D6", "D3", "CJ", "C9", "C6"],
       "e_hand" : ["S7", "S4", "HJ", "H9", "H8", "H4", "DK", "DT", "D2", "CA", "CQ", "CT", "C4"],
       "context" : "Contract: 4 spades. You draw trumps in three rounds and play three top hearts ending in dummy, East having 4H. Which suit do you play next?",
       "correct_answer" : "H",
       "hand_id" : 1
    
        conn: sqlite3 connection object

        player_elo (int) e.g. 1200: player starting ELO.

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

        # Get data for this hand.
        hand_json = hands[hand_index]
        hand_id = hand_json["hand_id"]
        hand_elo = get_hand_elo(hand_id, conn)

        # Show information about the hand.
        show_hand_header(
                player_elo=player_elo,
                hand_elo=hand_elo,
                hand_id=hand_id
                )

        # Show the hand.
        list_of_hands = [
                hand_json["n_hand"],
                hand_json["w_hand"],
                hand_json["s_hand"],
                hand_json["e_hand"]
                ]
        context = hand_json["context"]
        correct_answer = hand_json["correct_answer"]
        hidden_hands = hand_json["hidden_hands"]
        user_was_correct = render_four_hands_with_context_and_ask_for_answer(
                list_of_hands=list_of_hands, 
                context=context,
                correct_answer=correct_answer,
                hidden_hands=hidden_hands)

        # Calculate new player and hand ELO scores.
        new_player_elo, new_hand_elo = elo.get_new_elos(
                player_elo, hand_elo, user_was_correct
                )
   
        # Update hand ELO in the database.
        conn.execute("""
        update hand_elo set elo = {} where
        hand_id = {}""".format(new_hand_elo, hand_id)
        )
        conn.commit()

    # Done message.
    print("Done!")

    return None

def run_session():
    """
    wrapper function to run an entire session.
    """

    # Load hands in JSON format.
    hands = load_hands()

    # Connect to the SQL database, creating if it doesn't exist, 
    conn = sqlite3.connect("data/bridge_problems.sqlite")
    
    # Initialize ELO table.
    initialize_elo_table()

    # Show hands continuously to the user.
    show_hands_continuously(hands, conn)

if __name__ == "__main__":

    run_session()
