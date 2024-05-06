"""
This module contains the functions to represent the data in a candlestick chart.
    Author: MrSh4d0w

"""

import mplfinance as mpf
import pandas as pd


def represent_graphic(data, mav=(5, 20, 50)):
    """Represent the data in a candlestick chart. 
    If you want to take the data of an excel file use:  pd.read_excel(excel_file)
    You can take the first x elements with: data.head(x)
    You can take the last x elements with: data.tail(x)

    Args:
        data (dataframe): list of dictionaries with the data to represent
        mav (tuple): moving averages (default: (5, 20, 50))
    """

    # Convert the date column to datetime format
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')

    # Set the date column as the index of the DataFrame
    data.set_index('Timestamp', inplace=True)

    # Sort the DataFrame by the index (dates) in ascending order
    data.sort_index(ascending=True, inplace=True)

    # Plot the candlestick chart
    mpf.plot(data, type='candle', style='yahoo', volume=True, mav=(5, 20, 50))

