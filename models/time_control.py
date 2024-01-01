class TimeControl:
    def __init__(self, clock_data):
        self.initial = clock_data.get("initial", 0)
        self.increment = clock_data.get("increment", 0)
        self.total_time = clock_data.get("totalTime", 0)
        self.est_game_duration = self.get_estimated_game_duration()
        self.name = self.get_time_control_name()

    # https://lichess.org/faq#time-controls
    def get_estimated_game_duration(self):
        return self.initial + 40 * self.increment

    def get_time_control_name(self):
        if self.est_game_duration < 29:
            return "ultraBullet"
        elif self.est_game_duration < 179:
            return "bullet"
        elif self.est_game_duration < 479:
            return "blitz"
        elif self.est_game_duration < 1499:
            return "rapid"
        else:
            return "classical"
