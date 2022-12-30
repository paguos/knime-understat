from nodes.task import LeagueTask, LeagueOperation
from nodes.task import TeamTask, TeamOperation, TeamStat


def test_league_table_task():
    step = LeagueTask(LeagueOperation.TABLE, "EPL", "2019")
    df = step.execute()

    expected_rows = 20
    expected_columns = [
        'Team', 'M', 'W', 'D', 'L', 'G', 'GA', 'PTS', 'xG', 'NPxG',
        'xGA', 'NPxGA', 'NPxGD', 'PPDA', 'OPPDA', 'DC', 'ODC', 'xPTS'
    ]

    assert df.shape == (expected_rows, len(expected_columns))
    assert expected_columns == list(df.columns)


def test_league_players_task():
    task = LeagueTask(LeagueOperation.PLAYERS, "EPL", "2019")
    df = task.execute()

    expected_rows = 514
    expected_columns = [
        'id', 'player_name', 'games', 'time', 'goals',
        'xG', 'assists', 'xA', 'shots', 'key_passes',
        'yellow_cards', 'red_cards', 'position', 'team_title', 'npg',
        'npxG', 'xGChain', 'xGBuildup'
    ]

    assert df.shape == (expected_rows, len(expected_columns))
    assert expected_columns == list(df.columns)


def test_team_players_task():
    task = TeamTask(TeamOperation.PLAYERS, "Arsenal", "2019")
    df = task.execute()
    expected_rows = 28
    expected_columns = [
        'id', 'player_name', 'games', 'time', 'goals',
        'xG', 'assists', 'xA', 'shots', 'key_passes',
        'yellow_cards', 'red_cards', 'position', 'team_title', 'npg',
        'npxG', 'xGChain', 'xGBuildup'
    ]

    assert df.shape == (expected_rows, len(expected_columns))
    assert expected_columns == list(df.columns)


def test_team_stats_task():
    task = TeamTask(TeamOperation.STATS, "Arsenal", "2019")
    df = task.execute()
    expected_rows = 5
    expected_columns = [
        "situation",
        "shots",
        "goals",
        "xG",
        "shots (against)",
        "goals (against)",
        "xG (against)"
    ]

    assert df.shape == (expected_rows, len(expected_columns))
    assert expected_columns == list(df.columns)

    task = TeamTask(TeamOperation.STATS, "Arsenal", "2019", TeamStat.FORMATION)
    df = task.execute()
    expected_rows = 10
    expected_columns = [
        "formation",
        "time",
        "shots",
        "goals",
        "xG",
        "shots (against)",
        "goals (against)",
        "xG (against)"
    ]

    assert df.shape == (expected_rows, len(expected_columns))
    assert expected_columns == list(df.columns)
