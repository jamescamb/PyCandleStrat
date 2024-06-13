"""
This tool allows the user to specify what candlestick pattern to look for in what context,
(i.e., bearish engulfing following 2 down days),
and return the optimal strategy in terms of buy or sell the following days open level, and stop,
target and take profit for different time horizons following the observation of that pattern,
along with some summary statistics on the returns from that strategy (i.e., win rate, return, SD of return).
We assume that so long as a stop or take profit is within the relevant time periods range, it was possible to trade there.
"""

from analysis import Strategy

country = "US"
pattern = "hammer"

strat = Strategy(country, pattern, "2024-01-01")
strat.initial_plot()
