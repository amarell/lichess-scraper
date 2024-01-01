from bs4 import BeautifulSoup
import urllib
from util import *
import unicodedata


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
        try:
            html = urllib.request.urlopen(
                f"{self.base_url}@/{user}/perf/{time_control}"
            ).read()
            soup = BeautifulSoup(html, "html.parser")
            result_split = soup.find("section", class_="result split")
            tables = result_split.find_all("table")

            worst_losses_against = [
                unicodedata.normalize("NFKD", link.text).split(" ")[1]
                if is_titled_player(unicodedata.normalize("NFKD", link.text))
                else link.text
                for link in tables[1].find_all("a", class_="user-link")
            ]
            best_victories_against = [
                unicodedata.normalize("NFKD", link.text).split(" ")[1]
                if is_titled_player(unicodedata.normalize("NFKD", link.text))
                else link.text
                for link in tables[0].find_all("a", class_="user-link")
            ]

            print(best_victories_against, worst_losses_against)

            active_account_win = None
            active_account_loss = None

            for user in best_victories_against:
                if not self.is_account_banned(user) and not self.is_account_closed(
                    user
                ):
                    active_account_win = user
                    break

            for user in worst_losses_against:
                if not self.is_account_banned(user) and not self.is_account_closed(
                    user
                ):
                    active_account_loss = user
                    break

            return active_account_win, active_account_loss
        except:
            print(f"{self.base_url}@/{user}/perf/{time_control} cannot be found!")
            return "", ""

    def is_account_banned(self, user):
        try:
            html = urllib.request.urlopen(f"{self.base_url}@/{user}").read()
            soup = BeautifulSoup(html, "html.parser")
            account_banned = soup.find("div", class_="warning tos_warning")
            return account_banned is not None
        except:
            print(f"User {user} doesn't exist.")
            return False

    def is_account_closed(self, user):
        try:
            html = urllib.request.urlopen(f"{self.base_url}@/{user}").read()
            return False
        except:
            return True
