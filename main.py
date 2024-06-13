"""
This tool allows the user to specify what candlestick pattern to look for in what context,
(i.e., bearish engulfing following 2 down days),
and return the optimal strategy in terms of buy or sell the following days open level, and stop,
target and take profit for different time horizons following the observation of that pattern,
along with some summary statistics on the returns from that strategy (i.e., win rate, return, SD of return).
We assume that so long as a stop or take profit is within the relevant time periods range, it was possible to trade there.
"""

from data import read_local_file, check_bad_values, correct_dates, correct_changes
from plotting import summary_plot, candlestick_plot
from analysis import Strategy

country = "US"
pattern = "hammer"

strat = Strategy(country, pattern)
strat.initialise()

start_date = "2024-01-11"
end_date = "2024-06-11"

summary_plot(country, strat.data, start_date, end_date)
candlestick_plot(country, strat.data, start_date, end_date)