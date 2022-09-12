import datetime as Date
from datetime import date
import time as Time
from time import strptime
import argparse as ap

Period = tuple[Date, Date, float]

# Returns a datetime object from a string with format YYYY-MM-DD
def str_to_date(string: str) -> Date:
    tmp: time = strptime(string, "%Y-%m-%d")
    return date(tmp.tm_year, tmp.tm_mon, tmp.tm_mday)

# Parses the list of part time periods
def parse_list(raw: str) -> list[Period]:
    raw = raw[1:-1]
    res: list[Period] = []
    curr: list = []
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
def parse_args() -> Period:
    parser: ArgumentParser = ap.ArgumentParser()
    parser.add_argument("part_time_periods")
    parser.add_argument("start_date")
    parser.add_argument("end_date")
    args: str = parser.parse_args()

    periods: list[Period] = parse_list(args.part_time_periods)
    start: Date = str_to_date(args.start_date)
    end: Date = str_to_date(args.end_date)
    return (periods, start, end)
