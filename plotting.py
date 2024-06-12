"""
Make plots of financial data
"""

# Import libraries
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

def summary_plot(data: pd.DataFrame) -> pd.DataFrame:
    """
    Plot the overall trends of a dataset
    """

    plt.subplot(2, 1, 1)
    plt.plot(data["Date"], data["Price"])

    plt.show()