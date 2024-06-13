"""
Analysis of candelstick patterns
"""

# Import libraries
from typing import Optional
from data import read_local_file, check_bad_values, correct_dates, correct_changes
from plotting import summary_plot, candlestick_plot

# List potential candlestick patterns
patterns = ["hammer",
            "inv_hammer",
            "bull_engulf",
            "piercing",
            "morning",
            "soldiers",
            "hanging",
            "shooting",
            "bear_engulf",
            "evening",
            "crows",
            "cloud",
            "doji",
            "spinning",
            "falling",
            "rising"]

class Strategy:
    """
    OOP strategy class
    """

    def __init__(self,
                 country: str,
                 pattern: str,
                 start_date: Optional[str] = "2000-01-01",
                 end_date: Optional[str] = "2025-01-01"):

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
        
        self.data = df

    def initial_plot(self):

        summary_plot(self.country, self.data, self.start_date, self.end_date)
        candlestick_plot(self.country, self.data, self.start_date, self.end_date)

    def initialise(self):

        print("Country:", self.country)
        print("Pattern:", self.pattern)


