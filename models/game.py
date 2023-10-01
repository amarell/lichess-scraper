from models.player import Player
from models.opening import Opening
from models.time_control import TimeControl
from enum import Enum
from util import *


class GameOutcome(Enum):
    DEFEAT = -1
    DRAW = 0
    WIN = 1


class Game:
    def __init__(self, game_data):
        self.id = game_data.get("id", "")
        self.rated = game_data.get("rated", False)
        self.variant = game_data.get("variant", "")
        self.speed = game_data.get("speed", "")
        self.perf = game_data.get("perf", "")
        self.created_at = game_data.get("createdAt", 0)
        self.last_move_at = game_data.get("lastMoveAt", 0)
        self.status = game_data.get("status", "")
        self.winner = game_data.get("winner", "")

        white_data = game_data.get("players", {}).get("white", {})
        black_data = game_data.get("players", {}).get("black", {})
        self.players = {
            "white": Player(white_data),
            "black": Player(black_data),
        }

        self.white = self.players["white"]
        self.black = self.players["black"]

        self.opening = Opening(game_data.get("opening", {}))

        self.black_history = []
        self.white_history = []

        self.moves = game_data.get("moves", "")
        self.clocks = game_data.get("clocks", [])
        self.pgn = game_data.get("pgn", "")

        time_control_data = game_data.get("clock", {})
        self.time_control = TimeControl(time_control_data)

    def __str__(self):
        return (
            f"Game ID: {self.id}\nRated: {self.rated}\nVariant: {self.variant}\nSpeed: {self.speed}\n"
            f"Performance: {self.perf}\nCreated At: {self.created_at}\nLast Move At: {self.last_move_at}\n"
            f"Status: {self.status}\nWinner: {self.winner}\n"
            f"White Player: {self.white.username} (Rating: {self.white.rating})\n"
            f"Black Player: {self.black.username} (Rating: {self.black.rating})\n"
            f"Opening: {self.opening.name} (ECO: {self.opening.eco}, Ply: {self.opening.ply})\n"
            f"Moves: {self.moves}\n"
            f"TimeControl: Initial: {self.time_control.initial}, Increment: {self.time_control.increment}, Total Time: {self.time_control.total_time} seconds\n"
        )

    def get_users_game_outcome(self, user):
        if is_user_white(user, self):
            if self.winner == "white":
                return GameOutcome.WIN
            elif self.winner == "":
                return GameOutcome.DRAW
            else:
                return GameOutcome.DEFEAT

        else:
            if self.winner == "white":
                return GameOutcome.DEFEAT
            elif self.winner == "":
                return GameOutcome.DRAW
            else:
                return GameOutcome.WIN

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Game) and self.id == other.id

    def toList(self):
        return [
            self.id,
            self.rated,
            self.variant,
            self.time_control.get_time_control_name(),
            self.perf,
            self.status,
            self.winner,
            self.white.username,
            self.black.username,
            self.white.rating,
            self.black.rating,
            self.opening.name,
            self.opening.eco,
            self.opening.ply,
            self.moves,
            [outcome.value for outcome in self.black_history],
            [outcome.value for outcome in self.white_history],
        ]
