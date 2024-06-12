"""
This tool allows the user to specify what candlestick pattern to look for in what context,
(i.e., bearish engulfing following 2 down days),
and return the optimal strategy in terms of buy or sell the following days open level, and stop,
target and take profit for different time horizons following the observation of that pattern,
along with some summary statistics on the returns from that strategy (i.e., win rate, return, SD of return).
We assume that so long as a stop or take profit is within the relevant time periods range, it was possible to trade there.
"""

from data import read_local_file, check_bad_values, correct_dates, correct_changes

df = read_local_file("US-bond-yield.csv")
if df is None:
    raise Exception("Program closing.")

check_bad_values(df)
correct_dates(df)
correct_changes(df)

print(df.head())