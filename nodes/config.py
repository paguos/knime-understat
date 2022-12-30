from enum import Enum


class Competition(Enum):
    EPL = "EPL"
    LA_LIGA = "La Liga"
    BUNDESLIGA = "Bundesliga"
    SERIE_A = "Serie A"
    LEAGUE_1 = "Ligue 1"
    RPFL = "RFPL"


class LeagueOperation(Enum):
    PLAYERS = "Players"
    TABLE = "Table"


class TeamOperation(Enum):
    PLAYERS = "Players"
    STATS = "Stats"


class TeamStat(Enum):
    ATTACK_SPEED = "attackSpeed"
    FORMATION = "formation"
    GAME_STATE = "gameState"
    RESULT = "result"
    SHOT_ZONE = "shotZone"
    SITUATION = "situation"
    TIMING = "timing"

    def headers(self):
        headers = [
            self.value,
            "shots",
            "goals",
            "xG",
            "shots (against)",
            "goals (against)",
            "xG (against)"
        ]

        if self == TeamStat.FORMATION:
            headers.insert(1, "time")
        return headers
