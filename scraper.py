from bs4 import BeautifulSoup
from util import *
import urllib


class Scraper:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Scraper, cls).__new__(cls)
            cls._instance.base_url = "https://lichess.org/"

        return cls._instance

    """
    Returns user ids of `user` worst defeat and best victory
    """

    def get_user_extremes(self, user, time_control):
        html = urllib.request.urlopen(
            f"https://lichess.org/@/{user}/perf/{time_control}"
        ).read()
        soup = BeautifulSoup(html, "html.parser")
        result_split = soup.find("section", class_="result split")
        tables = result_split.find_all("table")

        worst_loss = tables[1].find("a", class_="user-link")
        best_victory = tables[0].find("a", class_="user-link")
        return best_victory.text, worst_loss.text
