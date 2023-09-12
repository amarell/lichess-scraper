import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

headers = {
    "Authorization": "Bearer " + os.getenv("API_TOKEN"),
}


def run():
    r = requests.get(
        "https://lichess.org/api/account",
        headers=headers,
    )

    print(json.dumps(r.json(), indent=4))


if __name__ == "__main__":
    run()
