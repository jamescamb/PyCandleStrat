"""
Trading government bonds
"""

# Import libraries
import pandas as pd

class Strategy:
    """
    OOP strategy class
    """

    def __init__(self, data: pd.DataFrame) -> None:

        self.data = data
        data["Action"] = "hold"

    def naive_trader(self) -> float:
        """
        Trade only on qualitative candlestick patterns
        """

        funds = 0
        available = True

        for i in self.data.index.tolist()[1:]:
            #if self.data["Trend"].iloc[i - 1] == "up" and available:
            if self.data.loc[i - 1, "Trend"] == "up" and available:
                # Buy bond
                funds -= self.data.loc[i, "Open"]
                self.data.at[i, "Action"] = "buy"
                available = False
            elif self.data.loc[i - 1, "Trend"] == "down" and not available:
                # Sell bond
                funds += self.data.loc[i, "Open"]
                self.data.at[i, "Action"] = "sell"
                available = True
        
        if not available:
            funds += self.data["Price"].iloc[-1]

        print("Naive candlestick trader gives {:.4f}% return on investment".format(100*funds))
        
        return funds