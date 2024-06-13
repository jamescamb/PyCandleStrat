"""
Make plots of financial data
"""

# Import libraries
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

from typing import Optional
from data import check_date, filter_data

def summary_plot(country: str,
                 data: pd.DataFrame,
                 start_date: Optional[str] = "2000-01-01",
                 end_date: Optional[str] = "2025-01-01") -> None:
    """
    Plot the overall trends of a dataset
    """

    # Start and end dates need to be in form 'YYYY-MM-DD'
    check_date(start_date)
    check_date(end_date)
    filtered_df = filter_data(data, start_date, end_date)

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

def candlestick_plot(country: str,
                     data: pd.DataFrame,
                     start_date: Optional[str] = "2000-01-01",
                     end_date: Optional[str] = "2025-01-01") -> None:
    """
    Plot a candelstick chart from a dataset
    """

    # Start and end dates need to be in form 'YYYY-MM-DD'
    check_date(start_date)
    check_date(end_date)
    filtered_df = filter_data(data, start_date, end_date).copy()

    filtered_df.rename(columns={"Price": "Close"}, inplace=True)
    filtered_df = filtered_df.set_index("Date")
 
    mpf.plot(filtered_df.iloc[::-1],
             type="candle",
             style="charles",
             title=country,
             ylabel="Yield [%]",
             xlabel="Trading Days")