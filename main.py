"""
PyCandleStrat

MIT License 2024
"""

from analysis import Identify
from trading import Strategy
from data import resampled_data
from plotting import multiple_candlestick, monte_carlo_paths

country = "US"
pattern = "all"
start_date = "2024-01-01"

ident = Identify(country, pattern, start_date)
#ident.print_data(10)
#ident.initial_plot()
df = ident.analyse_pattern()
strat = Strategy(country, df)
returns = strat.evaluate()
new_df = resampled_data(country, 20)
multiple_candlestick(country, new_df, start_date)
monte_carlo_paths(country, new_df)

# TODO:
# Finish candlestick patterns
# Momentum trader
# Hidden Markov model
# Monte Carlo simulations
# ML approaches
# Options pricing