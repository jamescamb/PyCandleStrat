"""
Import and read data, and convert it to a Pandas dataframe
"""

# Import libraries
import pandas as pd

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