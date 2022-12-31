import knime_extension as knext
import logging
import utils

from config import Competition
from config import LeagueOperation
from config import TeamOperation
from config import PlayerOperation
from config import TeamStat
from task import LeagueTask
from task import TeamTask
from task import PlayerTask

LOGGER = logging.getLogger(__name__)


class BaseNode:

    configure = []

    def configure(self, configure_context):
        pass


@knext.parameter_group(label="League Settings")
class LeagueNodeSettings:

    information = knext.StringParameter(
        "Information",
        "The desired league's information.",
        LeagueOperation.TABLE.value,
        enum=[en.value for en in LeagueOperation]
    )

    league = knext.StringParameter(
        "Competition",
        "The league's name (e.g. EPL, La Liga, Serie A, Bundesliga, Ligue 1)",
        Competition.EPL.value,
        enum=[en.value for en in Competition]
    )

    season = knext.IntParameter(
        "Season",
        "The league's season (e.g. 2019, 2020)",
        utils.current_season(),
        min_value=2014
    )


@knext.parameter_group(label="Team Settings")
class TeamNodeSettings:

    information = knext.StringParameter(
        "Information",
        "The desired league's information.",
        TeamOperation.PLAYERS.value,
        enum=[en.value for en in TeamOperation]
    )

    team = knext.StringParameter(
        "Team Name",
        "The team's name (e.g. Barcelona, Liverpool, Manchester City)",
    )

    season = knext.IntParameter(
        "Season",
        "The league's season (e.g. 2019, 2020)",
        utils.current_season(),
        min_value=2014
    )

    team_stat = knext.StringParameter(
        "Stat",
        "The desired league's information.",
        TeamStat.SITUATION.value,
        enum=[en.value for en in TeamStat]
    )


@knext.parameter_group(label="Player Settings")
class PlayerNodeSettings:

    information = knext.StringParameter(
        "Information",
        "The desired player's information.",
        PlayerOperation.STATS.value,
        enum=[en.value for en in PlayerOperation]
    )

    player_id = knext.IntParameter(
        "Player id",
        "The player's id",
        1,
        min_value=1
    )


@knext.node(
    name="Understat League Reader",
    node_type=knext.NodeType.SOURCE,
    icon_path="resources/football-award.png",
    category="/community"
)
@knext.output_table(
    name="Output Data",
    description="The collected data for a league in a specified season."
)
class LeagueNode(BaseNode):
    """
    Fetches information of a league in the given season
    from the [understat's website](https://understat.com).

    This node uses the [understat python package](https://understat.readthedocs.io/).

    The node's icon was designed by Freepik, and obtained
    for free via [flaticon.com](https://www.flaticon.com/free-icon/football-award_2374785?term=football).
    """

    settings = LeagueNodeSettings()

    def execute(self, exec_context):

        information = LeagueOperation(self.settings.information)

        step = LeagueTask(information, league=self.settings.league,
                          season=self.settings.season)

        return knext.Table.from_pandas(step.execute())


@knext.node(
    name="Understat Team Reader",
    node_type=knext.NodeType.SOURCE,
    icon_path="resources/football-team.png",
    category="/community"
)
@knext.output_table(
    name="Output Data",
    description="The collected data for a team in a specified season."
)
class TeamNode(BaseNode):
    """
    Fetches information of a team in the given season
    from the [understat's website](https://understat.com).

    This node uses the [understat python package](https://understat.readthedocs.io/).

    The node's icon was designed by Nikita Golubev, and obtained
    for free via [flaticon.com](https://www.flaticon.com/free-icon/team_2257031).
    """

    settings = TeamNodeSettings()

    def execute(self, exec_context):

        information = TeamOperation(self.settings.information)
        stat = TeamStat(self.settings.team_stat)

        step = TeamTask(information, team_name=self.settings.team,
                        season=self.settings.season, stat=stat)

        return knext.Table.from_pandas(step.execute())


@knext.node(
    name="Understat Player Reader",
    node_type=knext.NodeType.SOURCE,
    icon_path="resources/soccer-player.png",
    category="/community"
)
@knext.output_table(
    name="Output Data",
    description="The collected data of a player."
)
class PlayerNode(BaseNode):
    """
    Fetches information of a player
    from the [understat's website](https://understat.com).

    This node uses the [understat python package](https://understat.readthedocs.io/).

    The node's icon was designed by  kosonicon, and obtained
    for free via [flaticon.com](https://www.flaticon.com/free-icon/soccer-player_4049083).
    """

    settings = PlayerNodeSettings()

    def execute(self, exec_context):

        information = PlayerOperation(self.settings.information)

        step = PlayerTask(information, self.settings.player_id)
        return knext.Table.from_pandas(step.execute())
