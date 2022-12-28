import knime_extension as knext
import logging
import utils

from config import Competition
from task import LeaguePlayersTask
from task import LeagueTableTask

LOGGER = logging.getLogger(__name__)


class BaseNode:

    configure = []

    def configure(self, configure_context):
        pass


@knext.parameter_group(label="League Settings")
class LeagueNodeSettings:
    league = knext.StringParameter(
        "Competition",
        "The league's name (e.g. EPL, La Liga, Serie A, Bundesliga, Ligue 1)",
        Competition.EPL.name,
        enum=[en.value for en in Competition]
    )

    season = knext.IntParameter(
        "Season",
        "The league's season (e.g. 2019, 2020)",
        utils.current_season(),
        min_value=2014
    )


@knext.node(
    name="Understat League Table",
    node_type=knext.NodeType.SOURCE,
    icon_path="resources/football-award.png",
    category="/community"
)
@knext.output_table(
    name="Output Data",
    description="The collected data for a league in a specified season."
)
class LeagueTableNode(BaseNode):
    """
    Fetches the standings of the given league in the given season
    from the [understat's website](https://understat.com).

    This node uses the [understat python package](https://understat.readthedocs.io/).
    """

    settings = LeagueNodeSettings()

    def execute(self, exec_context):
        step = LeagueTableTask(league=self.settings.league,
                               season=self.settings.season)
        return knext.Table.from_pandas(step.execute())


@knext.node(
    name="Understat League Players",
    node_type=knext.NodeType.SOURCE,
    icon_path="resources/football-team.png",
    category="/community"
)
@knext.output_table(
    name="Output Data",
    description="The collected data for a league in a specified season."
)
class LeaguePlayersNode(BaseNode):
    """
    Fetches a list of players of a given league and season
    from the [understat's website](https://understat.com).

    This node uses the [understat python package](https://understat.readthedocs.io/).

    The node's icon was designed by Nikita Golubev, and obtained
    for free in [flaticon.com](https://www.flaticon.com/free-icon/team_2257031?term=soccer).
    """

    settings = LeagueNodeSettings()

    def execute(self, exec_context):
        step = LeaguePlayersTask(league=self.settings.league,
                                 season=self.settings.season)
        return knext.Table.from_pandas(step.execute())
