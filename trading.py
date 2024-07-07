"""
Trading government bonds
"""

# Import libraries
import numpy as np
import pandas as pd

from typing import Optional

class Strategy:
    """
    OOP strategy class
    """

    def __init__(self,
                 country: str,
                 data: pd.DataFrame,
                 mc_strat: pd.DataFrame) -> None:

        self.data = data
        self.mc_strat = mc_strat
        self.country = country
        data["Action"] = "hold"
    
    def evaluate(self) -> float:
        """
        Evaluate all trading strategies
        """

        print("Out of Sample:")
        self.hold_trader(self.data, True)
        self.naive_trader(self.data, True)

        print("In Sample")
        returns = []
        self.hold_trader(self.mc_strat, True)
        for i in range(1, self.mc_strat["DF"].iloc[-1] + 1):
            returns.append(self.naive_trader(self.mc_strat[self.mc_strat["DF"] == i]))
        returns = np.array(returns)
        mean, std = np.mean(returns), np.std(returns)
        print("Naive candlestick trader gives on average {:.4f}% net increase on bond yield with {:.4f} standard deviation".format(mean, std))
    
    def hold_trader(self, df: pd.DataFrame, statement: Optional[bool] = False) -> float:
        """
        Buy at the first instance and sell at the last instance
        """

        funds = df["Price"].iloc[-1] - df["Price"].iloc[0]

        if statement:
            print("Holding trader gives {:.4f}% net increase on bond yield".format(funds))

        return funds

    def naive_trader(self, df: pd.DataFrame, statement: Optional[bool] = False) -> float:
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

        if statement:
            print("Naive candlestick trader gives {:.4f}% net increase on bond yield".format(funds))
        
        return funds