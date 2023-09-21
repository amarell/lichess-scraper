from util import *
from models.game import Game
from api import *


"""
Gets `max_games_per_user` games for a given `start_user` if they have that many games played.
Then takes their opponent in the last game and does the same for that user.
This keeps happening until `n` games are in the list.
"""


def get_n_games(n, start_user, max_games_per_user=10):
    api = APIClient()

    # initial state
    games = []
    game_ids = []
    user = start_user

    if user is None or len(user) == 0:
        raise ValueError("Please provide id of the first user.")

    while len(games) < n:
        user_games = api.get_games_from_user(user, max_amount=max_games_per_user)
        for g in user_games:
            if g["id"] not in game_ids:
                game_ids.append(g["id"])
                games.append(Game(g))

        last_game = games[-1]

        if is_user_white(user, last_game):
            user = last_game.black.username
        else:
            user = last_game.white.username

    return games
