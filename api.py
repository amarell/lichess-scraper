import os
import dotenv
import requests
import ndjson
import json

dotenv.load_dotenv()

game_headers = {
    "Authorization": "Bearer " + os.getenv("API_TOKEN"),
    "Content-Type": "text/plain",
    "Accept": "application/x-ndjson",
}

headers = {
    "Authorization": "Bearer " + os.getenv("API_TOKEN"),
    "Content-Type": "text/plain",
    "Accept": "application/json",
}


class APIClient:
    def __init__(self):
        self.api_token = os.getenv("API_TOKEN")
        self.base_url = "https://lichess.org/api"

    def get_games_by_id(self, ids):
        payload = ",".join(ids)

        payload = payload[:-1]

        r = requests.post(
            f"{self.base_url}/games/export/_ids?pgnInJson=true&clocks=true&accuracy=true&opening=true",
            headers=game_headers,
            data=payload,
        )

        return r.json(cls=ndjson.Decoder)

    def get_games_from_user(self, username, max_amount=10):
        print("running get games from user...")
        r = requests.get(
            f"{self.base_url}/games/user/{username}?pgnInJson=true&clocks=true&accuracy=true&opening=true&max={max_amount}",
            headers=game_headers,
        )

        return r.json(cls=ndjson.Decoder)

    def get_user_public_data(self, username):
        r = requests.get(
            f"{self.base_url}/user/{username}",
            headers=headers,
        )

        return r.json()

    def stream_game(self, id):
        r = requests.get(
            f"{self.base_url}/stream/game/{id}", headers=game_headers, stream=True
        )

        for line in r.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                print(json.loads(decoded_line))
