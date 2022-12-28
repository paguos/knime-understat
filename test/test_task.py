
from nodes.task import LeagueTableTask


def test_execute():
    step = LeagueTableTask("EPL", "2019")
    df = step.execute()

    expected_rows = 20
    expected_columns = [
        'Team', 'M', 'W', 'D', 'L', 'G', 'GA', 'PTS', 'xG', 'NPxG',
        'xGA', 'NPxGA', 'NPxGD', 'PPDA', 'OPPDA', 'DC', 'ODC', 'xPTS'
    ]

    assert df.shape == (expected_rows, len(expected_columns))
    assert expected_columns == list(df.columns)
