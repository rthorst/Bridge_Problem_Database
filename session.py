import os
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


def render_hands_in_streamlit(hand_json, hands_widget):
    """Helper function to render hand diagram in streamlit.
    
    Parameters:
    ----------------
    hand_json : json object containing 4 hands, context, etc.
    hands_widget: streamlit widget, to which the hands will be written.

    Renders the hands in HTML + markdown by calling 
    render_hands.render_four_hands_with_context()
    """

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
    
    return None

#################################################################
################## Start Streamlit App #########################
#################################################################

# Streamlit renders the following code in declarative style from
# top to bottom. 

player_elo = 1200 # TODO: a known future direction is to store
                  # player ELO across sessions.

# Load all hands from the database, and randomize their order
# of presentation.
hands = load_hands()
hand_indices = np.arange(len(hands), dtype=np.int8)
np.random.shuffle(hands)

# Connect to the "hands" collection in the database, which
# allows faster updates after each hand. 
client = pymongo.MongoClient()
db = client["bridge_problem_database"]
hands_collection = db["hands"]

# Initialize empty streamlit "widgets" to write page components
# to. By using widgets, we are able to over-write the content
# (e.g. with a new hand) more easily.
header_widget = streamlit.empty()
hands_widget = streamlit.empty()
response_widget = streamlit.empty()

# Show the user a hand
hand_json = hands.pop()
show_hand_header(player_elo=player_elo,
    header_widget=header_widget,
    hand_json=hand_json)
render_hands_in_streamlit(hand_json, hands_widget)

# Store the answer to the current hand in a temporary 
# file (answer.txt). This is a HACK and should be 
# refactored, but is necessary because any time the 
# user enters an answer, Streamlit re-executes the app
# from the top.
if not os.path.exists("answer.txt"):
    with open("answer.txt", "w") as of:
        of.write(hand_json["correct_answer"])

# Ask for an answer.
# Note that when the user interacts enters an answer, 
# the entire script will re-run.
user_answer = response_widget.text_input("Your answer:")

if user_answer not in [None, ""]:

    # Look up the correct answer, which will be 
    # in the stored "answer.txt" file since streamlit
    # has already reloaded the page in the background and
    # proceeded to the next problem.
    correct_answer = open("answer.txt", "r").read()

    # Calculate new player and hand ELO scores.
    user_was_correct = (user_answer.lower() == correct_answer.lower())
    hand_elo = hand_json["elo"]
    new_player_elo, new_hand_elo = elo.get_new_elos(
            player_elo, 
            hand_elo, 
            user_was_correct)

    # Update player and hand ELO in the database.
    # For now, the player ELO is only stored in the 
    # current session, but a future direction is to 
    # store player ELO across sessions.
    hand_id = hand_json["_id"]
    query = {"_id" : hand_id} # update rows matching this query.
    update = {"$set" : {"elo" : new_hand_elo}} # update to perform.
    hands_collection.update_one(query, update)

    player_elo = new_player_elo

    # Cache the correct answer to this current hand in answer.txt,
    # so that when the page is reloaded the answer is preserved.
    with open("answer.txt", "w") as of:
        of.write(hand_json["correct_answer"])
