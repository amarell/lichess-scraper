from util import *
from models.game import Game, GameOutcome
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

        for g in user_games[: len(user_games) - history_offset]:
            new_game = Game(g)
            new_game = fill_history(new_game, history_offset, user, user_games, i)
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

        prev_user = user
        user = best_win_against if climb else worst_defeat_against

        if user is None:
            last_game = list(sorted(games, key=lambda game: game.index))[-1]
            user = (
                last_game.black.username
                if is_user_white(prev_user, last_game)
                else last_game.white.username
            )

    return games


def fill_history(game, history_offset, user, user_games, current_index):
    scraper = Scraper()
    api = APIClient()

    if is_user_white(user, game):
        game.white_history = [
            Game(g).get_users_game_outcome(user)
            for g in user_games[current_index + 1 : current_index + history_offset + 1]
        ]
    else:
        game.black_history = [
            Game(g).get_users_game_outcome(user)
            for g in user_games[current_index + 1 : current_index + history_offset + 1]
        ]

    if is_user_white(user, game):
        if scraper.is_account_closed(game.black.username) or scraper.is_account_banned(
            game.black.username
        ):
            # The idea is that if one user got banned, they were cheating and likely won all their past games
            # I should probably think of something else to handle this scenario
            game.black_history = [GameOutcome.WIN] * history_offset
        else:
            game.black_history = [
                Game(g).get_users_game_outcome(game.black.username)
                for g in api.get_games_from_user_until(
                    game.black.username,
                    game.last_move_at,
                    history_offset + 1,
                )[1:]
            ]
    else:
        if scraper.is_account_closed(game.white.username) or scraper.is_account_banned(
            game.white.username
        ):
            # The idea is that if one user got banned, they were cheating and likely won all their past games
            # I should probably think of something else to handle this scenario
            game.white_history = [GameOutcome.WIN] * history_offset
        else:
            game.white_history = [
                Game(g).get_users_game_outcome(game.white.username)
                for g in api.get_games_from_user_until(
                    game.white.username,
                    game.last_move_at,
                    history_offset + 1,
                )[1:]
            ]

    return game
