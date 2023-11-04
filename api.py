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
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(APIClient, cls).__new__(cls)
            cls._instance.api_token = os.getenv("API_TOKEN")
            cls._instance.base_url = "https://lichess.org/api"
        return cls._instance

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
        r = requests.get(
            f"{self.base_url}/games/user/{username}?pgnInJson=true&clocks=true&accuracy=true&opening=true&max={max_amount}&perfType=ultraBullet,bullet,blitz,rapid,classical",
            headers=game_headers,
        )

        return r.json(cls=ndjson.Decoder)

    def get_games_from_user_until(
        self,
        username,
        until,
        max_amount=10,
    ):
        r = requests.get(
            f"{self.base_url}/games/user/{username}?pgnInJson=true&clocks=true&accuracy=true&opening=true&max={max_amount}&until={until}&perfType=ultraBullet,bullet,blitz,rapid,classical",
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
