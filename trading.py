"""
Trading government bonds
"""

# Import libraries
import numpy as np
import pandas as pd

from typing import Optional, Tuple

class Execute:
    """
    OOP execution class
    """

    def __init__(self,
                 country: str,
                 data: pd.DataFrame) -> None:

        self.data = data
        self.country = country
        data["Action"] = "hold"
    
    def evaluate(self) -> Tuple[float, float, float, float]:
        """
        Evaluate all trading strategies
        """

        print("Out of Sample:")
        self.hold_trader(self.data[self.data["DF"] == 0], True)
        self.naive_trader(self.data[self.data["DF"] == 0], True)

        print("In Sample:")
        returns_hold, returns_naive = [], []
        for i in range(1, self.data["DF"].iloc[-1] + 1):
            returns_hold.append(self.hold_trader(self.data[self.data["DF"] == i]))
            returns_naive.append(self.naive_trader(self.data[self.data["DF"] == i]))
        returns_hold, returns_naive = np.array(returns_hold), np.array(returns_naive)
        mean_hold, std_hold = np.mean(returns_hold), np.std(returns_hold)
        mean_naive, std_naive = np.mean(returns_naive), np.std(returns_naive)
        print("Holding trader gives on average {:.4f}% net increase on bond yield with {:.4f} standard deviation".format(mean_hold, std_hold))
        print("Naive candlestick trader gives on average {:.4f}% net increase on bond yield with {:.4f} standard deviation".format(mean_naive, std_naive))

        return mean_hold, std_hold, mean_naive, std_naive
    
    def hold_trader(self, df: pd.DataFrame, printout: Optional[bool] = False) -> float:
        """
        Buy at the first instance and sell at the last instance
        """

        funds = df["Price"].iloc[-1] - df["Price"].iloc[0]

        if printout:
            print("Holding trader gives {:.4f}% net increase on bond yield".format(funds))

        return funds

    def naive_trader(self, df: pd.DataFrame, printout: Optional[bool] = False) -> float:
        """
        Trade only on qualitative candlestick patterns
        """

        funds = 0
        available = True

        for i in df.index.tolist()[1:]:
            if df.loc[i - 1, "Trend"] == "up" and available:
                # Buy bond
                funds -= df.loc[i, "Open"]
                df.at[i, "Action"] = "buy"
                available = False
            elif df.loc[i - 1, "Trend"] == "down" and not available:
                # Sell bond
                funds += df.loc[i, "Open"]
                df.at[i, "Action"] = "sell"
                available = True
        
        if not available:
            funds += df["Price"].iloc[-1]

        if printout:
            print("Naive candlestick trader gives {:.4f}% net increase on bond yield".format(funds))
        
        return funds