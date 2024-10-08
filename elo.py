# elo.py

import math

def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

def mov_multiplier(mov, rating_diff):
    return (mov + 1) ** 1.5

def update_player_ratings(game):
    K = 80  # Medium K-factor

    # Calculate average team ratings
    team1_rating = sum(player.rating for player in game.team1_players) / len(game.team1_players)
    team2_rating = sum(player.rating for player in game.team2_players) / len(game.team2_players)

    # Expected scores
    expected_team1 = expected_score(team1_rating, team2_rating)
    expected_team2 = 1 - expected_team1

    # Actual scores
    if game.team1_score > game.team2_score:
        actual_team1 = 1
        actual_team2 = 0
    elif game.team1_score < game.team2_score:
        actual_team1 = 0
        actual_team2 = 1
    else:
        actual_team1 = 0.5
        actual_team2 = 0.5

    # Margin of Victory
    mov = abs(game.team1_score - game.team2_score)
    rating_diff = abs(team1_rating - team2_rating)
    multiplier = mov_multiplier(mov, rating_diff)

    # Rating adjustments
    delta_team1 = K * multiplier * (actual_team1 - expected_team1)
    delta_team2 = -delta_team1  # Since delta_team1 + delta_team2 = 0

    # Update player ratings
    for player in game.team1_players:
        player.rating += delta_team1 / len(game.team1_players)
    for player in game.team2_players:
        player.rating += delta_team2 / len(game.team2_players)
