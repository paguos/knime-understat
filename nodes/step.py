import aiohttp
import asyncio

import pandas as pd

from understat import Understat


class LeagueTableStep:

    def __init__(self, league, season) -> None:
        self.league = league
        self.season = season

    async def fetch_data(self):
        async with aiohttp.ClientSession() as session:
            understat = Understat(session)
            table = await understat.get_league_table(self.league, self.season)
            headers = table.pop(0)
            self.data = pd.DataFrame.from_records(table, columns=headers)

    def execute(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.fetch_data())

        return self.data
