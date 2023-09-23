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
    games = set()
    user = start_user

    if user is None or len(user) == 0:
        raise ValueError("Please provide id of the first user.")

    while len(games) < n:
        user_games = api.get_games_from_user(user, max_amount=max_games_per_user)

        i = 0

        for g in user_games:
            i += 1
            if g["variant"] == "standard":
                new_game = Game(g)
                if i > len(user_games) - 5:
                    if is_user_white(user, new_game):
                        new_game.white_history = [
                            Game(g).get_users_game_outcome(user)
                            for g in user_games[i - 5 : i]
                        ]
                    else:
                        new_game.black_history = [
                            Game(g).get_users_game_outcome(user)
                            for g in user_games[i - 5 : i]
                        ]

                games.add(new_game)

        i = 0

        last_game = Game(user_games[-1])

        if is_user_white(user, last_game):
            user = last_game.black.username
        else:
            user = last_game.white.username

    return games
