import aiohttp
import asyncio
import pandas as pd

from understat import Understat

from config import LeagueOperation


class LeagueTask:

    def __init__(self, operation, league, season) -> None:
        self.operation = operation
        self.league = league
        self.season = season

    async def fetch_data(self):
        async with aiohttp.ClientSession() as session:
            understat = Understat(session)

            if (self.operation == LeagueOperation.PLAYERS):
                table = await understat.get_league_players(self.league, self.season)
            elif (self.operation == LeagueOperation.TABLE):
                table = await understat.get_league_table(self.league, self.season)

            headers = table.pop(0)
            self.data = pd.DataFrame.from_records(table, columns=headers)

    def execute(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.fetch_data())

        return self.data
