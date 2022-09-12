from parsing import parse_args
from split import split_periods_monthly
from compute import compute_all_months_rates

(periods, start, end) = parse_args()
split = split_periods_monthly(periods, start, end)
print(compute_all_months_rates(split, start, end))

