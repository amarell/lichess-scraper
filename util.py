import json
import csv


def dump_games_to_csv(games):
    data = [g.toList() for g in games]

    headers = [
        "id",
        "Rated",
        "Variant",
        "Time_Control",
        "Performance",
        "Status",
        "Winner",
        "White_Username",
        "Black_Username",
        "White_Rating",
        "Black_Rating",
        "Opening_Name",
        "Opening_Eco",
        "Opening_PLY",
        "Moves",
        "Black_History",
        "White_History",
        "Black_Account_Closed",
        "White_Account_Closed",
    ]

    with open("2k.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)

    file.close()


def pretty_print_json(json_content):
    print(json.dumps(json_content, indent=4, sort_keys=True))


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
        "NM",
    ]


def is_user_white(user, game):
    return game.white.username == user
