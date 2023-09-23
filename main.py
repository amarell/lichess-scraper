from util import *
from game_util import *
from api import *
from models.game import Game
from scraper import *


def run():
    # scraper = Scraper()

    games = get_n_games(20, "szymonoberc", 10)

    games_with_history = {
        g for g in games if len(g.black_history) > 0 or len(g.white_history) > 0
    }

    for g in games_with_history:
        print(f"White history: {g.white_history}")
        print(f"Black history: {g.black_history}")

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
