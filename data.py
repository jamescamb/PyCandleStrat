"""
Import and read data, and convert it to a Pandas dataframe
"""

# Import libraries
import random
import numpy as np
import pandas as pd
from typing import Optional

random.seed(0)
np.random.seed(0)

def read_local_file(filename: str, confirm: Optional[bool] = True):
    """
    Read in a local CSV file and return a Panda dataframe
    """

    try:
        # Applicable to data from 'investing.com'
        data = pd.read_csv(filename,  dtype={"Date": 'string',
                                             "Price": 'float',
                                             "Open": 'float',
                                             "High": 'float',
                                             "Low": 'float',
                                             "Change %": 'string'})
        if confirm:
            print("Successfully read", filename, "into a Panda dataframe")
            print("Bond yield data has", data.shape[0], "entries")
        
        return data
    except:
        print("Error: File not found or invalid")
        return None

def check_bad_values(data: pd.DataFrame) -> pd.DataFrame:
    """
    Check for null or missing values and delete them
    """

    bad_values = data.isnull()
    if bad_values.sum().sum() != 0:
        print("Warning: Erroneous values detected")
        data.dropna(inplace=True)
    
    return data

def correct_dates(data: pd.DataFrame) -> pd.DataFrame:
    """
    Convert string dates to Panda datetime type
    """

    data["Date"] = pd.to_datetime(data["Date"], format="%m/%d/%Y")
    
    return data

def correct_changes(data: pd.DataFrame) -> pd.DataFrame:
    """
    Convert string percentage changes to floats
    """

    data["Change %"] = data["Change %"].apply(lambda x: float(x[:-1]))

    return data

def check_date(date: str) -> None:
    """
    Make sure the string input date is valid,
    otherwise raise an exception error
    """

    valid = True
    arr = date.split("-")

    if len(arr) != 3:
        valid = False
    else:
        year, month, day = arr[0], arr[1], arr[2]
        if len(year) != 4 or int(year) < 0:
            valid = False
        if int(month) > 12 or int(month) < 1:
            valid = False
        if int(day) > 31 or int(day) < 1:
            valid = False

    if valid == False:
        raise Exception("Error: Invalid date entered")

def filter_data(data: pd.DataFrame,
                start_date: str,
                end_date: str) -> pd.DataFrame:
    """
    Filter data by dates
    """

    start_date = pd.to_datetime(start_date, format="%Y-%m-%d")
    end_date = pd.to_datetime(end_date, format="%Y-%m-%d")
    mask = (data["Date"] >= start_date) & (data["Date"] <= end_date)
    filtered_data = data.loc[mask]

    return filtered_data

def asym_rolling_minmax(data: pd.DataFrame,
                        look_back: int,
                        look_forward: int,
                        minimum: bool) -> list:
    """
    Create an asymmetrical local minimum searching function
    """

    result = []
    n = data.shape[0]

    for i in range(n):
        start = max(0, i - look_back)
        end = min(n, i + look_forward + 1)
        window = data["Price"][start:end]
        if minimum:
            result.append(min(window))
        else:
            result.append(max(window))

    return result

def expanding_quantiles(data: pd.DataFrame,
                        column: str,
                        quantiles: Optional[list] = [0.25, 0.50, 0.75]) -> pd.DataFrame:
    """
    Calculate quantiles for a specific column called "column"
    Data is time-consistent, i.e. we only use data up to that point in time
    """

    result = pd.DataFrame(index = data.index, columns=[f"{int(q*100)}" + " " + column for q in quantiles], dtype='float')

    for i in range(1, len(data) + 1):
        result.iloc[i - 1] = data[column].iloc[:i].quantile(quantiles).values
    
    return result

def shuffle_with_window_size(values: list, window_size: int) -> list:
    """
    Shuffle a list, while maintaining consecutive values of length 'window size'
    """

    chunks = [values[i : i + window_size] for i in range(0, len(values), window_size)]
    random.shuffle(chunks)
    shuffled_list = [item for chunk in chunks for item in chunk]
    
    return shuffled_list

def resampled_data(country: str, copies: int, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Monte Carlo inspired method for producing synthetic data over all OHLC values 
    """

    filename = country + "-bond-yield.csv"
    df = read_local_file(filename, False)
    if df is None:
        raise Exception("Program closing.")
    else:
        check_bad_values(df)
        correct_dates(df)
        correct_changes(df)
        df.sort_values(["Date"], ignore_index=True, inplace=True)
    
    df["DF"] = 0
    dataframes = [df.copy()]

    for i in range(copies):
        new_df = df.copy()
        for col in ["Open", "High", "Low"]:
            new_df[col] = new_df[col] / new_df["Price"]
        new_df["Price"] = new_df["Price"].pct_change()
        #new_df.loc[1:, "Price"] = np.random.permutation(new_df.loc[1:, "Price"].values)
        new_df.loc[1:, "Price"] = shuffle_with_window_size(new_df.loc[1:, "Price"].values, 10)
        new_df.loc[0, "Price"] = df.loc[0, "Price"]
        for j in range(1, len(new_df)):
            new_df.at[j, "Price"] = (1 + new_df.at[j, "Price"]) * new_df.at[j - 1, "Price"]
        for col in ["Open", "High", "Low"]:
            new_df[col] = new_df[col] * new_df["Price"]
        new_df["Change %"] = 100 * new_df["Price"].pct_change()
        new_df["Change %"] = new_df["Change %"].fillna(0)
        new_df["DF"] = i + 1
        dataframes.append(new_df)
    
    df_combined = pd.concat(dataframes)

    mask = (df_combined["Date"] >= start_date) & (df_combined["Date"] <= end_date)
    df_combined = df_combined.loc[mask]

    return df_combined

def count_patterns(df: pd.DataFrame) -> list:
    """
    Count how many patterns are identified for each Monte Carlo shuffle
    """

    n_patterns = []

    for i in range(df["DF"].iloc[-1] + 1):
        n_patterns.append(len([s for s in df[df["DF"] == i]["Pattern"] if s != ""]))
    
    return n_patterns