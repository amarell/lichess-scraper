from util import *
from api import *
from models.game import Game
import asyncio


# initial global state
games = []
game_ids = []
user = "forgotten_character"


def run():
    api = APIClient()

    get_n_games(20, api)

    # api.stream_game("h9nyJUuo")
    # games = api.get_games_by_id(["TJxUmbWK", "4OtIh2oh"])
    # games = api.get_games_from_user("Vhtool")

    # for g in games:
    #     print(
    #         json.dumps(
    #             g,
    #             sort_keys=True,
    #             indent=4,
    #         )
    #     )


def get_n_games(n, api):
    while len(games) < n:
        global user
        user_games = api.get_games_from_user(user)
        for g in user_games:
            if g["id"] not in game_ids:
                game_ids.append(g["id"])
                games.append(Game(g))

        last_game = games[-1]

        if is_user_white(user, last_game):
            user = last_game.black.username
        else:
            user = last_game.white.username


if __name__ == "__main__":
    run()
