from util import *
from api import *


def run():
    api = APIClient()
    pretty_print_json(api.get_user_public_data("amarell"))
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
