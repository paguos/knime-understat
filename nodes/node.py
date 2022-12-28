import knime_extension as knext
import logging
import utils

from config import Competition
from task import LeagueTableTask

LOGGER = logging.getLogger(__name__)


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
class LeagueTableNode:
    """
    Fetches the standings of the given league in the given season
    from the [understat's website](https://understat.com).

    This node uses the [understat python package](https://understat.readthedocs.io/).
    """

    configure = []

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

    def configure(self, configure_context):
        pass

    def execute(self, exec_context):
        step = LeagueTableTask(league=self.league,
                               season=self.season)
        return knext.Table.from_pandas(step.execute())
