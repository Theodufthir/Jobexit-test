import datetime as Date
from calendar import monthrange

Period = tuple[Date, Date, float]

# Returns the rate for a month
def compute_month_rate(ptime_list: list[Period], year: Date, month: Date) -> float:
    res: float = 0 # result
    ptime: float = 0 # used to count the total proportion of part time
    month_len: int = monthrange(year, month)[1]

    for (start, end, rate) in ptime_list:
        period_len: int = end.day - start.day + 1
        res += rate * (period_len / month_len) # adding part time rate
        ptime += period_len / month_len
    res += (1 - ptime) # adding full time rate

    return round(res, 2)

# Returns the list of rates for all months
def compute_all_months_rates(month_periods: list[list[Period]], start: Date, end: Date) -> list[float]:
    month_rates: list[float] = []
    curr_year: int = start.year
    curr_month: int = start.month
    for month in month_periods:
        month_rates.append(compute_month_rate(month, curr_year, curr_month))
        curr_year += 1 if (curr_month == 12) else 0
        curr_month = curr_month % 12 + 1
    return month_rates
