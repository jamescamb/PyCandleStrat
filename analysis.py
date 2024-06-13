"""
Analysis of candelstick patterns
"""

# Import libraries
import pandas as pd

from data import read_local_file, check_bad_values, correct_dates, correct_changes

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

    def __init__(self, country: str, pattern: str):

        self.country = country
        self.pattern = pattern

        filename = country + "-bond-yield.csv"
        df = read_local_file(filename)
        if df is None:
            raise Exception("Program closing.")
        else:
            check_bad_values(df)
            correct_dates(df)
            correct_changes(df)
        
        self.data = df

    def initialise(self):

        print("Country:", self.country)
        print("Pattern:", self.pattern)


