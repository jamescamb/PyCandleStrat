"""
Analysis of candelstick patterns
"""

# Import libraries
import pandas as pd

from typing import Optional
from data import read_local_file, check_bad_values, correct_dates, correct_changes
from plotting import summary_plot, candlestick_plot

# List potential candlestick patterns
patterns = ["hammer", "inv_hammer",
            "bull_engulf", "piercing",
            "morning", "soldiers",
            "hanging", "shooting",
            "bear_engulf", "evening",
            "crows", "cloud",
            "doji", "spinning",
            "falling", "rising"]

class Strategy:
    """
    OOP strategy class
    """

    def __init__(self,
                 country: str,
                 pattern: str,
                 start_date: Optional[str] = "2000-01-01",
                 end_date: Optional[str] = "2025-01-01") -> None:

        self.country = country
        self.pattern = pattern
        self.start_date = start_date
        self.end_date = end_date

        filename = country + "-bond-yield.csv"
        df = read_local_file(filename)
        if df is None:
            raise Exception("Program closing.")
        else:
            check_bad_values(df)
            correct_dates(df)
            correct_changes(df)
        
        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        self.data = df.loc[mask]

    def initial_plot(self) -> None:
        
        # Print summary plot
        print("Printing summary plot")
        summary_plot(self.country, self.data)
        # Print candlestick plot
        print("Printing candelstick plot")
        candlestick_plot(self.country, self.data)
    
    def analyse_pattern(self) -> None:

        # Calculate body length
        self.data["Body"] = abs(self.data["Open"] - self.data["Price"])
        # Calculate lower wick length
        self.data["L-Wick"] = self.data[["Open", "Price"]].min(axis=1) - self.data["Low"]
        # Calculate the upper wick length
        self.data["U-Wick"] = self.data["High"] - self.data[["Open", "Price"]].max(axis=1)
        # Calculate local minimum over window size
        window_size = 10
        self.data["Min"] = (self.data["Price"] == self.data["Price"].rolling(window=window_size, center=True).min())

        if self.pattern == "hammer":
            print("Searching for bullish hammer pattern")
            self.hammer()
        else:
            print("Error: Pattern not recognised")

    def hammer(self) -> pd.DataFrame:
        """
        The hammer candlestick pattern is formed of a short body with a long lower wick,
        and is found at the bottom of a downward trend.
        
        A hammer shows that although there were selling pressures during the day,
        ultimately a strong buying pressure drove the price back up.
        The colour of the body can vary,
        but green hammers indicate a stronger bull market than red hammers.
        """

        # Lower wick >= 200% of body
        mask_long_wick = (2*self.data["Body"] <= self.data["L-Wick"])
        # Body within the 20th percentile
        q1_body = self.data["Body"].quantile(0.20)
        mask_short_body = self.data["Body"] <= q1_body
        # Local minimum
        mask_minimum = self.data["Min"] == True
        
        mask = mask_long_wick & mask_short_body & mask_minimum
        filtered_data = self.data.loc[mask]
        
        return filtered_data


