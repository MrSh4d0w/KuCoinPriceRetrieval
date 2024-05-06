"""
Main file to execute the program. It will obtain the data, represent it, train the IA model and test it.
    Author: Nessico (MrSh4d0w)

"""


"""
    OBTAIN DATA TO STUDY    

"""
import pandas as pd
import marketdata as mkd

# Definition of the crypto to study (BTC-USDT, ETH-USDT, etc.) (coin-pair)
crypto = 'BTC-USDT'

# Definition of the start and end date to study
start_timestamp = mkd.getDatetime_to_timestamp(mkd.getDatetime(2022, 1, 1, 1, 0, 0))
end_timestamp = mkd.getDatetime_to_timestamp(mkd.getDatetime(2024, 3, 6, 11, 15, 0))

# Definition of the temporality to study
temporality = '4hour'

# Definition of the shared list to store the data
shared_list = []

data = mkd.multi_threading(start_timestamp, end_timestamp, temporality, 'BTC-USDT', shared_list)

# Write the data to an Excel file
file = f'BTC-USDT.{temporality}.{mkd.getTimestamp_to_date(start_timestamp)}.{mkd.getTimestamp_to_date(end_timestamp)}'
excel_file = file + '.xlsx'

mkd.write_to_excel(shared_list, excel_file)

"""
    REPRESENT THE DATA 

"""

import graph as g

print(f"Representing the data in a candlestick chart for {crypto} from {mkd.getTimestamp_to_date(start_timestamp)} to {mkd.getTimestamp_to_date(end_timestamp)} with a temporality of {temporality}...")
g.represent_graphic(pd.read_excel(excel_file).head(100), mav=(10, 25, 50))


#   NEXT REAL VALUES MUST BE COMPARED TO THE ACTUAL DATE IF WE CAN OBTAIN IT OR WE ARE TRYING
#   TO OBTAIN VALUES THAT DOESN'T EXIST YET
    
#  WE CAN ALSO COMPARE THE PREDICTIONS WITH THE REAL VALUES OF THE LAST DAYS TO SEE IF THE MODEL
    
# OPERATIONS WITH THE TEMPORALITY USED TO COMPARE THE REAL VALUES AGAINST THE PREDICTIONS
    

