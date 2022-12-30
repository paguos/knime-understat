import aiohttp
import asyncio
import pandas as pd

from understat import Understat

from config import LeagueOperation
from config import TeamOperation, TeamStat
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
