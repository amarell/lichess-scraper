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

            print("Games added :", len(games), "/", n)

            if new_game.white.rating > max_elo_threshold:
                climb = False
            elif new_game.white.rating < min_elo_threshold:
                climb = True

            i += 1

        i = 0

        best_win_against, worst_defeat_against = scraper.get_user_extremes(
            user, list(games)[0].time_control.name
        )

        print(
            "Best win against: ",
            best_win_against,
            " Worst Defaeat against",
            worst_defeat_against,
            " climb:",
            climb,
        )

        # prev_user = user
        user = best_win_against if climb else worst_defeat_against

        # Fallback 1: switch logic to try the other extreme if the first one fails
        # This has a potential to lead to an infinite loop in which case we have to somehow break it
        # if user is None:
        #     user = worst_defeat_against if climb else best_win_against

        # Fallback 2 -
        # If some user's games are already added, just find some random user from tv and use him as next
        if user is None or games_contains_user(list(games), user):
            tv_games = [Game(g) for g in api.get_games_from_tv()]
            usernames = get_all_users_from_tv(tv_games)
            user = first_not_in_games(usernames, games)

            print("Chose a random player from Lichess TV: " + user + "\n")

        # Fallback 3: choose the prev user's last opponent in case all best wins/defeats are banned or closed
        # Should not happen very frequently in practice
        # if user is None:
        #     print(
        #         "Falling back to prev user's last opponent because his worst/best game opponents are closed / banned"
        #     )

        #     last_game = list(sorted(games, key=lambda game: game.index))[-1]
        #     user = (
        #         last_game.black.username
        #         if is_user_white(prev_user, last_game)
        #         else last_game.white.username
        #     )

    return list(games)


def first_not_in_games(usernames, games):
    for user in usernames:
        if not games_contains_user(games, user):
            return user

    print("All users on TV are already added in games :(")
    return usernames[0]


def games_contains_user(games, user):
    contains = False
    for game in games:
        if game.black.username == user or game.white.username == user:
            contains = True

    return contains


def get_all_users_from_tv(tv_games):
    black = [g.black.username for g in tv_games]
    white = [g.white.username for g in tv_games]
    return black + white


def get_n_games_new(
    n,
    start_user,
    max_games_per_user=10,
    history_offset=5,
    max_elo_threshold=1800,
    min_elo_threshold=800,
):
    api = APIClient()
    # scraper = Scraper()

    climb = True
    games = []
    user = start_user

    if user is None or len(user) == 0:
        raise ValueError("Please provide id of the first user.")

    while len(games) < n:
        user_games = api.get_games_from_user(
            user, max_amount=max_games_per_user + history_offset
        )
        print("Total games collected :", len(games), "/", n)
        new_user_games = []
        i = 0
        for g in user_games[: len(user_games) - history_offset]:
            new_game = Game(g)
            new_game = fill_history(new_game, history_offset, user, user_games, i)

            new_user_games.append(new_game)

            print("Games added :", len(new_user_games), "/", n)

            if new_game.white.rating > max_elo_threshold:
                climb = False
            elif new_game.white.rating < min_elo_threshold:
                climb = True

            i += 1

        i = 0

        max_elo_opponent, min_elo_opponent = find_max_elo_opponent(
            new_user_games, user
        ), find_min_elo_opponent(new_user_games, user)

        print(max_elo_opponent, min_elo_opponent)

        prev_user = user
        user = max_elo_opponent if climb else min_elo_opponent

        # Fallback: choose the prev user's last opponent in case all best wins are banned or closed
        # Should not happen very frequently in practice
        if user is None:
            print(
                "Falling back to prev user's last opponent because his worst/best game opponents are closed / banned"
            )
            user = (
                new_user_games[-1].black.username
                if is_user_white(prev_user, new_user_games[-1])
                else new_user_games[-1].white.username
            )

        games += new_user_games
    return games


def find_max_elo_opponent(games, user):
    maxIdx = 0
    for idx, game in enumerate(games):
        if get_opponent_rating(user, game) > get_opponent_rating(user, games[maxIdx]):
            maxIdx = idx
    return get_opponent_username(user, games[maxIdx])


def find_min_elo_opponent(games, user):
    minIdx = 0
    for idx, game in enumerate(games):
        if get_opponent_rating(user, game) < get_opponent_rating(user, games[minIdx]):
            minIdx = idx
    return get_opponent_username(user, games[minIdx])


def get_opponent_username(user, game):
    if is_user_white(user, game):
        return game.black.username
    return game.white.username


def get_opponent_rating(user, game):
    if is_user_white(user, game):
        return game.black.rating
    return game.white.rating


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
            print("Found a banned user!", game.black.username)
            game.black_history = [GameOutcome.WIN] * history_offset
            game.black_closed = True
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
            print("Found a banned user", game.white.username)
            game.white_history = [GameOutcome.WIN] * history_offset
            game.white_closed = True
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
