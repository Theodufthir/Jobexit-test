import datetime as Date
from parsing import parse_args
from split import split_periods_monthly
from compute import compute_all_months_rates
from check import check_validity

Period = tuple[Date, Date, float]

(periods, start, end) = parse_args()
check_validity(periods, start, end)
split, start = split_periods_monthly(periods, start, end)
print(compute_all_months_rates(split, start, end))

