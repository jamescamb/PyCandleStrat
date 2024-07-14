"""
Analysis of candelstick patterns
"""

# Import libraries
import pandas as pd
import numpy as np

from typing import Optional, Tuple
from data import read_local_file, check_bad_values, correct_dates
from data import correct_changes, asym_rolling_minmax, expanding_quantiles
from data import resampled_data
from plotting import summary_plot, candlestick_plot, scatter_matrix_plot
from plotting import multiple_candlestick, monte_carlo_paths

# List potential candlestick patterns
patterns = ["hammer", "inv_hammer",
            "bull_engulf", "piercing",
            "morning", "soldiers",
            "hanging", "shooting",
            "bear_engulf", "evening",
            "crows", "cloud",
            "doji", "spinning",
            "falling", "rising"]

class Identify:
    """
    OOP identify class
    """

    def __init__(self,
                 country: str,
                 pattern: str,
                 printout: Optional[bool] = False,
                 start_date: Optional[str] = "2000-01-01",
                 end_date: Optional[str] = "2025-01-01",
                 import_df: Optional[pd.DataFrame] = None) -> None:

        self.country = country
        self.pattern = pattern
        self.printout = printout
        self.start_date = start_date
        self.end_date = end_date

        filename = country + "-bond-yield.csv"

        if import_df is not None:
            print("Importing bond yield data for", country)
            df = import_df
        else:
            df = read_local_file(filename)
        
        if df is None:
            raise Exception("Program closing.")
        elif import_df is None:
            check_bad_values(df)
            correct_dates(df)
            correct_changes(df)
            df.sort_values(["Date"], ignore_index=True, inplace=True)
        
        mask = (df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))
        self.data = df.loc[mask]
        print("Selected", self.data.shape[0], "entries")
    
    def print_data(self, number: int) -> None:
        """
        Print the dataframe
        """
        
        print("Printing dataframe of first {} values by date".format(number))
        print(self.data.head(number))

    def initial_plot(self) -> None:
        """
        Print some initial graphs
        """
        
        # Print summary plot
        print("Printing summary plot")
        summary_plot(self.country, self.data)
        # Print candlestick plot
        print("Printing candelstick plot")
        candlestick_plot(self.country, self.data)
        # Print scatter matrix plot
        print("Printing scatter matrix plot")
        scatter_matrix_plot(self.data)
    
    def generate_covariates(self) -> pd.DataFrame:
        """
        Calculate important derivative data
        """

        # Calculate body length
        self.data["Body"] = abs(self.data["Open"] - self.data["Price"])
        # Calculate lower wick length
        self.data["L-Wick"] = self.data[["Open", "Price"]].min(axis=1) - self.data["Low"]
        # Calculate the upper wick length
        self.data["U-Wick"] = self.data["High"] - self.data[["Open", "Price"]].max(axis=1)

        look_back, look_forward = 3, 1
        quantiles = [0.05, 0.25, 0.50]
        columns = [f"{int(q*100)}" + " " + "Body" for q in quantiles]
        # Add columns that describe the patterns and trends
        self.data["Pattern"] = ""
        self.data["Trend"] = ""
        
        if "DF" in self.data.columns:
            self.data["Min"] = False
            self.data["Max"] = False
            for i in range(self.data["DF"].iloc[-1] + 1):
                # Calculate quantile data of body length
                for col in columns:
                    self.data.loc[self.data["DF"] == i, col] = expanding_quantiles(self.data[self.data["DF"] == i], "Body", quantiles)[col]
                # Calculate local minimum over (asymmetrical) window size
                # We can only detect a local minimum look_forward days after it has happened
                self.data.loc[self.data["DF"] == i, "Min"] = (self.data[self.data["DF"] == i]["Price"] == asym_rolling_minmax(self.data[self.data["DF"] == i], look_back, look_forward, True))
                self.data.loc[self.data["DF"] == i, "Max"] = (self.data[self.data["DF"] == i]["Price"] == asym_rolling_minmax(self.data[self.data["DF"] == i], look_back, look_forward, False))
        else:
            # Calculate quantile data of body length
            result = expanding_quantiles(self.data, "Body", quantiles)
            self.data = pd.concat([self.data, result], axis=1)
            # Calculate local minimum over (asymmetrical) window size
            # We can only detect a local minimum look_forward days after it has happened
            self.data["Min"] = (self.data["Price"] == asym_rolling_minmax(self.data, look_back, look_forward, True))
            self.data["Max"] = (self.data["Price"] == asym_rolling_minmax(self.data, look_back, look_forward, False))

        return self.data
    
    def analyse_pattern(self) -> pd.DataFrame:
        """
        Analyse data for known patterns
        """

        self.generate_covariates()

        if self.pattern == "all":
            all = pd.concat([self.hammer(), self.inv_hammer(), self.bull_engulf(), self.piercing(),
                             self.morning(), self.soldiers(), self.hanging(), self.shooting(),
                             self.bear_engulf(), self.evening(), self.crows(), self.cloud(),
                             self.doji(), self.spinning(), self.falling(), self.rising()])
            all.sort_index(inplace=True)
            if self.printout:
                print(all)
                print(len(all), "patterns identified")
        elif self.pattern == "hammer":
            print("Searching for bullish hammer pattern")
            self.hammer()
        elif self.pattern == "inv_hammer":
            print("Searching for bullish inverse hammer pattern")
            self.inv_hammer()
        elif self.pattern == "bull_engulf":
            print("Searching for bullish engulfing pattern")
            self.bull_engulf()
        elif self.pattern == "piercing":
            print("Searching for bullish piercing line pattern")
            self.piercing()
        elif self.pattern == "morning":
            print("Searching for bullish morning star pattern")
            self.morning()
        elif self.pattern == "soldiers":
            print("Searching for bullish three white soldier pattern")
            self.soldiers()
        elif self.pattern == "hanging":
            print("Searching for bearish hanging man pattern")
            self.hanging()
        elif self.pattern == "shooting":
            print("Searching for bearish shooting star pattern")
            self.shooting()
        elif self.pattern == "bear_engulf":
            print("Searching for bearish engulfing pattern")
            self.bear_engulf()
        elif self.pattern == "evening":
            print("Searching for bearish evening star pattern")
            self.evening()
        elif self.pattern == "crows":
            print("Searching for bearish three black crows pattern")
            self.crows()
        elif self.pattern == "cloud":
            print("Searching for bearish dark cloud cover pattern")
            self.cloud()
        elif self.pattern == "doji":
            print("Searching for continuation doji pattern")
            self.doji()
        elif self.pattern == "spinning":
            print("Searching for continuation spinning top pattern")
            self.spinning()
        elif self.pattern == "falling":
            print("Searching for continuation falling three method pattern")
            self.falling()
        elif self.pattern == "rising":
            print("Searching for continuation rising three method pattern")
            self.rising()
        else:
            print("Error: Pattern not recognised")
        
        return self.data

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
        mask_short_body = (self.data["Body"] <= self.data["25 Body"])
        # Local minimum
        mask_minimum = (self.data["Min"] == True)
        
        mask = mask_long_wick & mask_short_body & mask_minimum
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "hammer"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "up"

        if self.printout:
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
        mask_long_wick = (1.5*self.data["Body"] <= self.data["U-Wick"])
        # Local minimum
        mask_minimum = (self.data["Min"] == True)

        mask = mask_short_wick & mask_long_wick & mask_minimum
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "inv_hammer"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "up"

        if self.printout:
            if filtered_data.empty:
                print("No inverse hammer pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Inverse hammer patterns detected at:")
                print(filtered_data)

        return filtered_data
    
    def bull_engulf(self) -> pd.DataFrame:
        """
        The bullish engulfing pattern is formed of two candlesticks.
        The first candle is a short red body that is completely engulfed by a larger green candle.
        
        Though the second day opens lower than the first,
        the bullish market pushes the price up,
        culminating in an obvious win for buyers.
        """

        # Second candle has a green body
        mask_second_red = (self.data["Price"] > self.data["Open"])
        # First candle has a red body
        mask_first_green = (self.data["Open"].shift(1) > self.data["Price"].shift(1))
        # First candle has a short body (body within the 50th percentile)
        mask_first_short = (self.data["Body"].shift(1) <= self.data["50 Body"])
        # First candle is engulfed by the second candle
        mask_engulf = (self.data["Open"] < self.data["Price"].shift(1)) & (self.data["Price"] > self.data["Open"].shift(1))

        mask = mask_second_red & mask_first_green & mask_first_short & mask_engulf
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "bull_engulf"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "up"

        if self.printout:
            if filtered_data.empty:
                print("No bullish engulfing pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Bullish engulfing pattern detected at:")
                print(filtered_data)

        return filtered_data
    
    def piercing(self) -> pd.DataFrame:
        """
        The piercing line is also a two-stick pattern,
        made up of a long red candle, followed by a long green candle.
        
        There is usually a significant gap down between the first candlestick's closing price,
        and the green candlestick's opening.
        It indicates a strong buying pressure,
        as the price is pushed up to or above the mid-price of the previous day.
        """

        # Second candle has a green body
        mask_second_green = (self.data["Price"] > self.data["Open"])
        # First candle has a red body
        mask_first_red = (self.data["Open"].shift(1) > self.data["Price"].shift(1))
        # Both candles have long bodies (body greater than the 50th percentile)
        mask_first_long = (self.data["Body"].shift(1) >= self.data["50 Body"])
        mask_second_long = (self.data["Body"] >= self.data["50 Body"])
        # Significant gap down between first candle price and second candle opening
        mask_gap_down = (self.data["Price"].shift(1) - self.data["Open"] >= self.data["25 Body"])
        # Price on second bar must be must be more than halfway up the body of the first bar
        mask_body = (self.data["Price"] >= self.data["Price"].shift(1) + self.data["Body"].shift(1)/2)

        mask = mask_first_red & mask_second_green & mask_first_long & mask_second_long & mask_gap_down & mask_body
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "piercing"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "up"

        if self.printout:
            if filtered_data.empty:
                print("No piercing line pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Piercing line patterns detected at:")
                print(filtered_data)

        return filtered_data
    
    def morning(self) -> pd.DataFrame:
        """
        The morning star candlestick pattern is considered a sign of hope in a bleak market downtrend.
        It is a three-stick pattern: one short-bodied candle between a long red and a long green.
        Traditionally, the 'star' will have no overlap with the longer bodies,
        as the market gaps both on open and close.
        
        It signals that the selling pressure of the first day is subsiding,
        and a bull market is on the horizon.
        """

        # Third candle has a green body
        mask_third_green = (self.data["Price"] > self.data["Open"])
        # First candle has a red body
        mask_first_red = (self.data["Open"].shift(2) > self.data["Price"].shift(2))
        # First and third candles have long bodies (body greater than the 50th percentile)
        mask_first_long = (self.data["Body"].shift(2) >= self.data["50 Body"])
        mask_third_long = (self.data["Body"] >= self.data["50 Body"])
        # Second candle has a short body (less than the 25th percentile)
        mask_second_short = (self.data["Body"].shift(1) <= self.data["25 Body"])

        mask = mask_third_green & mask_first_red & mask_first_long & mask_third_long & mask_second_short
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "morning"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "up"

        if self.printout:
            if filtered_data.empty:
                print("No morning star pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Morning star pattern detected at:")
                print(filtered_data)

        return filtered_data
    
    def soldiers(self) -> pd.DataFrame:
        """
        The three white soldiers pattern occurs over three days.
        It consists of consecutive long green (or white) candles with small wicks,
        which open and close progressively higher than the previous day.
        
        It is a very strong bullish signal that occurs after a downtrend,
        and shows a steady advance of buying pressure.
        """

        # All three bodies are green
        mask_green = (self.data["Price"] > self.data["Open"]) & (self.data["Price"].shift(1) > self.data["Open"].shift(1)) & (self.data["Price"].shift(2) > self.data["Open"].shift(2))
        # All three candles have small wicks (less than 25% of the body)
        mask_upper_wicks = (0.25*self.data["Body"] >= self.data["U-Wick"]) & (0.25*self.data["Body"].shift(1) >= self.data["U-Wick"].shift(1)) & (0.25*self.data["Body"].shift(2) >= self.data["U-Wick"].shift(2))
        mask_lower_wicks = (0.25*self.data["Body"] >= self.data["L-Wick"]) & (0.25*self.data["Body"].shift(1) >= self.data["L-Wick"].shift(1)) & (0.25*self.data["Body"].shift(2) >= self.data["L-Wick"].shift(2))
        # Successive candles open and close progressively higher
        mask_close = (self.data["Price"] > self.data["Price"].shift(1)) & (self.data["Price"].shift(1) > self.data["Price"].shift(2))
        mask_open = (self.data["Open"] > self.data["Open"].shift(1)) & (self.data["Open"].shift(1) > self.data["Open"].shift(2))

        mask = mask_green & mask_lower_wicks & mask_upper_wicks & mask_close & mask_open
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "soldiers"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "up"

        if self.printout:
            if filtered_data.empty:
                print("No three white soldier pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Three white soldier pattern detected at:")
                print(filtered_data)

        return filtered_data
    
    def hanging(self) -> pd.DataFrame:
        """
        The hanging man is the bearish equivalent of a hammer;
        it has the same shape but forms at the end of an uptrend.
        
        It indicates that there was a significant sell-off during the day,
        but that buyers were able to push the price up again.
        The large sell-off is often seen as an indication that the bulls are losing control of the market.
        """

        # Lower wick >= 150% of body
        mask_long_wick = (1.5*self.data["Body"] <= self.data["L-Wick"])
        # Body within the 25th percentile
        mask_short_body = (self.data["Body"] <= self.data["25 Body"])
        # Local maximum
        mask_maximum = (self.data["Max"] == True)

        mask = mask_long_wick & mask_short_body & mask_maximum
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "hanging"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "down"

        if self.printout:
            if filtered_data.empty:
                print("No hanging man pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Hanging man pattern detected at:")
                print(filtered_data)

        return filtered_data
    
    def shooting(self) -> pd.DataFrame:
        """
        The shooting star is the same shape as the inverted hammer,
        but is formed in an uptrend: it has a small lower body, and a long upper wick.
        
        Usually, the market will gap slightly higher on opening,
        and rally to an intra-day high before closing at a price just above the open,
        like a star falling to the ground.
        """

        # Lower wick <= 25% of body
        mask_short_wick = (0.25*self.data["Body"] >= self.data["L-Wick"])
        # Upper wick >= 150% of body
        mask_long_wick = (1.5*self.data["Body"] <= self.data["U-Wick"])
        # Local maximum
        mask_maximum = (self.data["Max"] == True)
        # Candle has a red body
        mask_green = (self.data["Open"] > self.data["Price"])

        mask = mask_short_wick & mask_long_wick & mask_maximum & mask_green
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "shooting"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "down"

        if self.printout:
            if filtered_data.empty:
                print("No shooting star pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Shooting star patterns detected at:")
                print(filtered_data)

        return filtered_data
    
    def bear_engulf(self) -> pd.DataFrame:
        """
        A bearish engulfing pattern occurs at the end of an uptrend.
        The first candle has a small green body that is engulfed by a subsequent long red candle.
        
        It signifies a peak or slowdown of price movement,
        and is a sign of an impending market downturn.
        The lower the second candle goes,
        the more significant the trend is likely to be.
        """

        # Second candle has a red body
        mask_second_red = (self.data["Price"] < self.data["Open"])
        # First candle has a green body
        mask_first_green = (self.data["Price"].shift(1) > self.data["Open"].shift(1))
        # First and second candles have short and long bodies (less than or greater than the 50th percentile)
        mask_first_short = (self.data["Body"].shift(1) <= self.data["50 Body"])
        mask_second_long = (self.data["Body"] >= self.data["50 Body"])
        # First candle is engulfed by the second candle
        mask_engulf = (self.data["Low"] < self.data["Low"].shift(1)) & (self.data["High"] > self.data["High"].shift(1))

        mask = mask_first_green & mask_second_red & mask_first_short & mask_second_long & mask_engulf
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "bear_engulf"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "down"

        if self.printout:
            if filtered_data.empty:
                print("No bearish engulfing pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Bearish engulfing patterns detected at:")
                print(filtered_data)

        return filtered_data
    
    def evening(self) -> pd.DataFrame:
        """
        The evening star is a three-candlestick pattern that is the equivalent of the bullish morning star.
        It is formed of a short candle sandwiched between a long green candle and a large red candlestick.
        
        It indicates the reversal of an uptrend,
        and is particularly strong when the third candlestick erases the gains of the first candle.
        """

        # Third candle has a red body
        mask_third_red = (self.data["Open"] > self.data["Price"])
        # First candle has a green body
        mask_first_green = (self.data["Price"].shift(2) > self.data["Open"].shift(2))
        # First and third candles have long bodies (body greater than the 50th percentile)
        mask_first_long = (self.data["Body"].shift(2) >= self.data["50 Body"])
        mask_third_long = (self.data["Body"] >= self.data["50 Body"])
        # Second candle has a short body (less than the 25th percentile)
        mask_second_short = (self.data["Body"].shift(1) <= self.data["25 Body"])

        mask = mask_first_green & mask_third_red & mask_first_long & mask_third_long & mask_second_short
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "evening"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "down"

        if self.printout:
            if filtered_data.empty:
                print("No evening star pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Evening star pattern detected at:")
                print(filtered_data)

        return filtered_data
    
    def crows(self) -> pd.DataFrame:
        """
        The three black crows candlestick pattern comprises of three consecutive long red candles with short or non-existent wicks.
        Each session opens at a similar price to the previous day,
        but selling pressures push the price lower and lower with each close.
        
        Traders interpret this pattern as the start of a bearish downtrend,
        as the sellers have overtaken the buyers during three successive trading days.
        """

        # All three candles have a red body
        mask_first_red = (self.data["Open"].shift(2) > self.data["Price"].shift(2))
        mask_second_red = (self.data["Open"].shift(1) > self.data["Price"].shift(1))
        mask_third_red = (self.data["Open"] > self.data["Price"])
        # All three with very small wicks
        mask_first_wicks = (0.2*self.data["Body"].shift(2) >= self.data["L-Wick"].shift(2)) & (0.2*self.data["Body"].shift(2) >= self.data["U-Wick"].shift(2))
        mask_second_wicks = (0.2*self.data["Body"].shift(1) >= self.data["L-Wick"].shift(1)) & (0.2*self.data["Body"].shift(1) >= self.data["U-Wick"].shift(1))
        mask_third_wicks = (0.2*self.data["Body"] >= self.data["L-Wick"]) & (0.2*self.data["Body"] >= self.data["U-Wick"])

        mask = mask_first_red & mask_second_red & mask_third_red & mask_first_wicks & mask_second_wicks & mask_third_wicks
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "crows"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "down"

        if self.printout:
            if filtered_data.empty:
                print("No three black crows pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Three black crows pattern detected at:")
                print(filtered_data)

        return filtered_data
    
    def cloud(self) -> pd.DataFrame:
        """
        The dark cloud cover candlestick pattern indicates a bearish reversal,
        a black cloud over the previous day's optimism.
        It comprises two candlesticks:
        a red candlestick which opens above the previous green body, and closes below its midpoint.
        
        It signals that the bears have taken over the session, pushing the price sharply lower.
        If the wicks of the candles are short it suggests that the downtrend was extremely decisive.
        """

        # First candle has a green body
        mask_first_green = (self.data["Price"].shift(1) > self.data["Open"].shift(1))
        # Second candle has a red body
        mask_second_red = (self.data["Open"] > self.data["Price"])
        # Red candle opens above the previous green body
        mask_red_open = (self.data["Open"] > self.data["Price"].shift(1))
        # Red candle closes below the midpoint of the green body
        mask_red_close = (self.data["Price"] < self.data["Open"].shift(1) + self.data["Body"].shift(1)/2)

        mask = mask_first_green & mask_second_red & mask_red_open & mask_red_close
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "cloud"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "down"
        
        if self.printout:
            if filtered_data.empty:
                print("No dark cloud cover pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Dark cloud cover pattern detected at:")
                print(filtered_data)

        return filtered_data
    
    def doji(self) -> pd.DataFrame:
        """
        When a market's open and close are almost at the same price point,
        the candlestick resembles a cross or plus sign,
        and traders should look out for a short to non-existent body, with wicks of varying length.
        
        This doji's pattern conveys a struggle between buyers and sellers that results in no net gain for either side.
        Alone a doji is neutral signal,
        but it can be found in reversal patterns such as the bullish morning star and bearish evening star.
        """

        # Very small bodies
        mask_first_body = (self.data["Body"].shift(1) < self.data["5 Body"].shift(1))
        mask_second_body = (self.data["Body"] < self.data["5 Body"])

        mask = mask_first_body & mask_second_body
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "doji"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "cont"

        if self.printout:
            if filtered_data.empty:
                print("No doji pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Doji pattern detected at:")
                print(filtered_data)
        
        return filtered_data
    
    def spinning(self) -> pd.DataFrame:
        """
        The spinning top candlestick pattern has a short body centered between wicks of equal length.
        The pattern indicates indecision in the market,
        resulting in no meaningful change in price:
        the bulls sent the price higher, while the bears pushed it low again.
        Spinning tops are often interpreted as a period of consolidation, or rest,
        following a significant uptrend or downtrend.
        
        On its own the spinning top is a relatively benign signal,
        but they can be interpreted as a sign of things to come as it signifies that the current market pressure is losing control.
        """

        # Short bodies
        mask_first_body = (self.data["Body"].shift(1) < self.data["25 Body"].shift(1))
        mask_second_body = (self.data["Body"] < self.data["25 Body"])
        # Wicks with approximately equal length (less than 20% difference)
        mask_first_wick = (abs(self.data["U-Wick"].shift(1) - self.data["L-Wick"].shift(1)) < 0.2*self.data["U-Wick"].shift(1))
        mask_second_wick = (abs(self.data["U-Wick"] - self.data["L-Wick"]) < 0.2*self.data["U-Wick"])

        mask = mask_first_body & mask_second_body & mask_first_wick & mask_second_wick
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "spinning"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "cont"
        
        if self.printout:
            if filtered_data.empty:
                print("No spinning top pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Spinning top pattern detected at:")
                print(filtered_data)
        
        return filtered_data
    
    def falling(self) -> pd.DataFrame:
        """
        Three-method formation patterns are used to predict the continuation of a current trend, be it bearish or bullish.
        
        The bearish pattern is called the 'falling three methods'.
        It is formed of a long red body, followed by three small green bodies, and another red body.
        The green candles are all contained within the range of the bearish bodies.
        It shows traders that the bulls do not have enough strength to reverse the trend.
        """

        # First and last bodies are red
        mask_red = (self.data["Open"].shift(4) > self.data["Price"].shift(4)) & (self.data["Open"] > self.data["Price"])
        # Three bodies in the middle are all green
        mask_green = (self.data["Price"].shift(3) > self.data["Open"].shift(3)) & (self.data["Price"].shift(2) > self.data["Open"].shift(2)) & (self.data["Price"].shift(1) > self.data["Open"].shift(1))
        # Green candles contained within the range of the red bodies
        mask_contain_first = (np.minimum(self.data["Low"], self.data["Low"].shift(4)) < self.data["Low"].shift(3))
        mask_contain_third = (np.maximum(self.data["High"], self.data["High"].shift(4)) > self.data["High"].shift(1))
        # There is a falling trend
        mask_falling = (self.data["Price"].shift(4) > self.data["Price"])

        mask = mask_red & mask_green & mask_contain_first & mask_contain_third & mask_falling
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "falling"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "cont"

        if self.printout:
            if filtered_data.empty:
                print("No falling three method pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Falling three method pattern detected at:")
                print(filtered_data)
        
        return filtered_data
    
    def rising(self) -> pd.DataFrame:
        """
        The opposite is true for the bullish pattern, called the 'rising three methods' candlestick pattern.
        It comprises of three short reds sandwiched within the range of two long greens.
        The pattern shows traders that, despite some selling pressure, buyers are retaining control of the market.
        """

        # First and last bodies are green
        mask_green = (self.data["Price"].shift(4) > self.data["Open"].shift(4)) & (self.data["Price"] > self.data["Open"])
        # Three bodies in the middle are all red
        mask_red = (self.data["Open"].shift(3) > self.data["Price"].shift(3)) & (self.data["Open"].shift(2) > self.data["Price"].shift(2)) & (self.data["Open"].shift(1) > self.data["Price"].shift(1))
        # Red candles contained within the range of the green bodies
        mask_contain_first = (np.minimum(self.data["Low"], self.data["Low"].shift(4)) < self.data["Low"].shift(3))
        mask_contain_third = (np.maximum(self.data["High"], self.data["High"].shift(4)) > self.data["High"].shift(1))
        # There is a rising trend
        mask_falling = (self.data["Price"] > self.data["Price"].shift(4))

        mask = mask_red & mask_green & mask_contain_first & mask_contain_third & mask_falling
        filtered_data = self.data.loc[mask].copy()
        self.data.loc[mask, "Pattern"] = filtered_data["Pattern"] = "rising"
        self.data.loc[mask, "Trend"] = filtered_data["Trend"] = "cont"

        if self.printout:
            if filtered_data.empty:
                print("No rising three method pattern detected from", self.start_date, "to", self.end_date)
            else:
                print("Rising three method pattern detected at:")
                print(filtered_data)
        
        return filtered_data
    
    def monte_carlo(self, copies: int, plot: Optional[bool] = True) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Get Monte Carlo data and plot it
        """

        all_data = resampled_data(self.country, copies, self.start_date, self.end_date)

        if plot:
            multiple_candlestick(self.country, all_data, self.start_date)
            monte_carlo_paths(self.country, all_data, self.start_date)
        
        return all_data
    
    def moving_averages(self, short: int, long: int) -> None:
        """
        Calculate short and long moving averages of closing price
        """
        
        self.data["SMA"] = self.data["Price"].rolling(window=short, min_periods=1).mean()
        self.data["LMA"] = self.data["Price"].rolling(window=long, min_periods=1).mean()