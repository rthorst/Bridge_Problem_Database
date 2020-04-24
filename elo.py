import math

def get_new_elos(player_elo, hand_elo, user_was_correct):
    """
    player_elo (integer) old player elo
    hand_elo (integer) old hand elo
    user_was_correct (boolean)

    return tuple of:
        new_player_elo (int)
        new_hand_elo (int)
    """

    # Calculate expected win probabilities.
    player_win_probability = 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (player_elo - hand_elo) / 400)) 
    hand_win_probability = (1 - player_win_probability)

    # Calculate difference in outcome from expectation.
    player_outcome_minus_expected = int(user_was_correct) - player_win_probability
    hand_outcome_minus_expected = (1 - int(user_was_correct)) - hand_win_probability

    # Calculate new elos.
    K = 30 # scaling factor.
    new_player_elo = player_elo + K*(player_outcome_minus_expected)
    new_hand_elo = hand_elo + K*(hand_outcome_minus_expected)

    return (new_player_elo, new_hand_elo)
