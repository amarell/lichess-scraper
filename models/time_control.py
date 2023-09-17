class TimeControl:
    def __init__(self, clock_data):
        self.initial = clock_data.get("initial", 0)
        self.increment = clock_data.get("increment", 0)
        self.total_time = clock_data.get("totalTime", 0)
