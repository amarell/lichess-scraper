import json
import csv


def dump_games_to_csv(games):
    data = [g.toList() for g in games]

    headers = [
        "id",
        "Rated",
        "Variant",
        "Time Control",
        "Performance",
        "Status",
        "Winner",
        "White Username",
        "Black Username",
        "White Rating",
        "Black Rating",
        "Opening Name",
        "Opening Eco",
        "Opening PLY",
        "Moves",
        "Black History",
        "White History",
    ]

    with open("output.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)

    file.close()


def pretty_print_json(json_content):
    print(json.dumps(json_content, indent=4, sort_keys=True))


# TODO
def get_current_session_streak():
    return


def is_titled_player(user):
    return user.split(" ")[0] in [
        "GM",
        "IM",
        "FM",
        "CM",
        "WGM",
        "WIM",
        "WFM",
        "WCM",
    ]


def is_user_white(user, game):
    return game.white.username == user


# TODO
def is_user_banned(user):
    return False
