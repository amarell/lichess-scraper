from util import *
from game_util import *
from api import *
from models.game import Game
from scraper import *


def run():
    games = get_n_games(10, "Roaccutane", 10)

    dump_games_to_csv(games)


if __name__ == "__main__":
    run()
