import aiohttp
import asyncio
import pandas as pd

from understat import Understat

from config import LeagueOperation
from config import PlayerOperation
from config import TeamOperation, TeamStat
from utils import parse_player_stats
from utils import parse_team_stats


class BaseTask:

    async def fetch_data(self):
        async with aiohttp.ClientSession() as session:
            understat = Understat(session)
            self.data = await self.task(understat)

    def execute(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.fetch_data())

        return self.data


class LeagueTask(BaseTask):

    def __init__(self, operation: LeagueOperation, league, season) -> None:
        self.operation = operation
        self.league = league
        self.season = season

    async def task(self, understat: Understat):
        if (self.operation == LeagueOperation.PLAYERS):
            data = await understat.get_league_players(self.league, self.season)
        elif (self.operation == LeagueOperation.TABLE):
            data = await understat.get_league_table(self.league, self.season)

        headers = data.pop(0)  # get headers
        return pd.DataFrame.from_records(data, columns=headers)


class TeamTask(BaseTask):

    def __init__(self, operation: TeamOperation, team_name, season, stat=TeamStat.SITUATION):
        self.operation = operation
        self.team_name = team_name
        self.season = season
        self.stat = stat

    async def task(self, understat: Understat):
        if (self.operation == TeamOperation.PLAYERS):
            data = await understat.get_team_players(self.team_name, self.season)
            headers = data.pop(0)  # get headers
            return pd.DataFrame.from_records(data, columns=headers)
        elif (self.operation == TeamOperation.STATS):
            data = await understat.get_team_stats(self.team_name, self.season)
            single_stat_data = parse_team_stats(data, self.stat)
            headers = self.stat.headers()
            return pd.DataFrame.from_records(single_stat_data, columns=headers)


class PlayerTask(BaseTask):

    def __init__(self, operation: PlayerOperation, player_id: int, grouped: bool = False):
        self.operation = operation
        self.player_id = player_id
        self.grouped = grouped

    async def task(self, understat: Understat):
        if (self.operation == PlayerOperation.SHOTS):
            data = await understat.get_player_shots(self.player_id)
            return pd.DataFrame.from_records(data)
        elif (self.operation == PlayerOperation.STATS):
            data = await understat.get_player_stats(self.player_id)
            single_stat_data = parse_player_stats(data)
            return pd.DataFrame.from_records(
                single_stat_data,
                columns=["position", "metric", "avg", "max", "min"]
            )
