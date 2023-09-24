import json


# TODO
def dump_json_into_csv(json):
    return


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
