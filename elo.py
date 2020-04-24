import math

def get_new_elos(old_player_elo, old_hand_elo, user_was_correct, K=30):
    """
    Based on the result of a hand, return new player and hand ELO scores.

    parameters:
        player_elo (integer) old player elo
        hand_elo (integer) old hand elo
        user_was_correct (boolean)
        K: scaling factor (default 30). 
    return tuple of:
        new_player_elo (int)
        new_hand_elo (int)
    """

    # Calculate expected win probabilities for the player and hand.
    player_win_probability = 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (old_player_elo - old_hand_elo) / 400)) 
    hand_win_probability = (1 - player_win_probability)

    # Calculate (outcome - expected) for the player and hand.
    # This difference is the basis for the ELO update.
    player_outcome_minus_expected = int(user_was_correct) - player_win_probability
    hand_outcome_minus_expected = (1 - int(user_was_correct)) - hand_win_probability

    # Calculate new elos, based on K * (outcome - expected).
    # K is a scaling factor, default 30, but this can be adjusted for example upwards for newer players
    # or downwards for older players. 
    new_player_elo = player_elo + K*(player_outcome_minus_expected)
    new_hand_elo = hand_elo + K*(hand_outcome_minus_expected)

    return (new_player_elo, new_hand_elo)
