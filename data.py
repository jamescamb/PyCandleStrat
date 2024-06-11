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
        data = pd.read_csv(filename,  dtype={"Data": 'string', "Price": 'float64', "Open": 'float64',
                                             "High": 'float64', "Low": 'float64', "Change": 'float64'})
        print("Successfully read", filename, "into a Panda dataframe")

        # Check for bad data
        bad_values = data.isnull()
        if bad_values.sum().sum() != 0:
            print("Warning: Erroneous values detected \n ")
            data.dropna(inplace=True)
        
        return data
    except:
        print("Error: File not found")
        return None


