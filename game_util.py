from util import *
from models.game import Game
from api import *
from scraper import *


"""
Gets `max_games_per_user` games for a given `start_user` if they have that many games played.
Then takes their opponent in the last game and does the same for that user.
This keeps happening until `n` games are in the list.

Params: 
n - number of games to return
max_games_per_user - maximum number of games before switching to another user
history_offset - how many games to keep in history
"""


def get_n_games(
    n,
    start_user,
    max_games_per_user=10,
    history_offset=5,
    max_elo_threshold=1800,
    min_elo_threshold=800,
):
    api = APIClient()
    scraper = Scraper()

    games = set()
    user = start_user

    if user is None or len(user) == 0:
        raise ValueError("Please provide id of the first user.")

    climb = True
    game_index = 0

    while len(games) < n:
        user_games = api.get_games_from_user(
            user, max_amount=max_games_per_user + history_offset
        )

        i = 0

        for g in user_games:
            if "variant" in g.keys() and g["variant"] == "standard":
                new_game = Game(g)
                if i < len(user_games) - history_offset:
                    if is_user_white(user, new_game):
                        new_game.white_history = [
                            Game(g).get_users_game_outcome(user)
                            for g in user_games[i + 1 : i + history_offset + 1]
                        ]
                    else:
                        new_game.black_history = [
                            Game(g).get_users_game_outcome(user)
                            for g in user_games[i + 1 : i + history_offset + 1]
                        ]
                        new_game.index = game_index
                        game_index += 1
                        games.add(new_game)

                        if new_game.white.rating > max_elo_threshold:
                            climb = False
                        elif new_game.white.rating < min_elo_threshold:
                            climb = True

                i += 1

        i = 0

        best_win_against, worst_defeat_against = scraper.get_user_extremes(
            user, list(games)[0].time_control.name.lower()
        )

        user = best_win_against if climb else worst_defeat_against
    return games
