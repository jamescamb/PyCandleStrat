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