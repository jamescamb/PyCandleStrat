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
    
    def evaluate(self) -> float:
        """
        Evaluate all trading strategies
        """

        self.hold_trader()
        self.naive_trader()
    
    def hold_trader(self) -> float:
        """
        Buy at the first instance and sell at the last instance
        """

        funds = self.data["Price"].iloc[-1] - self.data["Price"].iloc[0]

        print("Holding trader gives {:.4f}% net increase on bond yield".format(funds))

        return funds


    def naive_trader(self) -> float:
        """
        Trade only on qualitative candlestick patterns
        """

        funds = 0
        available = True

        for i in self.data.index.tolist()[1:]:
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

        print("Naive candlestick trader gives {:.4f}% net increase on bond yield".format(funds))
        
        return funds