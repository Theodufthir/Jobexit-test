import sys
import math
from datetime import date
from calendar import monthrange

# Returns the difference between two dates in months
def diff_month_nb(start, end):
    return (end.year - start.year) * 12 + end.month - start.month

# Returns the rate for a month
def compute_month_rate(ptime_list, month, year):
    res = 0 # result
    ptime = 0 # used to count the total proportion of part time
    month_len = monthrange(year, month)[1]
    
    for (start, end, rate) in ptime_list:
        period_len = (end - start).days + 1
        res += rate * (period_len / month_len) # adding part time rate
        ptime += period_len / month_len
    res += (1 - ptime) # adding full time rate
    
    return 1 / res

# Splits the part time periods that are shared between months to ones contained in it
def split_periods_monthly(ptime_list, start, end):
    
    # initialize the monthly list
    month_nb = diff_month_nb(start, end) + 1
    monthly_ptime_list = [[] for i in range(month_nb)]
    print(monthly_ptime_list)
    if ptime_list[0][0] < start:
        monthly_ptime_list[0].append((start, ptime_list[0][0], 0))
    
    # split part time periods and add to corresponding months
    for (p_start, p_end, p_rate) in ptime_list:
        p_month_nb = diff_month_nb(p_start, p_end)
        starting_index = diff_month_nb(start, p_start)

        if (p_month_nb == 0):
            monthly_ptime_list[starting_index].append((p_start, p_end, p_rate))
            continue

        curr_year = p_start.year
        curr_month = p_start.month
        new_period = (
                p_start,
                date(curr_year, curr_month, monthrange(curr_year, curr_month)[1]),
                p_rate)
        monthly_ptime_list[starting_index].append(new_period)
        
        ending_index = diff_month_nb(start, p_end)

        for i in range(starting_index + 1, ending_index):
            curr_year += 1 if (curr_month == 12) else 0
            curr_month = curr_month % 12 + 1
        
            new_period = (
                    date(curr_year, curr_month, 1),
                    date(curr_year, curr_month, monthrange(curr_year, curr_month)[1]),
                    p_rate)
            monthly_ptime_list[i].append(new_period)

        new_period = (date(curr_year, curr_month, 1), p_end, p_rate)
        monthly_ptime_list[ending_index].append(new_period)

    return monthly_ptime_list
