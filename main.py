"""
PyCandleStrat

MIT License 2024
"""

from analysis import Strategy

country = "US"
pattern = "hammer"
start_date = "2024-04-01"

strat = Strategy(country, pattern, start_date)
strat.print_data(10)
strat.initial_plot()
strat.analyse_pattern()