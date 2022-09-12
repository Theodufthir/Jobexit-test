import sys
import math
import datetime as dt

# Returns the rate for a month
def compute_month_rate(ptime_list, month, year):
    res = 0 # result
    ptime = 0 # used to count the total proportion of part time
    month_len = (dt.date(year + month // 12, month % 12 + 1, 1) - dt.date(year, month, 1)).days
    for (start, end, rate) in ptime_list:
        period_len = (end - start).days + 1
        res += rate * (period_len / month_len) # adding part time rate
        ptime += period_len / month_len
    res += (1 - ptime) # adding full time rate
    return 1 / res
