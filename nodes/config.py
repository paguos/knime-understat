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
