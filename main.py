"""
PyCandleStrat

MIT License 2024
"""

from analysis import Identify
from trading import Execute

#######################
##### GLOBAL VARS #####
#######################

COUNTRY = "US"
PATTERN = "all"
START = "2024-01-01"
MC_COPIES = 20

#######################
#### DATA ANALYSIS ####
#######################

real = Identify(COUNTRY, PATTERN, printout=True, start_date=START)
#real.print_data(10)
real.initial_plot()
real.analyse_pattern()
mc_data = real.monte_carlo(MC_COPIES)

synthetic = Identify(COUNTRY, PATTERN, start_date=START, import_df=mc_data)
df = synthetic.analyse_pattern()

##########################
#### TRADING ANALYSIS ####
##########################

strat = Execute(COUNTRY, df)
returns = strat.evaluate()

# TODO:
# Fix derivative calculations
# Finish candlestick patterns
# Momentum trader
# Hidden Markov model
# Monte Carlo simulations
# ML approaches
# Options pricing