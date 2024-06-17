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
            df.sort_values(by = "Date", inplace = True)
        
        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        self.data = df.loc[mask]
    
    def print_data(self, number: int) -> None:
        
        print("Printing dataframe of top {} values by date".format(number))
        print(self.data.head(number))

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
        window_size = 7
        self.data["Min"] = (self.data["Price"] == self.data["Price"].rolling(window=window_size, center=True).min())

        if self.pattern == "hammer":
            print("Searching for bullish hammer pattern")
            self.hammer()
        elif self.pattern == "inv_hammer":
            print("Searching for bullish inverse hammer pattern")
            self.inv_hammer()
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

        # Lower wick >= 150% of body
        mask_long_wick = (1.5*self.data["Body"] <= self.data["L-Wick"])
        # Body within the 25th percentile
        q1_body = self.data["Body"].quantile(0.25)
        mask_short_body = self.data["Body"] <= q1_body
        # Local minimum
        mask_minimum = self.data["Min"] == True
        
        mask = mask_long_wick & mask_short_body & mask_minimum
        filtered_data = self.data.loc[mask]

        if filtered_data.empty:
            print("No hammer pattern detected from", self.start_date, "to", self.end_date)
        else:
            print("Hammer patterns detected at:")
            print(filtered_data)
        
        return filtered_data

    def inv_hammer(self) -> pd.DataFrame:
        """
        A similarly bullish pattern is the inverted hammer.
        The only difference being that the upper wick is long,
        while the lower wick is short.
        
        It indicates a buying pressure,
        followed by a selling pressure that was not strong enough to drive the market price down.
        The inverse hammer suggests that buyers will soon have control of the market.
        """

        # Lower wick <= 25% of body
        mask_short_wick = (0.25*self.data["Body"] >= self.data["L-Wick"])
        # Upper wick >= 150% of body
        mask_long_wick = (self.data["Body"] <= self.data["U-Wick"])
        # Local minimum
        mask_minimum = self.data["Min"] == True

        mask = mask_short_wick & mask_long_wick & mask_minimum
        filtered_data = self.data.loc[mask]

        if filtered_data.empty:
            print("No inverse hammer pattern detected from", self.start_date, "to", self.end_date)
        else:
            print("Inverse hammer patterns detected at:")
            print(filtered_data)

        return filtered_data
    
