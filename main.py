from datetime import date
from time import strptime
from calendar import monthrange
import argparse as ap

# Returns the difference between two dates in months
def diff_month_nb(start, end):
    return (end.year - start.year) * 12 + end.month - start.month


# Returns a datetime object from a string with format YYYY-MM-DD
def str_to_date(string):
    tmp = strptime(string, "%Y-%m-%d")
    return date(tmp.tm_year, tmp.tm_mon, tmp.tm_mday)


# Returns the rate for a month
def compute_month_rate(ptime_list, year, month):
    res = 0 # result
    ptime = 0 # used to count the total proportion of part time
    month_len = monthrange(year, month)[1]

    for (start, end, rate) in ptime_list:
        period_len = end.day - start.day + 1
        res += rate * (period_len / month_len) # adding part time rate
        ptime += period_len / month_len
    res += (1 - ptime) # adding full time rate

    return res

# Returns the list of rates for all months
def compute_all_months_rates(month_periods, start, end):
    month_rates = []
    curr_year = start.year
    curr_month = start.month
    for month in month_periods:
        month_rates.append(compute_month_rate(month, curr_year, curr_month))
        curr_year += 1 if (curr_month == 12) else 0
        curr_month = curr_month % 12 + 1
    return month_rates


# Splits the part time periods that are shared between months to ones contained in it
def split_periods_monthly(ptime_list, start, end):

    # initialize the monthly list
    month_nb = diff_month_nb(start, end) + 1
    monthly_ptime_list = [[] for i in range(month_nb)]
    if ptime_list[0][0] < start:
        monthly_ptime_list[0].append((start, ptime_list[0][0], 0))

    # loop on non-split part time periods
    for (p_start, p_end, p_rate) in ptime_list:
        p_month_nb = diff_month_nb(p_start, p_end)
        starting_index = diff_month_nb(start, p_start)

        # if the period is within the month, no need to split
        if (p_month_nb == 0):
            monthly_ptime_list[starting_index].append((p_start, p_end, p_rate))
            continue

        # adding the start of the part time period to the month
        curr_year = p_start.year
        curr_month = p_start.month
        new_period = (
                p_start,
                date(curr_year, curr_month, monthrange(curr_year, curr_month)[1]),
                p_rate)
        monthly_ptime_list[starting_index].append(new_period)

        ending_index = diff_month_nb(start, p_end)

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


# Parses the list of part time periods
def parse_list(raw):
    raw = raw[1:-1]
    res = []
    curr = []
    for substr in raw.split(','):
        if '(' in substr:
            curr.append(str_to_date(substr.replace('(', '')))
        elif ')' in substr:
            curr.append(float(substr.replace(')', '')))
            res.append(tuple(curr))
            curr = []
        else:
            curr.append(str_to_date(substr))
    return res


# Adding arguments and parsing
parser = ap.ArgumentParser()
parser.add_argument("part_time_periods")
parser.add_argument("start_date")
parser.add_argument("end_date")
args = parser.parse_args()

periods = parse_list(args.part_time_periods)
start = str_to_date(args.start_date)
end = str_to_date(args.end_date)

split = split_periods_monthly(periods, start, end)

# Main
print(compute_all_months_rates(split, start, end))

