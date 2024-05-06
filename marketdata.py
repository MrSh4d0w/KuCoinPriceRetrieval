"""
This file contains the functions to retrieve the data from the KuCoin API.
It also contains the functions to write the data to an Excel file and to represent the data in a candlestick chart.
    Author: Nessico (MrSh4d0w)

"""

from datetime import datetime

#  MarketData
from kucoin.client import Market

client = Market(url='https://api.kucoin.com')

"""
    TIMESTAMP CONVERSION

"""
def getServerTimestamp():
    """Get the server timestamp.

    Returns:
        timestamp(int): timestamp in milliseconds
    """
    return client.get_server_timestamp()

def getServerTime():
    """Get the server time.

    Returns:
        datetime: server time
    """
    return datetime.fromtimestamp(getServerTimestamp()/1000)

def getDatetime(year, month, day, hour, minute, second):
    """Define a date in datetime format.

    Args:
        year (int): year
        month (int): month
        day (int): day
        hour (int): hour
        minute (int): minute
        second (int): second

    Returns:
        datetime: date
    """
    return datetime(year, month, day, hour, minute, second)

def getTimestamp_to_date(timestamp):
    """Convert timestamp (ms) to date (day, month, year).

    Args:
        timestamp (int): timestamp in milliseconds

    Returns:
        datetime: timestamp in date format (day, month, year)
    """
    return datetime.fromtimestamp(int(timestamp)).strftime('%d-%m-%Y')

def getTimestamp_to_datetime(timestamp):
    """Convert timestamp (ms) to date.

    Returns:
        datetime: timestamp in date format
    """
    return datetime.fromtimestamp(int(timestamp/1000))
    
def getDatetime_to_timestamp(date):
    """Convert date to timestamp (ms).
    It returned in ms to be consistent with the server timestamp.
    KuCoin uses ms for the timestamp.
    Returns:
        int: date in timestamp format (ms)
    """
    return int(date.timestamp())


"""
    DATA PROCESSING

"""


"""
    WRITE ON EXCEL THE DATA RETRIEVED
"""
from openpyxl import Workbook
from datetime import datetime

def write_to_excel(data, filename):
    """Write the data to an Excel file.

    Args:
        data (list): list of lists containing the data
        filename (str): name of the file
    """
    # Create a new workbook
    wb = Workbook()

    # Select the active sheet
    ws = wb.active

    # Add headers
    ws.append(["Timestamp", "Open", "Close", "High", "Low", "Volume", "base_volume"])

    # Create empty lists to store the values
    timestamps, open_prices, close_prices, high_prices, low_prices, volumes, base_volumes = ([] for _ in range(7))

    # Iterate over the data and write them to the Excel file
    for sublist in data:
        timestamp, open_price, close_price, high_price, low_price, volume, base_volume = sublist
        #timestamp_seconds = int(timestamp)  # Convert the timestamp to seconds
        #date = datetime.fromtimestamp(timestamp_seconds/1000)  # Convert the timestamp to date and time

        # Add the values to the current row
        row = [timestamp, float(open_price), float(close_price), float(high_price), float(low_price), float(volume), float(base_volume)]
        ws.append(row)

        # Append the values to the lists
        timestamps.append(timestamp)
        open_prices.append(float(open_price))
        close_prices.append(float(close_price))
        high_prices.append(float(high_price))
        low_prices.append(float(low_price))
        volumes.append(float(volume))
        base_volumes.append(float(base_volume))

    # Save the Excel file
    wb.save(filename)

    print(f"\nData has been written to {filename}")

"""
    GET DATA FROM KUCOIN API
    
"""
    
def getData(coin, interval, start, end, shared_data, writeOnExcel=False):
    """Get the data from the KuCoin API.
    Due to limitations in KuCoin API it only can retrieve 1500 elements.
    
    Args:
        coin (str): coin pair (e.g. BTC-USDT)
        interval (str): interval (1min, 5min, 15min, 1hour, 4hour, 8hour, 1day, 1week, 1month)
        start (int): start timestamp
        end (int): end timestamp
        writeOnExcel (bool): write the data to an Excel file (default: False)

    Returns:
        list: data
    """
    print(f"Getting data for {coin} from {start} to {end}")
    data = client.get_kline(coin, interval, startAt=start, endAt=end)
    file = f"{coin}.{interval}.{start}.{end}.xlsx"

    print(data)

    if writeOnExcel:
        write_to_excel(data, file)
    
    shared_data.extend(data)

    return data

"""
    MULTI-THREADING

"""
import threading

def multi_threading(start_timestamp, end_timestamp, temporality, coin, shared_data):
    """Retrieve the data in multiple threads.

    Args:
        start_timestamp (int): start timestamp
        end_timestamp (int): end timestamp
        temporality (str): temporality (1min, 5min, 15min, 1hour, 4hour, 8hour, 1day, 1week, 1month)
        coin (str): coin pair (e.g. BTC-USDT)
        shared_data (list): shared list to store the data
    
    Returns:
        list: shared list with the data
    """

    temporalities = {
        '1min': 1500 * 60,
        '5min': 1500 * 60 * 5,
        '15min': 1500 * 60 * 15,
        '1hour': 1500 * 60 * 60,
        '4hour': 1500 * 60 * 60 * 4,
        '8hour': 1500 * 60 * 60 * 8,
        '1day': 1500 * 60 * 60 * 24,
        '1week': 1500 * 60 * 60 * 24 * 7,
        '1month': 1500 * 60 * 60 * 24 * 30
    }

    num_threads = (end_timestamp - start_timestamp) // temporalities[temporality] + 1
    threads = []

    for i in range(num_threads):
        # We control the ranges with the i variable
        print(f"Thread {i} of {num_threads}")
        print("Start timestamp:", start_timestamp + i * temporalities[temporality])
        
        # Calculate the range of timestamps for the current thread
        start = start_timestamp + i * temporalities[temporality]

        # Calculate the end timestamp for the current thread
        end = min(start_timestamp + (i + 1) * temporalities[temporality], end_timestamp)

        thread = threading.Thread(target=getData, args=(coin, temporality, start, end, shared_data, False))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return shared_data

if __name__ == '__main__':
    # Definition of the crypto to study (BTC-USDT, ETH-USDT, etc.) (coin-pair)
    crypto = 'BTC-USDT'

    # Definition of the start and end date to study
    start_timestamp = getDatetime_to_timestamp(getDatetime(2021, 1, 1, 1, 0, 0))
    end_timestamp = getDatetime_to_timestamp(getDatetime(2024, 3, 6, 11, 15, 0))

    # Definition of the temporality to study
    temporality = '1hour'

    # Definition of the shared list to store the data
    shared_list = []

    data = multi_threading(start_timestamp, end_timestamp, temporality, 'BTC-USDT', shared_list)


    # Write the data to an Excel file
    file = f'BTC-USDT.{temporality}.{getTimestamp_to_date(start_timestamp)}.{getTimestamp_to_date(end_timestamp)}'
    excel_file = file + '.xlsx'

    write_to_excel(shared_list, excel_file)