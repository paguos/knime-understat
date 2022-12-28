from datetime import date


def current_season() -> int:
    return __get_season(date.today())


def __get_season(input_date: date) -> int:
    end_season = date(day=30, month=6, year=input_date.year)
    delta = input_date - end_season

    if delta.days > 0:
        return input_date.year
    else:
        return input_date.year - 1
