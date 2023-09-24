from util import *
from game_util import *
from api import *
from models.game import Game
from scraper import *


def run():
    # scraper = Scraper()

    games = get_n_games(30, "Roaccutane", 10)

    for g in sorted(games, key=lambda g: g.index):
        print(f"Player ids: {g.white.username} vs : {g.black.username}")
        print(f"White rating: {g.white.rating} vs : {g.black.rating}")

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


if __name__ == "__main__":
    run()
