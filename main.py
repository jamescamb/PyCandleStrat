"""
PyCandleStrat

MIT License 2024
"""

from analysis import Strategy

country = "US"
pattern = "piercing"
start_date = "2024-04-01"

strat = Strategy(country, pattern, start_date)
#strat.print_data(10)
strat.initial_plot()
strat.analyse_pattern()

# TODO:
# Finish candlestick patterns
# Momentum trader
# Hidden Markov model
# Monte Carlo simulations
# ML approaches