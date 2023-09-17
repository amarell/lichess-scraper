class Player:
    def __init__(self, player_data):
        self.username = player_data.get("user", {}).get("name", "")
        self.rating = player_data.get("rating", 0)
        self.rating_diff = player_data.get("ratingDiff", 0)
