"""
Make plots of financial data
"""

# Import libraries
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

from data import check_date
from typing import Optional

def summary_plot(country: str,
                 data: pd.DataFrame,
                 start_date: Optional[str] = "2000-01-01",
                 end_date: Optional[str] = "2025-01-01",) -> pd.DataFrame:
    """
    Plot the overall trends of a dataset
    """

    # Start and end dates need to be in form 'YYYY-MM-DD'
    check_date(start_date)
    check_date(end_date)

    start_date = pd.to_datetime(start_date, format="%Y-%m-%d")
    end_date = pd.to_datetime(end_date, format="%Y-%m-%d")
    mask = (data["Date"] >= start_date) & (data["Date"] <= end_date)
    filtered_df = data.loc[mask]

    plt.subplot(3, 1, 1)
    plt.title(country + " 10-Year Bond Yield")
    plt.plot(range(len(filtered_df))[::-1], filtered_df["Price"])
    plt.xticks([])
    plt.ylabel("Yield [%]")

    plt.subplot(3, 1, 2)
    colors = ['g' if x > 0 else 'r' for x in filtered_df["Change %"]]
    plt.bar(range(len(filtered_df))[::-1], filtered_df["Change %"], color=colors, width=1)
    plt.xticks([])
    plt.ylabel("Change [%]")

    plt.subplot(3, 1, 3)
    window_size = 10
    plt.plot(range(len(filtered_df))[::-1], filtered_df["Change %"].rolling(window_size).std())
    plt.xlabel("Trading Days")
    plt.ylabel("Volatility")

    plt.show()