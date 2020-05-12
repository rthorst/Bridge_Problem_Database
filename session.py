import os
import json 
import numpy as np
from render_hand import render_four_hands_with_context
import sqlite3
import elo
import pymongo
import streamlit
import datetime


def provide_feedback(user_was_correct, feedback_widget):
    """Provide feedback on whether the user was correct.

    Parameters:
    -------------
    user_was_correct (boolean)
    feedback_widget (streamlit widget object

    Returns:
    --------------
    None

    Write feedback, as HTML + markdown, to feedback_widget.
    By using a widget object, subsequent messages will overwrite
    the existing feedback.
    """

    if user_was_correct:
        feedback_msg = "<font color='green'>Correct!</font>"

    else:
        feedback_msg = "<font color='red'>Incorrect. Correct answer is {}</font>".format(correct_answer)
    
    feedback_widget.markdown(feedback_msg, unsafe_allow_html = True)

def test_if_correct_answer(user_answer, correct_answer):
    """Return True if user gave the correect answer

    Parameters:
    -----------
    user_answer (string)
    correct_answer (string)

    Returns:
    correct (Boolean)

    Currently, we validate by checking for an exact but case-insensitive
    string match. As a future direction we should consider cases where
    more flexibility may be desired, for example allowing "F" (false) to 
    count when "N" (no) is the correct answer.
    """

    return user_answer.lower() == correct_answer.lower()

def show_hand_header(player_elo, hand_json, header_widget):
    """
    Display a brief header for each hand, retuning None.

    Parameters:
    --------------
    player_elo (float) e.g. 1200
    hand_json (json) json object containing the hand.
    header_widget (streamlit widget)

    Returns:
    -------------
    None

    Write a simple header in markdown to header_widget. By writing
    to a streamlit widget, subsequent calls to this function will
    over-write the old header.
    """

    hand_elo = hand_json["elo"]
    msg = "### You are rated: {:.0f} This hand is rated: {:.0f}\n".format(
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

    Returns:
    ---------------
    None

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


def lookup_user_elo(username, user_collection):
    """Lookup a user's ELO rating.

    Parameters:
    -----------
    username (string)
    user_collection (pymongo collection object)

    Returns:
    ----------
    player_elo (numeric) e.g. 1200
    """

    params = {"username" : username}
    query_result = user_collection.find_one(params)
    
    if query_result:
        player_elo = query_result["elo"]
    else:
        player_elo = 1200

    return player_elo

def log_showing_hand(hand_json, username, events_collection):
    """Log that a hand was shown to the user in the events collection.

    Parameters:
    -----------
    hand_json (json)
    username (string)
    events_collection (pymongo collection object)

    Returns:
    ------------
    None

    Writes to the events collection a row with
    username, hand_id, correct_answer, timestamp.
    """

    event_record = {
        "username" : username,
        "hand_id" : hand_json["_id"],
        "correct_answer" : hand_json["correct_answer"],
        "timestamp" : datetime.datetime.now().timestamp()
    }
    events_collection.insert_one(event_record)

    return None

def lookup_correct_answer(events_collection):
    """Lookup the correct answer, from 2nd-most-recent row in events collection

    Paramters:
    ----------
    events_collection (pymongo collection)

    Returns:
    ----------
    correct_answer (string)
    """

    events_sorted_by_timestamp = events_collection.find().sort(
            "timestamp", pymongo.DESCENDING)
    second_most_recent_event = events_sorted_by_timestamp[1]

    return second_most_recent_event["correct_answer"]

#################################################################
################## Start Streamlit App #########################
#################################################################

# Streamlit renders the following code in declarative style from
# top to bottom. 

# Allow the user to log in on the sidebar.
username = streamlit.sidebar.text_input("Username:", value="guest")

# Load all hands from the database, and randomize their order
# of presentation.
hands = load_hands()
hand_indices = np.arange(len(hands), dtype=np.int8)
np.random.shuffle(hands)

# Connect to the "hands", "user", and "events" collections in 
# the database.
client = pymongo.MongoClient()
db = client["bridge_problem_database"]
hands_collection = db["hands"]
user_collection = db["user"]
events_collection = db["events"] # hands shown to users.

# Look up user ELO from the database. 
player_elo = lookup_user_elo(username, user_collection)

# Initialize empty streamlit "widgets" to write page components
# to. By using widgets, we are able to over-write the content
# (e.g. with a new hand) more easily.
header_widget = streamlit.empty()
feedback_widget = streamlit.empty() # correct/incorrect.
hands_widget = streamlit.empty()
response_widget = streamlit.empty()

# Show the user a hand and log to the database that the hand was shown.
hand_json = hands.pop()
show_hand_header(player_elo=player_elo,
    header_widget=header_widget,
    hand_json=hand_json)
render_hands_in_streamlit(hand_json, hands_widget)
log_showing_hand(hand_json=hand_json, 
        username=username, events_collection=events_collection)

# For debugging purposes, log the hand to the shell.
# This is helpful to identify incorrectly added hands.
print(hand_json)

# Ask for an answer.
# Note that when the user interacts enters an answer, 
# the entire script will re-run.
user_answer = response_widget.text_input("Your answer:")

if user_answer not in [None, ""]:

    # Lookup the correct answer, which is the second-to-most-
    # recent row in the events table. It is the second to most
    # recent row because the code above already showed one more hand.
    correct_answer = lookup_correct_answer(events_collection)

    # Calculate new player and hand ELO scores.
    user_was_correct = test_if_correct_answer(user_answer, correct_answer)
    hand_elo = hand_json["elo"]
    new_player_elo, new_hand_elo = elo.get_new_elos(
            player_elo, 
            hand_elo, 
            user_was_correct)

    # Provide feedback to the user (correct/incorrect)
    provide_feedback(user_was_correct, feedback_widget)

    # Update player and hand ELO in the database.
    # For now, the player ELO is only stored in the 
    # current session, but a future direction is to 
    # store player ELO across sessions.
    hand_id = hand_json["_id"]
    query = {"_id" : hand_id} # update rows matching this query.
    update = {"$set" : {"elo" : new_hand_elo}} # update to perform.
    hands_collection.update_one(query, update)

    player_elo = new_player_elo
    if username != "guest":
        query = {"username" : username}
        update = {"$set" : {"elo" : new_player_elo}}
        user_collection.update_one(query, update)
    
