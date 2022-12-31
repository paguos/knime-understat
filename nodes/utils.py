from datetime import date

from config import TeamStat


def parse_team_stats(stats, team_stat: TeamStat) -> []:
    result = []
    for category, data in stats[team_stat.value].items():
        row = []
        row.append(category)

        for metric, value in data.items():
            if metric == "stat":
                continue

            if metric == "against":
                against_values = [s for s in value.values()]
            else:
                row.append(value)

        row = row + against_values
        result.append(row)

    return result


def parse_player_stats(stats) -> []:
    result = []
    for s in stats:
        position = s["position"]

        for metric, data in s.items():
            if metric == "position":
                continue
            result.append([position, metric] + list(data.values()))
    return result


def current_season() -> int:
    return __get_season(date.today())


def __get_season(input_date: date) -> int:
    end_season = date(day=30, month=6, year=input_date.year)
    delta = input_date - end_season

    if delta.days > 0:
        return input_date.year
    else:
        return input_date.year - 1
