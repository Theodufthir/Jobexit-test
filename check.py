import datetime as Date

Period = tuple[Date, Date, float]

# Check if there are overlapping periods in the part time period list
def check_overlapping_periods(periods: list[Period]):
    rev_periods: list[Period] = periods.copy()
    rev_periods.reverse()

    i: int = 0
    for (start_1, end_1, _) in periods:
        i += 1
        j: int = 0
        for (start_2, end_2, _) in rev_periods:
            j += 1
            if i == j:
                continue
            if start_1 >= start_2 and start_1 < end_2:
                raise ValueError(f"Period {i} starts in period {j}")
            if end_1 <= end_2 and end_1 > start_1:
                raise ValueError(f"Period {i} ends in period {j}")


# Check if a period had the beginning date before the ending date
def check_inversed_dates(periods: list[Period], start, end):
    if start > end:
        raise ValueError("The start date of the employement is later than its end date")

    i: int = 0
    for (p_start, p_end, _) in periods:
        i += 1
        if p_start > p_end:
            raise ValueError(f"Period {i} start date is later than its end date")
        if p_start < start:
            raise ValueError(f"Period {i} start date is later than start date of the employement")
        if p_end > end:
            raise ValueError(f"Period {i} end date is later than the end date of the employement")

# Check if any rate is over 1 or negative
def check_invalid_rate(periods: list[Period]):
    i: int = 0
    for (_, _, rate) in periods:
        i += 1
        if rate > 1 or rate < 0:
            raise ValueError(f"Period {i}: Rate should be between 0 and 1")


# Check if the validity of all the data
def check_validity(periods: list, start: Date, end: Date):
    check_invalid_rate(periods)
    check_inversed_dates(periods, start, end)
    check_overlapping_periods(periods)
