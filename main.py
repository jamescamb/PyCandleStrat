"""
PyCandleStrat

MIT License 2024
"""

from analysis import Identify
from trading import Strategy

country = "US"
pattern = "all"
start_date = "2024-01-01"

ident = Identify(country, pattern, start_date)
#ident.print_data(10)
ident.initial_plot()
df = ident.analyse_pattern()
strat = Strategy(df)
returns = strat.evaluate()

# TODO:
# Finish candlestick patterns
# Momentum trader
# Hidden Markov model
# Monte Carlo simulations
# ML approaches
# Options pricing