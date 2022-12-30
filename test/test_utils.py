import json

import nodes.utils as utils

from freezegun import freeze_time

from nodes.config import TeamStat


def test_current_season():
    # Test day in the second half of the season
    with freeze_time("2015-03-20"):
        assert 2014 == utils.current_season()

    # Test day in the first half of the season
    with freeze_time("2015-09-20"):
        assert 2015 == utils.current_season()


def test_parse_team_stats():
    with open("test/resources/team_stats.json", "r") as f:
        stats = json.load(f)

    result = utils.parse_team_stats(stats, TeamStat.ATTACK_SPEED)
    expected_fast = ["Fast", 4, 22, 3.905101865530014, 1, 26, 3.631404686719179]
    expected_normal = ["Normal", 34, 250, 31.58086338173598, 24, 333, 30.250978828873485]

    assert len(result) == 4
    assert expected_fast in result
    assert expected_normal in result

    result = utils.parse_team_stats(stats, TeamStat.SITUATION)
    expected_penalty = ["Penalty", 3, 3, 2.283432960510254, 7, 8, 6.089350700378418]
    expected_open_play = ["OpenPlay", 42, 294, 39.762118372134864, 27, 401, 37.63162892917171]

    assert len(result) == 5
    assert expected_penalty in result
    assert expected_open_play in result
