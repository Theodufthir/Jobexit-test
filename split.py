import datetime as Date
from datetime import date
from calendar import monthrange

Period = tuple[Date, Date, float]

# Returns the difference between two dates in months
def diff_month_nb(start: Date, end: Date) -> int:
    return (end.year - start.year) * 12 + end.month - start.month


# Splits the part time periods that are shared between months to ones contained in it
def split_periods_monthly(ptime_list: list[Period], start: Date, end: Date) -> list[Period]:

    # initialize the monthly list
    month_nb: int = diff_month_nb(start, end) + 1
    monthly_ptime_list: list[list[Period]] = [[] for i in range(month_nb)]

    # if the first month is not complete, we have to add an empty period to it
    first_month_start:Date = date(start.year, start.month, 1)
    if first_month_start < start:
        monthly_ptime_list[0].append((first_month_start, start, 0))

    # loop on non-split part time periods
    for (p_start, p_end, p_rate) in ptime_list:
        p_month_nb: int = diff_month_nb(p_start, p_end)
        starting_index: int = diff_month_nb(start, p_start)

        # if the period is within the month, no need to split
        if (p_month_nb == 0):
            monthly_ptime_list[starting_index].append((p_start, p_end, p_rate))
            continue

        # adding the start of the part time period to the month
        curr_year: int = p_start.year
        curr_month: int = p_start.month
        new_period: Period = (
                p_start,
                date(curr_year, curr_month, monthrange(curr_year, curr_month)[1]),
                p_rate)
        monthly_ptime_list[starting_index].append(new_period)

        ending_index: int = diff_month_nb(start, p_end)

        # loop for full months within the period
        for i in range(starting_index + 1, ending_index):
            curr_year += 1 if (curr_month == 12) else 0
            curr_month = curr_month % 12 + 1

            new_period = (
                    date(curr_year, curr_month, 1),
                    date(curr_year, curr_month, monthrange(curr_year, curr_month)[1]),
                    p_rate)
            monthly_ptime_list[i].append(new_period)

        # adding the end of the part time period to the month
        new_period = (date(curr_year, curr_month, 1), p_end, p_rate)
        monthly_ptime_list[ending_index].append(new_period)

    # if the last month is not finished, we have to remove it
    if end.day < monthrange(end.year, end.month)[1]:
        monthly_ptime_list.pop()

    return monthly_ptime_list
