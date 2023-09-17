class Opening:
    def __init__(self, opening_data):
        self.eco = opening_data.get("eco", "")
        self.name = opening_data.get("name", "")
        self.ply = opening_data.get("ply", 0)
