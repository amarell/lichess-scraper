import requests


def run():
    r = requests.get(
        "https://random-data-api.com/api/users/random_user",
        headers={"Accept": "application/json"},
    )

    print(r.json())


if __name__ == "__main__":
    run()
