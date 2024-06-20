"""
Import and read data, and convert it to a Pandas dataframe
"""

# Import libraries
import pandas as pd
from typing import Optional

def read_local_file(filename: str):
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
    
    new_data = pd.concat([data, result], axis=1)
    
    return new_data

