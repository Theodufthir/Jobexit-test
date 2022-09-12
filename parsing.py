from datetime import date
from time import strptime
import argparse as ap

# Returns a datetime object from a string with format YYYY-MM-DD
def str_to_date(string):
    tmp = strptime(string, "%Y-%m-%d")
    return date(tmp.tm_year, tmp.tm_mon, tmp.tm_mday)

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


# Parses all arguments and returns them
def parse_args():
    parser = ap.ArgumentParser()
    parser.add_argument("part_time_periods")
    parser.add_argument("start_date")
    parser.add_argument("end_date")
    args = parser.parse_args()

    periods = parse_list(args.part_time_periods)
    start = str_to_date(args.start_date)
    end = str_to_date(args.end_date)
    return (periods, start, end)
