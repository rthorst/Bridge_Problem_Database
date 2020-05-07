import json 
import numpy as np
from render_hand import render_four_hands_with_context
import sqlite3
import elo
import pymongo
import streamlit

def show_hand_header(player_elo, hand_json, header_widget):
    """
    Display a brief header for each hand, retuning None.
    """

    hand_elo = hand_json["elo"]
    msg = "Your rating: {:.0f} Hand rating {:.0f}\n".format(
            player_elo, hand_elo)
    header_widget.markdown(msg)
    return None

def load_hands():
    """Load hands list of json objects.

    The hands are loaded from the PyMongo database bridge_problem_database,
    collection "hands"

    Output: hands, json[]. Example:

       "n_hand" : ["SQ", "S6", "S2", "HA", "HK", "H6", "H2", "DA", "DQ", "D5", "CK", "C3", "C2"],
       "s_hand" : ["SA", "SK", "SJ", "ST", "S5", "HQ", "H7", "H3", "D7", "D4", "C8", "C7", "C5"],
       "w_hand" : ["S9", "S8", "S3", "HT", "H5", "DJ", "D9", "D8", "D6", "D3", "CJ", "C9", "C6"],
       "e_hand" : ["S7", "S4", "HJ", "H9", "H8", "H4", "DK", "DT", "D2", "CA", "CQ", "CT", "C4"],
       "context" : "Contract: 4 spades. You draw trumps in three rounds and play three top hearts ending in dummy, East having 4H. Which suit do you play next?",
       "correct_answer" : "H",
       "_id" : hexadecimal id object,
       "elo" : 1200,
       "hidden_hands" : "NS"

    Todo, as a future direction this function may be eliminated. It should be possible to randomly
    query the hands directly as a MongoDB cursor object. No python lists needed.
    """

    # Connect to PyMongo database which stores the hands.
    client = pymongo.MongoClient()
    db = client["bridge_problem_database"]
    hands_collection = db["hands"]
    
    # Get all hands from the database, as a list of JSON objects.
    all_hands = hands_collection.find({})
    hands_json = list(all_hands)
    
    return hands_json


def show_hand(hand_json, hands_widget):
    """ """

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
    rendered_hands = render_four_hands_with_context(
            list_of_hands=list_of_hands, 
            context=context,
            hidden_hands=hidden_hands 
            )

    hands_widget.markdown(rendered_hands, unsafe_allow_html=True)
    print(rendered_hands)
    return None

##########################################################
####### The code below executes in sequence and ##########
####### drives the main Streamlit app  ###################
##########################################################

player_elo = 1200 # TODO a future direction is to make this dynamic.

# Load hands and randomize their order.
hands = load_hands()
hand_indices = np.arange(len(hands), dtype=np.int8)
np.random.shuffle(hands)

# Connect to the hands collection in the database.
# This connection is created here to allow faster
# writing of updated ELOs after each hand is played.
client = pymongo.MongoClient()
db = client["bridge_problem_database"]
hands_collection = db["hands"]
    
# Initialize empty streamlit widgets to write various 
# page components to. By using widgets, we allow new
# text, when written, to overwrite the old text.
header_widget = streamlit.empty()
hands_widget = streamlit.empty()
response_widget = streamlit.empty()

# Show the first hand and ask for an answer.
hand_json = hands.pop()

show_hand_header(player_elo=player_elo,
        header_widget=header_widget,
        hand_json=hand_json)
show_hand(hand_json, hands_widget)

user_answer = response_widget.text_input("Your answer:")

# If the user inputs and answer:
# (1) Validate answer and update ELO
# (2) Show another hand.

if user_answer not in [None, ""]:

    # Calculate new player and hand ELO scores.
    correct_answer = hand_json["correct_answer"]
    user_was_correct = (user_answer.lower() == correct_answer.lower())
    hand_elo = hand_json["elo"]
    new_player_elo, new_hand_elo = elo.get_new_elos(
            player_elo, 
            hand_elo, 
            user_was_correct)
    
    # Update hand ELO in the database.
    hand_id = hand_json["_id"]
    query = {"_id" : hand_id} # update rows matching this query.
    update = {"$set" : {"elo" : new_hand_elo}} # update to perform.
    hands_collection.update_one(query, update)

    # Update player ELO - for now, only in the current session.
    player_elo = new_player_elo

    # Show the next hand.
    hand_json = hands.pop()
    user_answer = response_widget.text_input("Your answer: ")

    show_hand_header(player_elo=player_elo,
        header_widget=header_widget,
        hand_json=hand_json)
    show_hand(hand_json, hands_widget)
       
if len(hands) == 0:
    hands_widget.markdown("You have played all hands in the database!")
