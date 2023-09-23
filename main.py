from util import *
from game_util import *
from api import *
from models.game import Game
from scraper import *


def run():
    scraper = Scraper()

    best_win, worst_loss = scraper.get_user_extremes("forgotten_character", "rapid")

    print(f"{best_win} - {worst_loss}")

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
