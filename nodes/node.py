import knime_extension as knext
import logging
import utils

from config import Competition
from config import LeagueOperation
from task import LeagueTask

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
