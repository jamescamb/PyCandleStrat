"""
PyCandleStrat

MIT License 2024
"""

from analysis import Identify
from trading import Strategy

country = "US"
pattern = "all"
start_date = "2024-01-01"

#### DATA ANALYSIS
ident = Identify(country, pattern, start_date)
#ident.print_data(10)
#ident.initial_plot()
mc_df = ident.monte_carlo(20)
cs_df = ident.analyse_pattern()

### TRADING ANALYSIS
strat = Strategy(country, cs_df, mc_df)
returns = strat.evaluate()

# TODO:
# Finish candlestick patterns
# Momentum trader
# Hidden Markov model
# Monte Carlo simulations
# ML approaches
# Options pricing