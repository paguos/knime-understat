
from nodes.task import LeaguePlayersTask
from nodes.task import LeagueTableTask


def test_league_table_task():
    step = LeagueTableTask("EPL", "2019")
    df = step.execute()

    expected_rows = 20
    expected_columns = [
        'Team', 'M', 'W', 'D', 'L', 'G', 'GA', 'PTS', 'xG', 'NPxG',
        'xGA', 'NPxGA', 'NPxGD', 'PPDA', 'OPPDA', 'DC', 'ODC', 'xPTS'
    ]

    assert df.shape == (expected_rows, len(expected_columns))
    assert expected_columns == list(df.columns)


def test_league_players_task():
    step = LeaguePlayersTask("EPL", "2019")
    df = step.execute()

    expected_rows = 514
    expected_columns = [
        'id', 'player_name', 'games', 'time', 'goals',
        'xG', 'assists', 'xA', 'shots', 'key_passes',
        'yellow_cards', 'red_cards', 'position', 'team_title', 'npg',
        'npxG', 'xGChain', 'xGBuildup'
    ]

    assert df.shape == (expected_rows, len(expected_columns))
    assert expected_columns == list(df.columns)
