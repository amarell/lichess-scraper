from util import *
from game_util import *
from api import *
from models.game import Game
from scraper import *


def run():
    games = get_n_games(10, "soinne", 10)

    for g in games:
        print("White: " + g.black.username + "vs. " + "White: " + g.white.username)
        print(g.white_history)
        print(g.black_history)
    # dump_games_to_csv(games)


if __name__ == "__main__":
    run()
